#!/usr/bin/env python3
"""generate_component_spec.py - Generates complete 8-state component specifications.

Produces production-grade design specifications and state machine matrices
(Default, Hover, Active, Focus, Disabled, Loading, Empty, Error) with
Tailwind CSS tokens, keyboard mappings, and WCAG 2.2 accessibility attributes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


COMPONENT_TEMPLATES = {
    "button": {
        "description": "Interactive trigger for initiating user actions and state changes.",
        "html_tag": "<button>",
        "role": "button",
        "keyboard": {
            "Enter": "Activates the button.",
            "Space": "Activates the button.",
            "Tab": "Moves focus to the button.",
        },
        "states": {
            "default": {
                "label": "Default (Idle)",
                "visual": "bg-blue-600 text-white shadow-sm font-medium rounded-md px-4 py-2.5 min-h-[44px]",
                "behavior": "Resting interactive state with crisp contrast (4.5:1+).",
                "aria": 'type="button"',
            },
            "hover": {
                "label": "Hover",
                "visual": "hover:bg-blue-700 hover:shadow transition-colors duration-150",
                "behavior": "Subtle 10% lightness reduction indicating mouse pointer proximity.",
                "aria": "",
            },
            "active": {
                "label": "Active (Pressed)",
                "visual": "active:bg-blue-800 active:scale-[0.98] transition-transform duration-75",
                "behavior": "Instant mechanical depression feedback upon pointer or key press.",
                "aria": "",
            },
            "focus_visible": {
                "label": "Focus-Visible",
                "visual": "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2",
                "behavior": "High-contrast 2px ring displayed exclusively on keyboard tab navigation.",
                "aria": ":focus-visible pseudo-class",
            },
            "disabled": {
                "label": "Disabled",
                "visual": "opacity-50 cursor-not-allowed bg-gray-300 text-gray-500 shadow-none",
                "behavior": "Non-interactive. Suppresses clicks. Explanatory tooltip provides context.",
                "aria": 'aria-disabled="true"',
            },
            "loading": {
                "label": "Loading",
                "visual": "cursor-wait bg-blue-600 text-transparent relative min-w-[120px]",
                "behavior": "Displays animated spinner. Locks dimensions to prevent layout twitching.",
                "aria": 'aria-busy="true" aria-live="polite"',
            },
            "empty": {
                "label": "Empty",
                "visual": "border-2 border-dashed border-gray-300 bg-transparent text-gray-500 hover:border-gray-400",
                "behavior": "First-run or zero-selection variant prompting initial user action (e.g. '+ Add Item').",
                "aria": "",
            },
            "error": {
                "label": "Error",
                "visual": "border-2 border-red-600 bg-red-50 text-red-700 focus-visible:ring-red-600",
                "behavior": "Action failed. Retains focus and links to error toast or alert banner.",
                "aria": 'aria-invalid="true"',
            },
        },
    },
    "input": {
        "description": "Text entry field for capturing single-line user input and queries.",
        "html_tag": "<input>",
        "role": "textbox",
        "keyboard": {
            "Tab": "Focuses the input field.",
            "Escape": "Clears current uncommitted input (if supported).",
        },
        "states": {
            "default": {
                "label": "Default (Idle)",
                "visual": "bg-white text-gray-900 border border-gray-300 rounded-md px-3 py-2 min-h-[44px]",
                "behavior": "Resting state with visible associated label above field.",
                "aria": 'id="user-input" name="field"',
            },
            "hover": {
                "label": "Hover",
                "visual": "hover:border-gray-400 transition-colors duration-150",
                "behavior": "Border darkens slightly on cursor approach.",
                "aria": "",
            },
            "active": {
                "label": "Active (Typing)",
                "visual": "border-blue-600 ring-1 ring-blue-600",
                "behavior": "Carat active, captures keyboard input events.",
                "aria": "",
            },
            "focus_visible": {
                "label": "Focus-Visible",
                "visual": "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2",
                "behavior": "Prominent 2px ring indicating active input destination.",
                "aria": "",
            },
            "disabled": {
                "label": "Disabled",
                "visual": "bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed",
                "behavior": "Read-only non-editable field. Value is preserved but locked.",
                "aria": 'disabled aria-disabled="true"',
            },
            "loading": {
                "label": "Loading (Validating)",
                "visual": "pr-10 bg-white border-blue-500",
                "behavior": "Displays inline micro-spinner icon on the right edge during async validation.",
                "aria": 'aria-busy="true"',
            },
            "empty": {
                "label": "Empty (Placeholder)",
                "visual": "placeholder:text-gray-400 italic text-gray-900",
                "behavior": "Displays subtle example format. Never uses placeholder as a replacement for label.",
                "aria": 'placeholder="e.g., alex@domain.com"',
            },
            "error": {
                "label": "Error",
                "visual": "border-red-600 text-red-900 focus-visible:ring-red-600 bg-red-50/50",
                "behavior": "Red border, displays inline error message below field with icon.",
                "aria": 'aria-invalid="true" aria-describedby="input-error-msg"',
            },
        },
    },
    "agent-card": {
        "description": "Agentic surface displaying AI agent status, reasoning traces, and action approvals.",
        "html_tag": "<article>",
        "role": "region",
        "keyboard": {
            "Enter": "Expands or collapses reasoning details.",
            "Space": "Toggles approval checkpoint.",
            "Tab": "Navigates between approval actions.",
        },
        "states": {
            "default": {
                "label": "Default (Resting)",
                "visual": "bg-white border border-gray-200 rounded-lg p-5 shadow-sm space-y-4",
                "behavior": "Shows high-level intent summary and agent status pill.",
                "aria": 'aria-label="Agent Execution Status"',
            },
            "hover": {
                "label": "Hover",
                "visual": "hover:border-gray-300 hover:shadow-md transition-all duration-200",
                "behavior": "Card elevates slightly when interactive actions are present.",
                "aria": "",
            },
            "active": {
                "label": "Active (Streaming)",
                "visual": "border-blue-500 ring-1 ring-blue-500/30",
                "behavior": "Active token streaming with pulse indicator.",
                "aria": 'aria-live="polite"',
            },
            "focus_visible": {
                "label": "Focus-Visible",
                "visual": "focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2",
                "behavior": "Focus highlights entire actionable container or nested action button.",
                "aria": ":focus-visible pseudo-class",
            },
            "disabled": {
                "label": "Disabled (Queued)",
                "visual": "opacity-60 bg-gray-50 border-gray-200 cursor-not-allowed",
                "behavior": "Agent is in queue awaiting upstream dependency completion.",
                "aria": 'aria-disabled="true"',
            },
            "loading": {
                "label": "Loading (Reasoning)",
                "visual": "bg-blue-50/30 border-blue-200 animate-pulse",
                "behavior": "Agent is planning steps or executing tools; displays step pill.",
                "aria": 'aria-busy="true"',
            },
            "empty": {
                "label": "Empty (Idle Prompt)",
                "visual": "border-dashed border-2 border-gray-300 text-center py-8",
                "behavior": "No active tasks. Displays prompt suggestions and capabilities overview.",
                "aria": "",
            },
            "error": {
                "label": "Error (Tool Failure)",
                "visual": "border-red-500 bg-red-50/30 text-red-900",
                "behavior": "Displays actionable error trace with 'Retry Task' and 'Modify Plan' options.",
                "aria": 'role="alert" aria-live="assertive"',
            },
        },
    },
}


def build_markdown_spec(name: str, comp_type: str, data: dict) -> str:
    lines = [
        f"# Component Specification: `{name}`",
        "",
        f"> **Component Archetype**: `{comp_type}` | **Role**: `{data['role']}` | **HTML Base**: `{data['html_tag']}`",
        "",
        data["description"],
        "",
        "---",
        "",
        "## 1. The 8-State Lifecycle Matrix",
        "",
        "| State | Label | Visual Classes (Tailwind CSS) | Interaction & Behavior | ARIA & Accessibility |",
        "| :---: | :--- | :--- | :--- | :--- |",
    ]

    for key, s in data["states"].items():
        lines.append(
            f"| `{key}` | **{s['label']}** | `{s['visual']}` | {s['behavior']} | `{s['aria']}` |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 2. Keyboard Ergonomics & Focus Management",
            "",
            "| Key Sequence | Expected Component Action |",
            "| :--- | :--- |",
        ]
    )

    for key, action in data["keyboard"].items():
        lines.append(f"| `<kbd>{key}</kbd>` | {action} |")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 3. WCAG 2.2 Level AA Verification Checklist",
            "",
            "- [x] **Contrast Ratio**: Baseline text and borders maintain $\\ge 4.5:1$ contrast against adjacent background.",
            "- [x] **Touch Target**: Sized to minimum $44 \\times 44\\text{ px}$ interactive bounding box on mobile.",
            "- [x] **Focus Ring**: Prominent 2px offset ring supplied for `:focus-visible` without suppressing keyboard outlines.",
            "- [x] **State Completeness**: Explicit handling for disabled, loading, empty, and error conditions.",
            "",
            "---",
            "",
            "## 4. Production Code Template (JSX / React with Tailwind)",
            "",
            "```tsx",
            f"// {name}.tsx - Accessible {comp_type.title()} Component with 8-State Support",
            "import React from 'react';",
            "",
            f"export interface {name}Props {{",
            "  label?: string;",
            "  isLoading?: boolean;",
            "  isDisabled?: boolean;",
            "  isError?: boolean;",
            "  errorMessage?: string;",
            "  onClick?: () => void;",
            "}",
            "",
            f"export const {name}: React.FC<{name}Props> = ({{",
            "  label = 'Action',",
            "  isLoading = false,",
            "  isDisabled = false,",
            "  isError = false,",
            "  errorMessage,",
            "  onClick,",
            "}) => {",
            "  return (",
            '    <div className="flex flex-col gap-1.5">',
            "      <button",
            '        type="button"',
            "        onClick={onClick}",
            "        disabled={isDisabled || isLoading}",
            "        aria-disabled={isDisabled || isLoading}",
            "        aria-busy={isLoading}",
            "        aria-invalid={isError}",
            "        className={`",
            f"          {data['states']['default']['visual']}",
            f"          {data['states']['hover']['visual']}",
            f"          {data['states']['active']['visual']}",
            f"          {data['states']['focus_visible']['visual']}",
            "          ${isDisabled ? '" + data["states"]["disabled"]["visual"] + "' : ''}",
            "          ${isError ? '" + data["states"]["error"]["visual"] + "' : ''}",
            "        `}",
            "      >",
            "        {isLoading ? (",
            '          <span className="flex items-center gap-2">',
            '            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">',
            '              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />',
            '              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />',
            "            </svg>",
            "            Loading...",
            "          </span>",
            "        ) : (",
            "          label",
            "        )}",
            "      </button>",
            "      {isError && errorMessage && (",
            '        <p role="alert" className="text-sm text-red-600 font-medium">',
            "          {errorMessage}",
            "        </p>",
            "      )}",
            "    </div>",
            "  );",
            "};",
            "```",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold production-grade 8-state component design specifications."
    )
    parser.add_argument(
        "--name", default="PrimaryButton", help="Component name (e.g. PrimaryButton, SearchInput)."
    )
    parser.add_argument(
        "--type",
        choices=["button", "input", "agent-card"],
        default="button",
        help="Component archetype template.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (markdown or json).",
    )
    parser.add_argument("--output", help="Optional output file path. Prints to stdout if omitted.")

    args = parser.parse_args()

    template = COMPONENT_TEMPLATES.get(args.type, COMPONENT_TEMPLATES["button"])

    if args.format == "json":
        result = json.dumps(
            {
                "name": args.name,
                "type": args.type,
                "specification": template,
            },
            indent=2,
        )
    else:
        result = build_markdown_spec(args.name, args.type, template)

    if args.output:
        p = Path(args.output)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(result, encoding="utf-8")
        print(f"Component specification written to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
