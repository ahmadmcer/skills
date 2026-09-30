#!/usr/bin/env python3
"""Improve a skill description based on eval results.

Takes eval results (from run_eval.py) and generates an improved description
by querying a model via standard API endpoints or a configured CLI runner.
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
from pathlib import Path

from scripts.utils import parse_skill_md


def _call_llm(
    prompt: str,
    model: str | None,
    api_key: str | None = None,
    api_base: str | None = None,
    runner_cmd: str | None = None,
    timeout: int = 300,
) -> str:
    """Call a model with the prompt and return the text response."""
    # 1. Configured CLI command runner
    if runner_cmd:
        env = {
            k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "OPENCODE_SUBPROCESS")
        }
        env["OPENCODE_SUBPROCESS"] = "1"

        if "{" in runner_cmd:
            cmd = runner_cmd.format(
                prompt=shlex.quote(prompt),
                model=shlex.quote(model or ""),
            )
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                env=env,
                timeout=timeout,
            )
        else:
            cmd = shlex.split(runner_cmd)
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                env=env,
                timeout=timeout,
            )

        if result.returncode != 0:
            raise RuntimeError(f"Runner command failed ({result.returncode}):\n{result.stderr}")
        return result.stdout

    # 2. Configured or discovered API endpoint
    effective_api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_API_KEY")
    effective_api_base = (
        api_base
        or os.environ.get("OPENAI_BASE_URL")
        or os.environ.get("LLM_API_BASE")
        or "https://api.openai.com/v1"
    )

    if effective_api_key:
        url = effective_api_base.rstrip("/")
        if not url.endswith("/chat/completions"):
            url = f"{url}/chat/completions"

        payload = {
            "model": model or "default",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {effective_api_key}",
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
                raise RuntimeError("API returned empty choices")
            return choices[0].get("message", {}).get("content", "")

    # 3. Check for available standard CLI tools as fallback
    for cli_name in ("opencode", "claude"):
        if (
            subprocess.run(
                ["where" if os.name == "nt" else "which", cli_name], capture_output=True
            ).returncode
            == 0
        ):
            env = {
                k: v
                for k, v in os.environ.items()
                if k not in ("CLAUDECODE", "OPENCODE_SUBPROCESS")
            }
            if cli_name == "claude":
                cmd = ["claude", "-p", "--output-format", "text"]
                if model:
                    cmd.extend(["--model", model])
                result = subprocess.run(
                    cmd,
                    input=prompt,
                    capture_output=True,
                    text=True,
                    env=env,
                    timeout=timeout,
                )
                if result.returncode == 0:
                    return result.stdout

    raise RuntimeError(
        "No model execution backend available. Please set OPENAI_API_KEY / LLM_API_KEY "
        "or provide --runner-cmd (e.g. --runner-cmd 'opencode run {prompt}')."
    )


def improve_description(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: dict,
    history: list[dict],
    model: str | None,
    test_results: dict | None = None,
    log_dir: Path | None = None,
    iteration: int | None = None,
    api_key: str | None = None,
    api_base: str | None = None,
    runner_cmd: str | None = None,
) -> str:
    """Call the model to improve the description based on eval results."""
    failed_triggers = [r for r in eval_results["results"] if r["should_trigger"] and not r["pass"]]
    false_triggers = [
        r for r in eval_results["results"] if not r["should_trigger"] and not r["pass"]
    ]

    # Build scores summary
    train_score = f"{eval_results['summary']['passed']}/{eval_results['summary']['total']}"
    if test_results:
        test_score = f"{test_results['summary']['passed']}/{test_results['summary']['total']}"
        scores_summary = f"Train: {train_score}, Test: {test_score}"
    else:
        scores_summary = f"Train: {train_score}"

    prompt = f"""You are optimizing a skill description for an agent skill called "{skill_name}". A skill is an instructional bundle with progressive disclosure -- there is a name and description that the agent inspects when deciding whether to activate the skill, and upon activation, the agent reads the skill instructions and accesses supporting resources.

The description appears in the agent's catalog of available skills. When a user sends a query, the agent decides whether to invoke the skill based solely on the title and on this description. Your goal is to write a description that triggers for relevant queries, and doesn't trigger for irrelevant ones.

Here's the current description:
<current_description>
"{current_description}"
</current_description>

Current scores ({scores_summary}):
<scores_summary>
"""
    if failed_triggers:
        prompt += "FAILED TO TRIGGER (should have triggered but didn't):\n"
        for r in failed_triggers:
            prompt += f'  - "{r["query"]}" (triggered {r["triggers"]}/{r["runs"]} times)\n'
        prompt += "\n"

    if false_triggers:
        prompt += "FALSE TRIGGERS (triggered but shouldn't have):\n"
        for r in false_triggers:
            prompt += f'  - "{r["query"]}" (triggered {r["triggers"]}/{r["runs"]} times)\n'
        prompt += "\n"

    if history:
        prompt += (
            "PREVIOUS ATTEMPTS (do NOT repeat these — try something structurally different):\n\n"
        )
        for h in history:
            train_s = f"{h.get('train_passed', h.get('passed', 0))}/{h.get('train_total', h.get('total', 0))}"
            test_s = (
                f"{h.get('test_passed', '?')}/{h.get('test_total', '?')}"
                if h.get("test_passed") is not None
                else None
            )
            score_str = f"train={train_s}" + (f", test={test_s}" if test_s else "")
            prompt += f"<attempt {score_str}>\n"
            prompt += f'Description: "{h["description"]}"\n'
            if "results" in h:
                prompt += "Train results:\n"
                for r in h["results"]:
                    status = "PASS" if r["pass"] else "FAIL"
                    prompt += f'  [{status}] "{r["query"][:80]}" (triggered {r["triggers"]}/{r["runs"]})\n'
            if h.get("note"):
                prompt += f"Note: {h['note']}\n"
            prompt += "</attempt>\n\n"

    prompt += f"""</scores_summary>

Skill content (for context on what the skill does):
<skill_content>
{skill_content}
</skill_content>

Based on the failures, write a new and improved description that is more likely to trigger correctly. When I say "based on the failures", it's a bit of a tricky line to walk because we don't want to overfit to the specific cases you're seeing. So what I DON'T want you to do is produce an ever-expanding list of specific queries that this skill should or shouldn't trigger for. Instead, try to generalize from the failures to broader categories of user intent and situations where this skill would be useful or not useful. The reason for this is twofold:

1. Avoid overfitting
2. The list might get loooong and it's injected into queries where there might be many skills, so we don't want to blow too much space on any given description.

Concretely, your description should not be more than about 100-200 words, even if that comes at the cost of accuracy. There is a hard limit of 1024 characters — descriptions over that will be truncated, so stay comfortably under it.

Here are some tips that we've found to work well in writing these descriptions:
- The skill should be phrased in the imperative -- "Use this skill for" rather than "this skill does"
- The skill description should focus on the user's intent, what they are trying to achieve, vs. the implementation details of how the skill works.
- The description competes with other skills for the agent's attention — make it distinctive and immediately recognizable.
- If you're getting lots of failures after repeated attempts, change things up. Try different sentence structures or wordings.

I'd encourage you to be creative and mix up the style in different iterations since you'll have multiple opportunities to try different approaches and we'll just grab the highest-scoring one at the end. 

Please respond with only the new description text in <new_description> tags, nothing else."""

    text = _call_llm(prompt, model, api_key=api_key, api_base=api_base, runner_cmd=runner_cmd)

    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = match.group(1).strip().strip('"') if match else text.strip().strip('"')

    transcript: dict = {
        "iteration": iteration,
        "prompt": prompt,
        "response": text,
        "parsed_description": description,
        "char_count": len(description),
        "over_limit": len(description) > 1024,
    }

    if len(description) > 1024:
        shorten_prompt = (
            f"{prompt}\n\n"
            f"---\n\n"
            f"A previous attempt produced this description, which at "
            f"{len(description)} characters is over the 1024-character hard limit:\n\n"
            f'"{description}"\n\n'
            f"Rewrite it to be under 1024 characters while keeping the most "
            f"important trigger words and intent coverage. Respond with only "
            f"the new description in <new_description> tags."
        )
        shorten_text = _call_llm(
            shorten_prompt,
            model,
            api_key=api_key,
            api_base=api_base,
            runner_cmd=runner_cmd,
        )
        match = re.search(r"<new_description>(.*?)</new_description>", shorten_text, re.DOTALL)
        shortened = match.group(1).strip().strip('"') if match else shorten_text.strip().strip('"')

        transcript["rewrite_prompt"] = shorten_prompt
        transcript["rewrite_response"] = shorten_text
        transcript["rewrite_description"] = shortened
        transcript["rewrite_char_count"] = len(shortened)
        description = shortened

    transcript["final_description"] = description

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"improve_iter_{iteration or 'unknown'}.json"
        log_file.write_text(json.dumps(transcript, indent=2), encoding="utf-8")

    return description


def main():
    parser = argparse.ArgumentParser(
        description="Improve a skill description based on eval results"
    )
    parser.add_argument(
        "--eval-results",
        required=True,
        help="Path to eval results JSON (from run_eval.py)",
    )
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--history", default=None, help="Path to history JSON (previous attempts)")
    parser.add_argument("--model", default=None, help="Model identifier for improvement")
    parser.add_argument("--api-key", default=None, help="API key for model evaluation")
    parser.add_argument("--api-base", default=None, help="Base URL for model API endpoint")
    parser.add_argument(
        "--runner-cmd", default=None, help="CLI command template to invoke for prompts"
    )
    parser.add_argument("--verbose", action="store_true", help="Print thinking to stderr")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    eval_results = json.loads(Path(args.eval_results).read_text(encoding="utf-8"))
    history = []
    if args.history:
        history = json.loads(Path(args.history).read_text(encoding="utf-8"))

    name, _, content = parse_skill_md(skill_path)
    current_description = eval_results["description"]

    if args.verbose:
        print(f"Current: {current_description}", file=sys.stderr)
        print(
            f"Score: {eval_results['summary']['passed']}/{eval_results['summary']['total']}",
            file=sys.stderr,
        )

    new_description = improve_description(
        skill_name=name,
        skill_content=content,
        current_description=current_description,
        eval_results=eval_results,
        history=history,
        model=args.model,
        api_key=args.api_key,
        api_base=args.api_base,
        runner_cmd=args.runner_cmd,
    )

    if args.verbose:
        print(f"Improved: {new_description}", file=sys.stderr)

    # Output as JSON with both the new description and updated history
    output = {
        "description": new_description,
        "history": history
        + [
            {
                "description": current_description,
                "passed": eval_results["summary"]["passed"],
                "failed": eval_results["summary"]["failed"],
                "total": eval_results["summary"]["total"],
                "results": eval_results["results"],
            }
        ],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
