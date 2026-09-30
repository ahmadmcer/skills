#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes an agent or model to trigger
(activate the skill) for a set of queries. Outputs results as JSON.
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for standard project markers."""
    current = Path.cwd()
    markers = [".git", ".opencode", "pyproject.toml", "package.json", ".claude"]
    for parent in [current, *current.parents]:
        if any((parent / marker).exists() for marker in markers):
            return parent
    return current


def _parse_trigger_response(text: str, skill_name: str) -> bool:
    """Extract a boolean trigger decision from model output or JSON."""
    clean = text.strip()
    if not clean:
        return False

    # Check for direct markdown code block with JSON
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", clean, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            if "trigger" in data:
                return bool(data["trigger"])
        except json.JSONDecodeError:
            pass

    # Try raw JSON decode
    try:
        data = json.loads(clean)
        if isinstance(data, dict):
            if "trigger" in data:
                return bool(data["trigger"])
            if "tool_calls" in data:
                for tc in data.get("tool_calls", []):
                    fn = tc.get("function", {})
                    if fn.get("name") == skill_name:
                        return True
    except json.JSONDecodeError:
        pass

    # Regex search for trigger field in JSON text
    match = re.search(r'"trigger"\s*:\s*(true|false)', clean, re.IGNORECASE)
    if match:
        return match.group(1).lower() == "true"

    # Tool call or skill invocation text indicator
    if (
        f'"{skill_name}"' in clean
        or f"'{skill_name}'" in clean
        or f"`{skill_name}`" in clean
    ):
        if (
            "invoke" in clean.lower()
            or "trigger" in clean.lower()
            or "activate" in clean.lower()
        ):
            return True

    return False


def _query_api(
    query: str,
    skill_name: str,
    skill_description: str,
    model: str,
    api_key: str,
    api_base: str,
    timeout: int,
) -> bool:
    """Evaluate triggering using a standard chat completions endpoint."""
    url = api_base.rstrip("/")
    if not url.endswith("/chat/completions"):
        url = f"{url}/chat/completions"

    system_prompt = (
        "You are an AI assistant evaluating whether to invoke a specialized skill for a user's task.\n\n"
        f"Available Skill: {skill_name}\n"
        f"Description: {skill_description}\n\n"
        "Criteria:\n"
        f'- Return {{"trigger": true}} if the user\'s intent clearly matches this skill and warrants activating it.\n'
        f'- Return {{"trigger": false}} if the request should be handled directly without activating this skill or falls outside its scope.\n'
        'Respond ONLY with a JSON object: {"trigger": true} or {"trigger": false}.'
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        "temperature": 0.0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        choices = res_data.get("choices", [])
        if not choices:
            return False
        message = choices[0].get("message", {})
        content = message.get("content", "")
        return _parse_trigger_response(content, skill_name)


def _query_command(
    query: str,
    skill_name: str,
    skill_description: str,
    runner_cmd: str,
    timeout: int,
    project_root: str,
) -> bool:
    """Evaluate triggering by invoking a configured CLI command."""
    formatted_cmd = (
        runner_cmd.format(
            query=shlex.quote(query),
            prompt=shlex.quote(query),
            skill_name=shlex.quote(skill_name),
            description=shlex.quote(skill_description),
        )
        if "{" in runner_cmd
        else f"{runner_cmd} {shlex.quote(query)}"
    )

    # Avoid environment recursion conflicts
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("CLAUDECODE", "OPENCODE_SUBPROCESS")
    }
    env["OPENCODE_SUBPROCESS"] = "1"

    result = subprocess.run(
        formatted_cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=project_root,
        env=env,
    )
    output = result.stdout + "\n" + result.stderr
    return _parse_trigger_response(output, skill_name)


def _query_heuristic(query: str, skill_name: str, skill_description: str) -> bool:
    """Heuristic evaluation for offline or local testing when no runner is active."""
    q_lower = query.lower()
    desc_lower = skill_description.lower()
    name_lower = skill_name.lower().replace("-", " ")

    # Direct name match
    if name_lower in q_lower or skill_name.lower() in q_lower:
        return True

    # Check for negative trigger phrases in description
    exclusions = []
    excl_match = re.search(
        r"(?:do not use|not for|skip for|avoid for)\s+([^.]+)", desc_lower
    )
    if excl_match:
        exclusions = [
            w.strip() for w in excl_match.group(1).split(",") if len(w.strip()) > 3
        ]

    for excl in exclusions:
        if excl in q_lower:
            return False

    # Extract distinctive words from description
    desc_words = {
        w
        for w in re.findall(r"\b[a-z]{4,}\b", desc_lower)
        if w
        not in {
            "this",
            "skill",
            "when",
            "user",
            "with",
            "from",
            "that",
            "have",
            "make",
            "sure",
            "should",
            "could",
            "would",
            "tasks",
            "their",
            "about",
        }
    }

    matches = sum(1 for w in desc_words if w in q_lower)
    return matches >= 2


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    api_key: str | None = None,
    api_base: str | None = None,
    runner_cmd: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered."""
    # 1. Configured CLI command runner
    if runner_cmd:
        try:
            return _query_command(
                query=query,
                skill_name=skill_name,
                skill_description=skill_description,
                runner_cmd=runner_cmd,
                timeout=timeout,
                project_root=project_root,
            )
        except Exception as e:
            print(f"Warning: CLI runner failed: {e}", file=sys.stderr)
            return False

    # 2. Configured or discovered API endpoint
    effective_api_key = (
        api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_API_KEY")
    )
    effective_api_base = (
        api_base
        or os.environ.get("OPENAI_BASE_URL")
        or os.environ.get("LLM_API_BASE")
        or "https://api.openai.com/v1"
    )

    if effective_api_key and model:
        try:
            return _query_api(
                query=query,
                skill_name=skill_name,
                skill_description=skill_description,
                model=model,
                api_key=effective_api_key,
                api_base=effective_api_base,
                timeout=timeout,
            )
        except Exception as e:
            print(
                f"Warning: API query failed ({e}); checking fallback", file=sys.stderr
            )

    # 3. Fallback to heuristic matcher
    return _query_heuristic(query, skill_name, skill_description)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
    api_key: str | None = None,
    api_base: str | None = None,
    runner_cmd: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model=model,
                    api_key=api_key,
                    api_base=api_base,
                    runner_cmd=runner_cmd,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": sum(triggers),
                "runs": len(triggers),
                "pass": did_pass,
            }
        )

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run trigger evaluation for a skill description"
    )
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument(
        "--description", default=None, help="Override description to test"
    )
    parser.add_argument(
        "--num-workers", type=int, default=10, help="Number of parallel workers"
    )
    parser.add_argument(
        "--timeout", type=int, default=30, help="Timeout per query in seconds"
    )
    parser.add_argument(
        "--runs-per-query", type=int, default=3, help="Number of runs per query"
    )
    parser.add_argument(
        "--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold"
    )
    parser.add_argument(
        "--model", default=None, help="Model identifier to use for evaluation"
    )
    parser.add_argument("--api-key", default=None, help="API key for model evaluation")
    parser.add_argument(
        "--api-base", default=None, help="Base URL for model API endpoint"
    )
    parser.add_argument(
        "--runner-cmd",
        default=None,
        help="CLI command template to invoke for each query",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print progress to stderr"
    )
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
        api_key=args.api_key,
        api_base=args.api_base,
        runner_cmd=args.runner_cmd,
    )

    if args.verbose:
        summary = output["summary"]
        print(
            f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr
        )
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(
                f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}",
                file=sys.stderr,
            )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
