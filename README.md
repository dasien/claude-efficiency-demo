# Claude Code Token Efficiency Testing Framework

A framework for empirically comparing different Claude Code configuration strategies to find the most token-efficient approach for a given task.

## Quick Start

```bash
pip install rich
python3 runner.py list      # See available variations and tasks
python3 runner.py run       # Run a test (interactive menu)
python3 runner.py compare   # Compare results from previous runs
```

## How It Works

1. Pick a **variation** (a Claude Code configuration strategy) and a **task** (a standardized prompt)
2. The runner creates an ephemeral temp directory with the variation's `.claude/` folder and a git repo
3. Copies the `claude` command to your clipboard — paste and run it in another terminal
4. After the run completes, press Enter to collect metrics from the session logs
5. Results (JSON + output artifacts) are saved to `results/`

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
- **JSON metrics**: `<variation>_<task>_<timestamp>.json` — tokens, cost, context usage, skills/agents used
- **Output artifacts**: `<variation>_<task>_<timestamp>/output/` — all docs, source code, and tests produced

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
python3 runner.py compare   # Table of all runs
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
