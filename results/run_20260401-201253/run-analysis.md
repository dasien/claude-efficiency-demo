# Run Analysis — Advanced Calculator (3-Mode: Basic/Scientific/Programmer)

**Run Group:** run_20260401-201253
**Task:** advanced-calculator (pre-written 568-line requirements doc)
**Model:** claude-opus-4-6 (all runs)

---

## Cost & Efficiency (Ranked by Cost)

| Rank | Variation | Cost | Total Tokens | Cache Create | Cache Read | Output | Msgs | Tools |
|------|-----------|------|-------------|-------------|------------|--------|------|-------|
| 1 | monolithic | **$8.56** | 2,407,319 | 130,857 | 2,239,860 | 36,549 | 45 | 35 |
| 2 | vanilla-claude | $10.42 | 2,904,030 | 151,692 | 2,705,367 | 46,910 | 53 | 39 |
| 3 | skills-only | $11.84 | 3,230,821 | 195,382 | 2,985,981 | 49,342 | 86 | 57 |
| 4 | agents-ondemand-optimized | $20.96 | 3,658,772 | 609,145 | 2,981,948 | 67,553 | 90 | 57 |
| 5 | skills-and-agents | $23.50 | 3,832,074 | 708,628 | 3,043,366 | 74,151 | 142 | 89 |
| 6 | agents-ondemand-skills | **$35.18** | 5,502,653 | 1,076,606 | 4,307,096 | 112,519 | 175 | 107 |

## Context Window Usage

| Variation | Peak Main Context | Peak Any Context |
|-----------|------------------:|------------------:|
| agents-ondemand-optimized | 32,388 | 70,578 |
| agents-ondemand-skills | 60,607 | 72,386 |
| skills-and-agents | 75,026 | 75,026 |
| skills-only | 75,584 | 75,584 |
| monolithic | 82,608 | 82,608 |
| vanilla-claude | 85,489 | 85,489 |

---

## Quality Assessment

### Artifact Sizes

| Variation | Doc Lines | Source Lines | Test Lines | Test Functions |
|-----------|----------|-------------|------------|---------------|
| vanilla-claude | 1,180 | 2,147 | 1,060 | 119 |
| monolithic | 1,212 | 2,049 | 1,036 | 123 |
| skills-only | 1,044 | 1,747 | 1,231 | 96 |
| skills-and-agents | 1,911 | 2,560 | 1,165 | 80 |
| agents-ondemand-skills | **3,347** | **3,013** | **1,594** | **150** |
| agents-ondemand-optimized | 2,047 | 3,139 | 1,264 | 131 |

### Feature Completeness

All 6 variations successfully implemented:
- All 3 modes (Basic, Scientific, Programmer) with separate views and logic
- Mode switching
- Full file structure following the suggested layout (calculator/gui/, calculator/logic/, tests/)

| Feature | Vanilla | Mono | Skills | Sk+Agents | AgentsOD | AgentsOpt |
|---------|---------|------|--------|-----------|----------|-----------|
| All 3 modes | Yes | Yes | Yes | Yes | Yes | Yes |
| Mode switching | Yes | Yes | Yes | Yes | Yes | Yes |
| Memory functions | Yes | Yes | Yes | Yes | Yes | Yes |
| Base conversion | Yes | Yes | Yes | Yes | Yes | Yes |
| Bitwise ops | Yes | Yes | Yes | Yes | Yes | Yes |
| Trig functions | Yes | Yes | Yes | Yes | Yes | Yes |
| Word size | Yes | Yes | Yes | Yes | Yes | Yes |
| Eval safety | Manual | Manual | Manual | Manual | Manual | **eval()** |
| Tests passing | All | All | All | All | **3 failed** | All |

### Quality Scores (1-5)

| Criterion | Vanilla | Mono | Skills | Sk+Agents | AgentsOD | AgentsOpt |
|-----------|---------|------|--------|-----------|----------|-----------|
| Doc depth | 3.5 | 3.5 | 3.0 | 4.5 | **5.0** | 4.5 |
| Code completeness | 4.0 | 4.0 | 3.5 | 4.5 | **4.5** | 4.5 |
| Test coverage | 4.0 | 4.0 | 3.5 | 3.5 | **4.5** | 4.0 |
| Code safety | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | **3.0** (eval) |
| Tests passing | 5.0 | 5.0 | 5.0 | 5.0 | **4.0** | 5.0 |
| **Overall** | **4.1** | **4.1** | **3.8** | **4.3** | **4.4** | **4.2** |

---

## Cost-Quality Overlay

| Variation | Cost | Quality | $/Quality Point | Efficiency Rank |
|-----------|------|---------|----------------|-----------------|
| **monolithic** | $8.56 | 4.1 | **$2.09** | **1st** |
| vanilla-claude | $10.42 | 4.1 | $2.54 | 2nd |
| skills-only | $11.84 | 3.8 | $3.12 | 3rd |
| agents-ondemand-optimized | $20.96 | 4.2 | $4.99 | 4th |
| skills-and-agents | $23.50 | 4.3 | $5.47 | 5th |
| agents-ondemand-skills | $35.18 | 4.4 | $7.99 | 6th |

---

## Key Findings

### 1. Scale Changes Everything — But Not the Winner

At this scale (2.4M-5.5M tokens, vs 500K-950K for the GUI task), the cost spread widened dramatically. Monolithic at $8.56 vs agents-ondemand at $35.18 is a **4.1x difference**. For the simple GUI task it was only 1.9x. Agent overhead compounds with task complexity.

### 2. Monolithic Remains the Best Value

Despite having the largest CLAUDE.md (475 lines of content, much of it irrelevant), monolithic delivered quality tied with vanilla (4.1) at the lowest cost ($8.56). The single-context cache amortization advantage is even more pronounced at scale.

### 3. Vanilla Claude Surprised Again

With zero configuration, vanilla produced 2,147 lines of source code, 119 test functions, and all tests passing — at $10.42. The pre-written requirements doc may be doing the heavy lifting here; when the spec is clear, Claude doesn't need much guidance.

### 4. Context Window Finally Mattered

Peak context ranged from 32K (agents-ondemand-optimized) to 85K (vanilla). This is still under the 200K limit, but approaching the range where context management matters. The optimized agent approach kept its main context at 32K by delegating effectively.

### 5. Agents-OnDemand-Skills Was Extremely Expensive

At $35.18, the original on-demand approach cost **4.1x monolithic** for only marginally better quality (4.4 vs 4.1). It spawned 9 agents and used 175 messages. The cache creation cost alone (1,076,606 tokens × $18.75/M = $20.19) exceeds monolithic's entire cost.

### 6. The Optimized Agent Approach Cut Costs by 40%

Agents-ondemand-optimized ($20.96) vs agents-ondemand-skills ($35.18) — a 40% reduction. The three optimizations worked:
- 3 agents instead of 9: fewer cache creation events (609K vs 1,077K cache create tokens)
- Terse returns: 32K main context vs 61K
- Consolidated work: 90 messages vs 175

### 7. Skills-Only Cheated — It Spawned Agents Anyway

Despite the CLAUDE.md saying "no agents," skills-only spontaneously spawned 4 agents (including a `bitwarden-software-engineer` agent). This suggests that for complex tasks, Claude may override configuration preferences when it decides delegation would help. This undermines the "skills-only" control.

### 8. Quality Converged at High Complexity

All variations scored between 3.8-4.4 — a much narrower range than the GUI task (3.3-4.4). The pre-written requirements doc leveled the playing field. When the spec is detailed, the configuration strategy matters less for quality and more for cost.

### 9. Agent-OnDemand-Skills Had Test Failures

3 parentheses-related tests failed in the scientific calculator. No other variation had failures. This may be due to the high number of agent handoffs (9 agents) causing inconsistency — each agent implements its piece without full context of what others did.

### 10. eval() Appeared in the Optimized Variation

Despite all skills including "use specific exception types, never bare except" guidance, agents-ondemand-optimized used `eval()` for expression evaluation. All other variations used manual dispatch. This is a security concern — `eval()` is riskier even with input validation.

---

## Comparison with Previous Runs (GUI Task)

| Metric | GUI Task Range | Advanced Task Range | Scale Factor |
|--------|---------------|--------------------| ------------|
| Cost | $2.69 - $8.13 | $8.56 - $35.18 | 3-4x |
| Total tokens | 491K - 954K | 2.4M - 5.5M | 5-6x |
| Peak context | 22K - 42K | 32K - 85K | 1.5-2x |
| Source lines | 257 - 358 | 1,747 - 3,139 | 7-9x |
| Test functions | 28 - 57 | 80 - 150 | 2.5-3x |

The advanced task was 5-6x more expensive in tokens, but context only grew 1.5-2x. Most of the extra tokens were in cache reads (more turns, more messages), not in context growth. This confirms that for current task sizes, context window isn't the bottleneck — cache creation cost is.

---

## Recommendations for the Advanced Calculator Task

1. **Use monolithic** for cost-effective results ($8.56, quality 4.1). The pre-written requirements doc compensates for the lack of agent specialization.

2. **Use agents-ondemand-optimized** if you need higher quality and can tolerate 2.4x the cost ($20.96, quality 4.2). The optimization levers (fewer agents, terse returns) are essential.

3. **Avoid agents-ondemand-skills** — at $35.18 it's 4x monolithic's cost with only marginal quality improvement and 3 test failures.

4. **Pre-written requirements docs are a great equalizer.** They make vanilla Claude nearly as effective as configured variations, suggesting that clear specs matter more than Claude Code configuration.
