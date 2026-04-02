# Claude Code Token Efficiency — Run Findings

## Overview

This document captures findings from running 6 configuration variations across 3 task complexities to measure cost, quality, and context window usage in Claude Code.

**Date:** 2026-04-01
**Model:** claude-opus-4-6 (all runs, including sub-agents)
**Pricing:** Opus — $15/M input, $75/M output, $18.75/M cache creation, $1.50/M cache read

---

## Variations Tested

1. **vanilla-claude** — No CLAUDE.md, no agents, no skills (control)
2. **monolithic** — Large CLAUDE.md with all knowledge inline (~475 lines)
3. **skills-only** — Light CLAUDE.md, 8 skills available, no agents
4. **skills-and-agents** — Light CLAUDE.md, 3 agents with 8 skills preloaded via frontmatter
5. **agents-ondemand-skills** — Light CLAUDE.md, 3 agents that invoke skills via `/skill-name`
6. **agents-ondemand-optimized** — Light CLAUDE.md, 3 consolidated agents, on-demand skills, terse return instructions

## Tasks Tested

1. **python-calculator** — Simple: CLI calculator, code + tests only
2. **python-calculator-docs** — Medium: CLI calculator with requirements, architecture, coding plan, test plan docs
3. **python-calculator-gui** — Complex: Tkinter GUI calculator with full docs, MVC architecture, and tests

---

## GUI Calculator Task — Full Results

This was the most comprehensive test, run across all 6 variations.

### Cost & Efficiency

| Rank | Variation | Cost | Total Tokens | Cache Create | Cache Read | Messages | Tool Calls | Agent Spawns |
|------|-----------|------|-------------|-------------|------------|----------|------------|-------------|
| 1 | vanilla-claude | $2.69 | 491,151 | — | — | 20 | 11 | 0 |
| 2 | monolithic | $3.94 | 722,597 | 101,199 | 606,287 | 23 | 12 | 0 |
| 3 | skills-only | $4.91 | 887,113 | 138,819 | 732,140 | 31 | 18 | 0 |
| 4 | agents-ondemand-optimized | $6.65 | 700,586 | 218,186 | 457,329 | 43 | 26 | 3 |
| 5 | agents-ondemand-skills | $7.39 | 953,696 | 226,068 | 699,557 | 59 | 30 | 7 |
| 6 | skills-and-agents | $8.13 | 941,728 | 232,593 | 672,271 | 50 | 24 | 7 |

### Context Window Usage

| Variation | Peak Main Context | Peak Any Sub-Agent |
|-----------|------------------|-------------------|
| agents-ondemand-optimized | 21,943 | 23,310 |
| vanilla-claude | 32,042 | — |
| skills-and-agents | 33,277 | 20,281 |
| agents-ondemand-skills | 38,193 | 16,291 |
| skills-only | 41,880 | — |
| monolithic | 42,098 | — |

### Quality Assessment

| Variation | Docs Lines | Test Functions | Eval Safety | Extra Features | Quality Score (1-5) |
|-----------|-----------|---------------|-------------|----------------|-------------------|
| vanilla-claude | 450 | 31 | eval() | — | 3.3 |
| monolithic | 506 | 57 | AST-safe | backspace | 4.1 |
| skills-only | 499 | 36 | manual dispatch | backspace | 3.6 |
| skills-and-agents | 1,417 | 54 | eval() | backspace, toggle_sign, percent | 4.4 |
| agents-ondemand-skills | 1,094 | 28 | eval() | — | 3.6 |
| agents-ondemand-optimized | 1,133 | 50 | eval() | — | 4.2 |

### Cost-Quality Overlay

| Variation | Cost | Quality | $/Quality Point | Efficiency Rank |
|-----------|------|---------|----------------|-----------------|
| vanilla-claude | $2.69 | 3.3 | $0.82 | 1st |
| monolithic | $3.94 | 4.1 | $0.96 | 2nd |
| skills-only | $4.91 | 3.6 | $1.36 | 3rd |
| agents-ondemand-optimized | $6.65 | 4.2 | $1.58 | 4th |
| skills-and-agents | $8.13 | 4.4 | $1.85 | 5th |
| agents-ondemand-skills | $7.39 | 3.6 | $2.05 | 6th |

---

## Cross-Task Cost Comparison

Results from running 4 variations across all 3 task complexities (before unused skills were added):

| Variation | Simple | Docs | GUI | Scaling Factor (Simple→GUI) |
|-----------|--------|------|-----|----------------------------|
| monolithic | $2.09 | $2.47 | $3.94 | 1.9x |
| skills-only | $0.82 | $3.44 | $4.91 | 6.0x |
| skills-and-agents | $1.91 | $6.19 | $8.13 | 4.3x |
| agents-ondemand-skills | $1.63 | $7.69 | $7.39 | 4.5x |

---

## Key Findings

### 1. Cache Economics Dominate Cost

Cache creation tokens cost 12.5x more than cache reads ($18.75 vs $1.50 per million). The single biggest cost driver across all variations is how many cache creation events occur.

- **Single-context approaches** (vanilla, monolithic, skills-only) pay cache creation once, then amortize across many cheap cache reads.
- **Agent-based approaches** pay cache creation per agent spawn. With 7 agents, that's 7 separate cache creation events.

### 2. Monolithic Scales Best on Cost

Despite having the largest CLAUDE.md (475 lines with unused C#/SQL/API content), monolithic consistently delivered good cost-quality ratios. The one-time cache creation cost of a large system prompt is amortized across all subsequent messages in the session.

### 3. Agent Coordination Has Real Overhead

Agent-based variations used 2-3x more messages and tool calls than non-agent variations for the same task. Each agent spawn, delegation, and result return adds turns that accumulate cost.

### 4. Unused Preloaded Skills Are Wasteful

When 4 irrelevant skills (C#, SQL, API, GUI) were added to all variations:
- **skills-and-agents** ($8.13) became more expensive than **agents-ondemand** ($7.39) because preloading injects all skill content into each agent's system prompt, even if unused.
- **On-demand loading** skips unused skills entirely, paying only for what's invoked.

### 5. On-Demand Agents Return Too Much Context

The original on-demand agents returned full document contents (47,689 chars) back to the main session, inflating its context. Preloaded agents returned only brief summaries (21,010 chars). This is a prompting issue, not an architectural one — the optimized variation fixed it with explicit "return only file paths" instructions.

### 6. Optimized Agents Show the Path Forward

The optimized variation reduced costs by 10% and tokens by 27% vs the original on-demand approach through three changes:
- **Fewer agents** (3 vs 7): fewer cache creation events
- **Terse returns**: 22K main context vs 38K
- **File paths not contents**: agents coordinated without bloating the main session

### 7. Quality Correlates with Agent Usage

Agent-based variations consistently produced 2-3x more documentation (1,100-1,400 lines vs 450-500 lines) and more comprehensive test suites. The quality premium exists but costs 2-3x more.

### 8. Skills Run Inline by Default — This Is Cheap

Skills without `context: fork` load into the parent's existing cached context. They extend the cache rather than creating a new one. This is why skills-only was efficient — it leveraged the parent's cache for all skill content.

### 9. Context Window Was Never a Constraint

Peak context usage ranged from 22K to 42K tokens across all variations — well under the 200K context limit, let alone the 1M window. For these task sizes, context management via agents was solving a problem that didn't exist. Agents would become valuable for tasks that approach context limits.

### 10. Vanilla Claude Is Surprisingly Capable

With zero configuration, vanilla Claude produced working code, docs, and tests at $2.69 — the cheapest run. Quality was the lowest (3.3) but adequate. This suggests configuration overhead should be justified by measurable quality improvements.

---

## Cost Breakdown: Where the Money Goes (Optimized Agents)

| Component | Cache Creation | Cost |
|-----------|---------------|------|
| Main session | 61,901 tokens | $1.16 |
| Doc-writer agent (5 skills) | 64,157 tokens | $1.20 |
| Implementer agent (2 skills) | 60,499 tokens | $1.13 |
| Tester agent (0 skills) | 31,629 tokens | $0.59 |
| **Total cache creation** | **218,186 tokens** | **$4.09** |
| Output tokens | 24,992 tokens | $1.87 |
| Cache reads | 457,329 tokens | $0.69 |
| **Grand total** | | **$6.65** |

Cache creation accounts for **61% of total cost**. The base Claude Code system prompt contributes ~30K tokens per agent spawn regardless of skills loaded.

---

## Potential Optimizations Not Yet Tested

1. **Model: sonnet for agents** — Cache creation at $3.75/M instead of $18.75/M (5x cheaper). Estimated savings: ~$2.34 on the optimized variation.
2. **Hybrid inline + forked skills** — Do most work inline (cheap cache reads), fork only heavy tasks (test execution) to isolate verbose output.
3. **Single-agent architecture** — One agent for everything, eliminating multiple cache creation events.
4. **`--bare` mode for agents** — Strip the default Claude Code system prompt to reduce the ~30K base tokens per agent.

---

## Recommendations

### For cost-sensitive work:
Use **monolithic** or **skills-only**. Single-context approaches minimize cache creation and deliver adequate quality. Monolithic offers the best cost-quality ratio at $0.96 per quality point.

### For quality-sensitive work:
Use **agents-ondemand-optimized** with consolidated agents and terse return instructions. Consider using `model: sonnet` for agents to cut costs further. This delivers near-top quality (4.2/5) with controlled costs.

### For maximum quality regardless of cost:
Use **skills-and-agents** with preloaded skills. Highest quality (4.4/5) but at the highest cost ($8.13).

### General principles:
- Prefer fewer, broader agents over many specialized ones
- Instruct agents to return file paths, not contents
- Use on-demand skill loading when many skills exist but few are needed per task
- Use preloaded skills when every skill will be used by the agent
- Skills running inline (without `context: fork`) are cheaper than agent delegation
- Cache creation is the primary cost lever — minimize the number of fresh context events
