# Project Guidelines

This is a Python software project. Delegate specialized work to the appropriate agents:

- **doc-writer**: For all documentation — requirements, architecture, coding plans, test plans.
- **implementer**: For all code implementation — application code, logic modules, GUI.
- **tester**: For writing and running tests.

## Orchestration Rules

- **Do NOT read back files** created by agents. Trust that the agent completed its work.
- **Pass file paths, not contents**, when coordinating between agents. For example, tell the implementer "implement based on the architecture in docs/architecture.md" rather than pasting the architecture content.
- **Return only summaries.** When an agent finishes, it should report what files it created and a one-line summary, not the full content.
- **Minimize agent spawns.** Combine related work into a single agent call when possible (e.g., all docs in one agent, all implementation in one agent).
