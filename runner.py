#!/usr/bin/env python3
"""Claude Code Token Efficiency Testing Framework.

Compare different Claude Code configuration strategies (monolithic CLAUDE.md,
skills + agents, skills only, etc.) to find the most token-efficient approach.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("Error: 'rich' is required. Install with: pip install rich")
    sys.exit(1)

console = Console()

# Paths
REPO_ROOT = Path(__file__).parent.resolve()
VARIATIONS_DIR = REPO_ROOT / "variations"
TASKS_DIR = REPO_ROOT / "tasks"
RESULTS_DIR = REPO_ROOT / "results"
CLAUDE_HOME = Path.home() / ".claude"

# Model pricing (per 1M tokens) — Opus 4.6
PRICING = {
    "input": 15.00,
    "output": 75.00,
    "cache_creation": 18.75,
    "cache_read": 1.50,
}


# Preferred display order for variations. Names not listed sort to the end alphabetically.
VARIATION_ORDER = [
    "vanilla-claude",
    "monolithic",
    "skills-only",
    "skills-and-agents",
    "agents-ondemand-skills",
    "agents-ondemand-optimized",
]


def discover_variations() -> list[dict]:
    """Find all variation directories with a .claude/ folder."""
    variations = []
    if not VARIATIONS_DIR.exists():
        return variations
    for d in VARIATIONS_DIR.iterdir():
        if d.is_dir() and (d / ".claude").exists():
            # Check for a description.txt override, otherwise derive from directory name
            desc_file = d / "description.txt"
            if desc_file.exists():
                description = desc_file.read_text().strip()
            else:
                description = d.name
            variations.append({
                "name": d.name,
                "path": d,
                "description": description,
            })

    def sort_key(v):
        try:
            return VARIATION_ORDER.index(v["name"])
        except ValueError:
            return len(VARIATION_ORDER)

    variations.sort(key=sort_key)
    return variations


# Preferred display order for tasks. Names not listed sort to the end alphabetically.
TASK_ORDER = [
    "python-calculator",
    "python-calculator-docs",
    "python-calculator-gui",
]


def discover_tasks() -> list[dict]:
    """Find all task definition files."""
    tasks = []
    if not TASKS_DIR.exists():
        return tasks
    for f in TASKS_DIR.glob("*.md"):
        # Check for a description.txt override, otherwise use first line
        desc_file = f.with_suffix(".desc")
        if desc_file.exists():
            description = desc_file.read_text().strip()
        else:
            description = f.stem
        tasks.append({
            "name": f.stem,
            "path": f,
            "description": description,
        })

    def sort_key(t):
        try:
            return TASK_ORDER.index(t["name"])
        except ValueError:
            return len(TASK_ORDER)

    tasks.sort(key=sort_key)
    return tasks


def create_test_directory(variation_path: Path) -> Path:
    """Create an ephemeral temp directory with the variation's .claude/ folder and a git repo."""
    tmp_dir = Path(tempfile.mkdtemp(prefix="claude-test-")).resolve()
    shutil.copytree(variation_path / ".claude", tmp_dir / ".claude")
    # Initialize a git repo (required for Claude Code)
    subprocess.run(
        ["git", "init"],
        cwd=tmp_dir,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "initial"],
        cwd=tmp_dir,
        capture_output=True,
        check=True,
    )
    return tmp_dir


def get_prompt_text(task_path: Path, prompt_override: str | None = None) -> str:
    """Get the prompt text, using override if provided, otherwise from task file."""
    if prompt_override:
        return prompt_override.strip()
    return task_path.read_text().strip()


def build_claude_command(
    test_dir: Path, prompt_text: str, session_id: str
) -> str:
    """Build the claude CLI command string."""
    # Escape single quotes in prompt text for shell
    escaped_prompt = prompt_text.replace("'", "'\\''")
    return (
        f"cd {test_dir} && claude -p "
        f"--session-id {session_id} "
        f"--permission-mode bypassPermissions "
        f"--output-format stream-json --verbose "
        f"'{escaped_prompt}'"
    )


def find_session_log(session_id: str) -> Path | None:
    """Find the session JSONL file by session ID."""
    projects_dir = CLAUDE_HOME / "projects"
    if not projects_dir.exists():
        return None
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        candidate = project_dir / f"{session_id}.jsonl"
        if candidate.exists():
            return candidate
    return None


def _parse_single_jsonl(jsonl_path: Path) -> dict:
    """Parse a single JSONL file and return raw counters."""
    totals = {
        "input": 0, "output": 0, "cache_creation": 0, "cache_read": 0,
        "messages": 0, "tool_calls": 0,
    }
    peak_context = 0
    final_context = 0
    skills = []
    agents = []

    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg = entry.get("message", {})
            if msg.get("role") == "assistant":
                totals["messages"] += 1

                usage = msg.get("usage", {})
                if usage:
                    totals["input"] += usage.get("input_tokens", 0)
                    totals["output"] += usage.get("output_tokens", 0)
                    totals["cache_creation"] += usage.get("cache_creation_input_tokens", 0)
                    totals["cache_read"] += usage.get("cache_read_input_tokens", 0)

                    # Context consumed = full prompt size for this API call
                    msg_context = (
                        usage.get("input_tokens", 0)
                        + usage.get("cache_creation_input_tokens", 0)
                        + usage.get("cache_read_input_tokens", 0)
                    )
                    peak_context = max(peak_context, msg_context)
                    final_context = msg_context

                content = msg.get("content", [])
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "tool_use":
                            totals["tool_calls"] += 1
                            tool_name = block.get("name", "")
                            tool_input = block.get("input", {})

                            if tool_name == "Skill":
                                skill = tool_input.get("skill", "unknown")
                                if skill not in skills:
                                    skills.append(skill)

                            if tool_name == "Agent":
                                desc = tool_input.get("description", "unknown")
                                agent_type = tool_input.get("subagent_type", "general-purpose")
                                agent_entry = f"{agent_type}: {desc}"
                                if agent_entry not in agents:
                                    agents.append(agent_entry)

    return {
        **totals,
        "peak_context": peak_context,
        "final_context": final_context,
        "skills": skills,
        "agents": agents,
    }


def parse_session_log(session_log: Path) -> dict:
    """Parse a session JSONL file and all sub-agent logs to extract metrics."""
    # Parse the main session log
    result = _parse_single_jsonl(session_log)
    all_skills = list(result["skills"])
    all_agents = list(result["agents"])
    peak_context_main = result["peak_context"]
    final_context_main = result["final_context"]
    peak_context_any = peak_context_main
    subagent_peak_contexts = []

    # Parse sub-agent logs (stored alongside the session file)
    session_id = session_log.stem
    subagents_dir = session_log.parent / session_id / "subagents"
    if subagents_dir.exists():
        for sub_log in subagents_dir.glob("*.jsonl"):
            sub = _parse_single_jsonl(sub_log)
            result["input"] += sub["input"]
            result["output"] += sub["output"]
            result["cache_creation"] += sub["cache_creation"]
            result["cache_read"] += sub["cache_read"]
            result["messages"] += sub["messages"]
            result["tool_calls"] += sub["tool_calls"]
            peak_context_any = max(peak_context_any, sub["peak_context"])
            subagent_peak_contexts.append(sub["peak_context"])
            for s in sub["skills"]:
                if s not in all_skills:
                    all_skills.append(s)
            for a in sub["agents"]:
                if a not in all_agents:
                    all_agents.append(a)

    total_input = result["input"]
    total_output = result["output"]
    total_cache_creation = result["cache_creation"]
    total_cache_read = result["cache_read"]

    cost = (
        (total_input / 1_000_000) * PRICING["input"]
        + (total_output / 1_000_000) * PRICING["output"]
        + (total_cache_creation / 1_000_000) * PRICING["cache_creation"]
        + (total_cache_read / 1_000_000) * PRICING["cache_read"]
    )

    return {
        "input_tokens": total_input,
        "output_tokens": total_output,
        "cache_creation_tokens": total_cache_creation,
        "cache_read_tokens": total_cache_read,
        "total_tokens": total_input + total_output + total_cache_creation + total_cache_read,
        "estimated_cost_usd": round(cost, 4),
        "message_count": result["messages"],
        "tool_call_count": result["tool_calls"],
        "peak_context_main": peak_context_main,
        "final_context_main": final_context_main,
        "peak_context_any": peak_context_any,
        "skills_used": all_skills,
        "agents_used": all_agents,
    }


def copy_output_artifacts(test_dir: Path, output_dir: Path) -> None:
    """Copy all non-.claude files from the test directory to the output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in test_dir.rglob("*"):
        if item.is_file() and ".claude" not in item.parts and ".git" not in item.parts:
            rel = item.relative_to(test_dir)
            dest = output_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)


def save_result(
    variation_name: str, task_name: str, prompt_text: str, metrics: dict,
    test_dir: Path | None = None,
) -> Path:
    """Save test result as JSON and copy output artifacts."""
    RESULTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_name = f"{variation_name}_{task_name}_{timestamp}"
    result = {
        "variation": variation_name,
        "task": task_name,
        "prompt": prompt_text,
        "timestamp": timestamp,
        "metrics": metrics,
    }
    result_path = RESULTS_DIR / f"{run_name}.json"
    result_path.write_text(json.dumps(result, indent=2))

    # Copy output artifacts if test directory is available
    if test_dir and test_dir.exists():
        output_dir = RESULTS_DIR / run_name / "output"
        copy_output_artifacts(test_dir, output_dir)

    return result_path


def load_results() -> list[dict]:
    """Load all saved results."""
    results = []
    if not RESULTS_DIR.exists():
        return results
    for f in sorted(RESULTS_DIR.glob("*.json")):
        try:
            results.append(json.loads(f.read_text()))
        except json.JSONDecodeError:
            continue
    return results


# --- CLI Commands ---


def cmd_list():
    """List available variations and tasks."""
    variations = discover_variations()
    tasks = discover_tasks()

    table = Table(title="Available Variations")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    for v in variations:
        table.add_row(v["name"], v["description"])
    console.print(table)
    console.print()

    table = Table(title="Available Tasks")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    for t in tasks:
        table.add_row(t["name"], t["description"])
    console.print(table)


def cmd_run(prompt_override: str | None = None):
    """Interactive test run flow."""
    variations = discover_variations()
    tasks = discover_tasks()

    if not variations:
        console.print("[red]No variations found in variations/ directory[/red]")
        return
    if not tasks:
        console.print("[red]No tasks found in tasks/ directory[/red]")
        return

    # Pick variation
    console.print("\n[bold]Select a variation:[/bold]")
    for i, v in enumerate(variations, 1):
        console.print(f"  {i}. [cyan]{v['name']}[/cyan] — {v['description']}")
    choice = IntPrompt.ask("Choice", default=1)
    if choice < 1 or choice > len(variations):
        console.print("[red]Invalid choice[/red]")
        return
    variation = variations[choice - 1]

    # Pick task
    console.print("\n[bold]Select a task:[/bold]")
    for i, t in enumerate(tasks, 1):
        console.print(f"  {i}. [cyan]{t['name']}[/cyan] — {t['description']}")
    choice = IntPrompt.ask("Choice", default=1)
    if choice < 1 or choice > len(tasks):
        console.print("[red]Invalid choice[/red]")
        return
    task = tasks[choice - 1]

    # Resolve prompt text
    prompt_text = get_prompt_text(task["path"], prompt_override)
    if prompt_override:
        console.print(f"\n[yellow]Using custom prompt override[/yellow]")
    console.print(Panel(prompt_text, title="Prompt", border_style="blue"))

    # Create test environment
    session_id = str(uuid.uuid4())
    console.print(f"\n[bold]Setting up test environment...[/bold]")
    test_dir = create_test_directory(variation["path"])
    console.print(f"  Test directory: [green]{test_dir}[/green]")
    console.print(f"  Session ID: [green]{session_id}[/green]")

    # Build command and copy to clipboard
    command = build_claude_command(test_dir, prompt_text, session_id)
    console.print()
    try:
        subprocess.run(["pbcopy"], input=command.encode(), check=True)
        console.print(f"[green]Command copied to clipboard![/green] ({variation['name']} + {task['name']})")
    except (FileNotFoundError, subprocess.CalledProcessError):
        console.print(f"[yellow]Command ({variation['name']} + {task['name']}):[/yellow]")
        console.print(command)
    console.print()
    console.print("[yellow]Paste and run the command in another terminal.[/yellow]")
    console.print("[yellow]Press Enter here when the run is complete...[/yellow]")
    input()

    # Parse results
    console.print("[bold]Collecting metrics...[/bold]")
    session_log = find_session_log(session_id)
    if session_log is None:
        console.print("[red]Could not find session log. Checking all project dirs...[/red]")
        console.print(f"[dim]Looking for session {session_id} in ~/.claude/projects/[/dim]")
        console.print("[red]Session log not found. The run may not have completed.[/red]")
        # Clean up
        shutil.rmtree(test_dir, ignore_errors=True)
        return

    metrics = parse_session_log(session_log)
    result_path = save_result(
        variation["name"], task["name"], prompt_text, metrics, test_dir=test_dir
    )

    # Display results
    console.print()
    _print_metrics(variation["name"], task["name"], metrics)
    console.print(f"\n[green]Results saved to: {result_path}[/green]")

    # Clean up temp directory
    shutil.rmtree(test_dir, ignore_errors=True)
    console.print(f"[dim]Cleaned up test directory: {test_dir}[/dim]")


def _print_metrics(variation: str, task: str, metrics: dict):
    """Print a formatted metrics summary."""
    table = Table(title=f"Results: {variation} + {task}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white", justify="right")

    table.add_row("Input tokens", f"{metrics['input_tokens']:,}")
    table.add_row("Output tokens", f"{metrics['output_tokens']:,}")
    table.add_row("Cache creation tokens", f"{metrics['cache_creation_tokens']:,}")
    table.add_row("Cache read tokens", f"{metrics['cache_read_tokens']:,}")
    table.add_row("Total tokens", f"[bold]{metrics['total_tokens']:,}[/bold]")
    table.add_row("Estimated cost", f"[bold]${metrics['estimated_cost_usd']:.4f}[/bold]")
    table.add_row("Messages", str(metrics["message_count"]))
    table.add_row("Tool calls", str(metrics["tool_call_count"]))
    table.add_row("Peak context (main)", f"{metrics['peak_context_main']:,}")
    table.add_row("Final context (main)", f"{metrics['final_context_main']:,}")
    table.add_row("Peak context (any)", f"{metrics['peak_context_any']:,}")
    table.add_row("Skills used", ", ".join(metrics["skills_used"]) or "none")
    table.add_row("Agents used", ", ".join(metrics["agents_used"]) or "none")

    console.print(table)


def cmd_compare():
    """Show comparison table of all saved results."""
    results = load_results()
    if not results:
        console.print("[yellow]No results found. Run some tests first![/yellow]")
        return

    table = Table(title="Comparison of All Runs")
    table.add_column("Variation", style="cyan")
    table.add_column("Task", style="white")
    table.add_column("Timestamp", style="dim")
    table.add_column("Total Tokens", justify="right")
    table.add_column("Input", justify="right")
    table.add_column("Output", justify="right")
    table.add_column("Cache Create", justify="right")
    table.add_column("Cache Read", justify="right")
    table.add_column("Cost", justify="right", style="green")
    table.add_column("Messages", justify="right")
    table.add_column("Tool Calls", justify="right")
    table.add_column("Peak Ctx", justify="right", style="red")
    table.add_column("Final Ctx", justify="right")
    table.add_column("Skills", style="yellow")
    table.add_column("Agents", style="magenta")

    for r in results:
        m = r["metrics"]
        table.add_row(
            r["variation"],
            r["task"],
            r["timestamp"],
            f"{m['total_tokens']:,}",
            f"{m['input_tokens']:,}",
            f"{m['output_tokens']:,}",
            f"{m['cache_creation_tokens']:,}",
            f"{m['cache_read_tokens']:,}",
            f"${m['estimated_cost_usd']:.4f}",
            str(m["message_count"]),
            str(m["tool_call_count"]),
            f"{m.get('peak_context_any', 0):,}",
            f"{m.get('final_context_main', 0):,}",
            ", ".join(m.get("skills_used", [])) or "-",
            ", ".join(m.get("agents_used", [])) or "-",
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Token Efficiency Testing Framework"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("list", help="List available variations and tasks")
    run_parser = subparsers.add_parser("run", help="Run an interactive test")
    run_parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Override the task's default prompt with a custom one",
    )
    subparsers.add_parser("compare", help="Compare results from previous runs")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "run":
        cmd_run(prompt_override=args.prompt)
    elif args.command == "compare":
        cmd_compare()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
