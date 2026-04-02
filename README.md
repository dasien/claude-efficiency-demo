# Claude Code Token Efficiency Testing Framework

A framework for empirically comparing different Claude Code configuration strategies to find the most token-efficient approach for a given task.

## Quick Start

```bash
pip install rich
python3 runner.py list      # See available variations and tasks
python3 runner.py open       # Open a new run group (auto-timestamped)
python3 runner.py run       # Run a test (interactive menu)
python3 runner.py run       # Run more tests — all go into the active group
python3 runner.py compare   # Generate comparison.md for the active group
python3 runner.py runs      # List all run groups
```

## How It Works

1. **Open a run group** with `python3 runner.py open` — creates a timestamped folder to collect related runs
2. Pick a **variation** (a Claude Code configuration strategy) and a **task** (a standardized prompt)
3. The runner creates an ephemeral temp directory with the variation's `.claude/` folder, task seed files, and a git repo
4. Copies the `claude` command to your clipboard — paste and run it in another terminal
5. After the run completes, press Enter to collect metrics from the session logs
6. Results (JSON + output artifacts) are saved into the active run group under `results/<run_group>/`
7. Run `python3 runner.py compare` to generate a `comparison.md` report for the active group

## Variations

Each variation is a different `.claude/` folder configuration testing a different approach to providing Claude with knowledge and delegation patterns.

| # | Variation | Description |
|---|-----------|-------------|
| 1 | **vanilla-claude** | No CLAUDE.md, no agents, no skills. Bare Claude Code with only its default system prompt. The control group. |
| 2 | **monolithic** | A single large CLAUDE.md (~475 lines) containing all knowledge inline — Python coding standards, architecture guidelines, testing methodology, Tkinter patterns, C# standards, SQL best practices, and REST API patterns. No agents or skills. |
| 3 | **skills-only** | A light CLAUDE.md that references 8 skills (`.claude/skills/`). Skills are loaded inline into the main context when invoked via `/skill-name`. No agents — all work happens in the main session. |
| 4 | **skills-and-agents** | A light CLAUDE.md with 3 specialized agents (architect, python-expert, tester). Each agent has all 8 skills preloaded via `skills:` frontmatter — skill content is injected into the agent's context at spawn time, whether or not the skill is needed. |
| 5 | **agents-ondemand-skills** | Same 3 agents as above, but skills are NOT preloaded. Instead, agent prompts instruct them to invoke `/skill-name` on demand. Only skills that are actually needed get loaded into the agent's context. |
| 6 | **agents-ondemand-optimized** | Refined on-demand approach with 3 consolidated agents (doc-writer, implementer, tester instead of per-phase agents), explicit instructions to return only file paths (not contents), and rules against reading back agent output. |

### Skills Available (variations 3-6)

| Skill | Relevant to Calculator Task? |
|-------|------------------------------|
| python-coding | Yes |
| architecture | Yes |
| testing | Yes |
| requirements | Yes |
| gui-tkinter | Yes (GUI task only) |
| server-api | No (noise) |
| csharp-coding | No (noise) |
| sql-development | No (noise) |

The 4 irrelevant skills test whether each approach wastes tokens on unused knowledge.

## Tasks

Tasks are standardized prompts at increasing complexity levels. Each variation runs the same prompt.

| # | Task | Description |
|---|------|-------------|
| 1 | **python-calculator** | Build a CLI calculator with +, -, *, / operations, a REPL loop, input validation, and pytest tests. Code and tests only — no documentation phase. |
| 2 | **python-calculator-docs** | Same calculator but with 6 phases: requirements doc, architecture doc, coding plan, test plan, implementation, and test execution. Tests whether documentation phases change the cost dynamics. |
| 3 | **python-calculator-gui** | Build a Tkinter GUI calculator with button grid, keyboard input, MVC architecture, and full 6-phase documentation. The most complex task — tests whether GUI-specific skills (tkinter) provide value and whether agent delegation pays off for larger tasks. |

### Custom Prompts

Override a task's default prompt:
```bash
python3 runner.py run --prompt "Build a REST API with Flask"
```

## Results

Results are saved to `results/` with:
Results are organized into **run groups** (created with `python3 runner.py open`):

```
results/
├── run_20260401-201253/                    # A run group
│   ├── monolithic_advanced-calculator_20260401-203611/
│   │   ├── result.json                     # Metrics, prompt, cost
│   │   └── output/                         # All files Claude produced
│   │       ├── docs/
│   │       ├── calculator/
│   │       └── tests/
│   ├── skills-only_advanced-calculator_20260401-205804/
│   │   ├── result.json
│   │   └── output/
│   ├── comparison.md                       # Generated by 'compare'
│   └── run-analysis.md                     # Manual analysis
├── run_20260402-.../                       # Another run group
└── .current-run                            # Tracks the active group
```

### Metrics Collected

| Metric | Description |
|--------|-------------|
| input_tokens | Non-cached input tokens |
| output_tokens | Generated output tokens |
| cache_creation_tokens | Tokens written to cache (expensive: $18.75/M for Opus) |
| cache_read_tokens | Tokens read from cache (cheap: $1.50/M for Opus) |
| estimated_cost_usd | Calculated cost based on model pricing |
| peak_context_main | Highest context window usage in the main session |
| peak_context_any | Highest context across main + all sub-agents |
| final_context_main | Context size at the end of the main session |
| skills_used | Which skills were invoked during the run |
| agents_used | Which agents were spawned during the run |

### Comparing Results

```bash
python3 runner.py compare              # Generate comparison.md for active group
python3 runner.py compare --group run_20260401-201253  # Compare a specific group
python3 runner.py runs                 # List all run groups
```

## Findings

See [results/run-findings.md](results/run-findings.md) for detailed analysis including cost-quality tradeoffs, context window usage, and recommendations.

## Adding New Variations

1. Create a directory under `variations/` with a `.claude/` folder inside
2. Add a `description.txt` with a short description
3. Populate `.claude/` with your CLAUDE.md, skills, and/or agents
4. Add the variation name to `VARIATION_ORDER` in `runner.py` for display ordering

## Adding New Tasks

1. Create a `.md` file in `tasks/` with the task prompt
2. Create a matching `.desc` file with a short description (e.g., `my-task.desc`)
3. Add the task name to `TASK_ORDER` in `runner.py` for display ordering

## Requirements

- Python 3.10+
- `rich` (for terminal UI)
- Claude Code CLI installed and authenticated
