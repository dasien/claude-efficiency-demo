# Comparison — run_20260401-201253

## Cost & Efficiency

| Variation | Task | Cost | Total Tokens | Cache Create | Cache Read | Output | Messages | Tools |
|-----------|------|------|-------------|-------------|------------|--------|----------|-------|
| agents-ondemand-optimized | advanced-calculator | $20.9628 | 3,658,772 | 609,145 | 2,981,948 | 67,553 | 90 | 57 |
| agents-ondemand-skills | advanced-calculator | $35.1824 | 5,502,653 | 1,076,606 | 4,307,096 | 112,519 | 175 | 107 |
| monolithic | advanced-calculator | $8.5553 | 2,407,319 | 130,857 | 2,239,860 | 36,549 | 45 | 35 |
| skills-and-agents | advanced-calculator | $23.5021 | 3,832,074 | 708,628 | 3,043,366 | 74,151 | 142 | 89 |
| skills-only | advanced-calculator | $11.8448 | 3,230,821 | 195,382 | 2,985,981 | 49,342 | 86 | 57 |
| vanilla-claude | advanced-calculator | $10.4214 | 2,904,030 | 151,692 | 2,705,367 | 46,910 | 53 | 39 |

## Context Usage

| Variation | Peak Context (main) | Final Context (main) | Peak Context (any) |
|-----------|--------------------:|---------------------:|-------------------:|
| agents-ondemand-optimized | 32,388 | 32,388 | 70,578 |
| agents-ondemand-skills | 60,607 | 60,607 | 72,386 |
| monolithic | 82,608 | 82,608 | 82,608 |
| skills-and-agents | 75,026 | 75,026 | 75,026 |
| skills-only | 75,584 | 75,584 | 75,584 |
| vanilla-claude | 85,489 | 85,489 | 85,489 |

## Skills & Agents Used

| Variation | Skills | Agents |
|-----------|--------|--------|
| agents-ondemand-optimized | python-coding, gui-tkinter, architecture, testing | doc-writer: Write architecture, coding plan, test plan; implementer: Implement full calculator application; tester: Write and run all calculator tests |
| agents-ondemand-skills | python-coding, architecture, testing | architect: Write architecture.md; architect: Write coding-plan.md; architect: Write test-plan.md; python-expert: Implement basic_logic.py; python-expert: Implement scientific_logic.py; python-expert: Implement programmer_logic.py; python-expert: Implement GUI views; tester: Implement all test files; python-expert: Implement app.py and main.py |
| monolithic | - | - |
| skills-and-agents | - | architect: Design architecture document; architect: Write coding plan document; architect: Write test plan document; python-expert: Implement logic layer modules; python-expert: Implement GUI layer modules; python-expert: Implement app controller and entry; tester: Write basic and memory tests; tester: Write scientific calculator tests; tester: Write programmer and mode switch tests |
| skills-only | - | bitwarden-software-engineer: Write test_basic.py; general-purpose: Write test_basic.py; general-purpose: Write test_scientific.py; general-purpose: Write test_programmer.py |
| vanilla-claude | - | - |
