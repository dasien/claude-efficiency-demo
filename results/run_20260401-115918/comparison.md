# Comparison — run_20260401-115918

## Cost & Efficiency

| Variation | Task | Cost | Total Tokens | Cache Create | Cache Read | Output | Messages | Tools |
|-----------|------|------|-------------|-------------|------------|--------|----------|-------|
| agents-ondemand-optimized | python-calculator-gui | $6.6526 | 700,586 | 218,186 | 457,329 | 24,992 | 43 | 26 |
| agents-ondemand-skills | python-calculator-gui | $7.3869 | 953,696 | 226,068 | 699,557 | 27,962 | 59 | 30 |
| monolithic | python-calculator-gui | $3.9385 | 722,597 | 101,199 | 606,287 | 15,082 | 23 | 12 |
| skills-and-agents | python-calculator-gui | $8.1294 | 941,728 | 232,593 | 672,271 | 36,782 | 50 | 24 |
| skills-only | python-calculator-gui | $4.9100 | 887,113 | 138,819 | 732,140 | 16,110 | 31 | 18 |
| vanilla-claude | python-calculator-gui | $2.6876 | 491,151 | 60,141 | 418,563 | 12,423 | 20 | 11 |

## Context Usage

| Variation | Peak Context (main) | Final Context (main) | Peak Context (any) |
|-----------|--------------------:|---------------------:|-------------------:|
| agents-ondemand-optimized | 21,943 | 21,943 | 23,310 |
| agents-ondemand-skills | 0 | 0 | 0 |
| monolithic | 0 | 0 | 0 |
| skills-and-agents | 0 | 0 | 0 |
| skills-only | 0 | 0 | 0 |
| vanilla-claude | 32,042 | 32,042 | 32,042 |

## Skills & Agents Used

| Variation | Skills | Agents |
|-----------|--------|--------|
| agents-ondemand-optimized | python-coding, gui-tkinter, requirements, architecture, testing | doc-writer: Write all project documentation; implementer: Implement calculator application; tester: Write and run calculator tests |
| agents-ondemand-skills | architecture, gui-tkinter, python-coding, requirements, testing | architect: Write requirements document; architect: Write architecture document; architect: Write coding plan document; architect: Write test plan document; python-expert: Implement calculator logic module; python-expert: Implement calculator GUI module; tester: Write and run calculator tests |
| monolithic | - | - |
| skills-and-agents | - | architect: Write requirements document; architect: Write architecture document; architect: Write coding plan document; architect: Write test plan document; python-expert: Implement calculator logic; python-expert: Implement calculator GUI; tester: Implement calculator tests |
| skills-only | requirements, architecture, testing, python-coding | - |
| vanilla-claude | - | - |
