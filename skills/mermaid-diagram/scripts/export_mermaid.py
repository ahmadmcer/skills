#!/usr/bin/env python3
"""
Mermaid Diagram Batch Exporter & URL Encoder (export_mermaid.py)

Extracts Mermaid diagrams from .mmd or Markdown (.md) files and:
1. Generates zero-install compressed `pako:` URLs for:
   - Mermaid Live Editor (`https://mermaid.live/edit#pako:...`)
   - Mermaid.ink SVG/PNG (`https://mermaid.ink/svg/pako:...`)
   - Kroki.io SVG (`https://kroki.io/mermaid/svg/...`)
2. Renders local SVG, PNG, or PDF files via `@mermaid-js/mermaid-cli` (`mmdc`)
   or downloads rendered SVGs/PNGs from `mermaid.ink` / `kroki.io`.

Usage:
    python export_mermaid.py --input README.md --format url
    python export_mermaid.py --input arch.mmd --format svg --output-dir ./dist
"""

from __future__ import annotations

import argparse
import base64
import json
import pathlib
import shutil
import subprocess
import sys
import urllib.request
import zlib
from typing import Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Reuse block extractor from audit_mermaid
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from audit_mermaid import extract_mermaid_blocks  # noqa: E402


def encode_mermaid_pako(code: str, theme: str = "default") -> str:
    """
    Encode Mermaid diagram state into a pako-compatible zlib + base64url string
    used by https://mermaid.live and https://mermaid.ink.
    """
    state = {
        "code": code.strip(),
        "mermaid": json.dumps({"theme": theme}),
        "autoSync": True,
        "updateDiagram": True,
    }
    raw_bytes = json.dumps(state).encode("utf-8")
    compressed = zlib.compress(raw_bytes, level=9)
    b64 = base64.urlsafe_b64encode(compressed).decode("ascii")
    return f"pako:{b64}"


def encode_kroki(code: str) -> str:
    """Encode Mermaid code for https://kroki.io/mermaid/svg/<payload>."""
    compressed = zlib.compress(code.strip().encode("utf-8"), level=9)
    return base64.urlsafe_b64encode(compressed).decode("ascii")


def build_urls(code: str, theme: str = "default") -> Dict[str, str]:
    pako_token = encode_mermaid_pako(code, theme=theme)
    kroki_token = encode_kroki(code)
    return {
        "mermaid_live_edit": f"https://mermaid.live/edit#{pako_token}",
        "mermaid_live_view": f"https://mermaid.live/view#{pako_token}",
        "mermaid_ink_svg": f"https://mermaid.ink/svg/{pako_token}",
        "mermaid_ink_png": f"https://mermaid.ink/img/{pako_token}?type=png",
        "kroki_svg": f"https://kroki.io/mermaid/svg/{kroki_token}",
    }


def render_with_mmdc(
    code: str,
    out_file: pathlib.Path,
    theme: str = "default",
    scale: int = 2,
) -> bool:
    mmdc_bin = shutil.which("mmdc")
    if not mmdc_bin:
        return False
    cmd = [
        mmdc_bin,
        "-i",
        "-",
        "-o",
        str(out_file),
        "-t",
        theme,
        "-b",
        "transparent",
        "-s",
        str(scale),
        "-q",
    ]
    proc = subprocess.run(cmd, input=code, text=True, capture_output=True, timeout=30)
    return proc.returncode == 0 and out_file.exists()


def download_remote(url: str, out_file: pathlib.Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "mermaid-diagram-skill/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read()
        out_file.write_bytes(data)
    return out_file.exists()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract Mermaid diagrams and export to SVG/PNG/PDF or shareable mermaid.live / Kroki URLs."
    )
    parser.add_argument("--input", type=pathlib.Path, required=True, help="Input .mmd or .md file")
    parser.add_argument(
        "--format",
        choices=["url", "svg", "png", "pdf"],
        default="url",
        help="Output format (default: url)",
    )
    parser.add_argument(
        "--engine",
        choices=["auto", "mmdc", "mermaid-ink", "kroki"],
        default="auto",
        help="Rendering engine for svg/png/pdf exports (default: auto)",
    )
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("./diagrams-out"), help="Output directory")
    parser.add_argument("--theme", type=str, default="default", help="Theme name")
    parser.add_argument("--scale", type=int, default=2, help="Scale factor for PNG rendering (default: 2)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 2

    blocks = extract_mermaid_blocks(args.input)
    if not blocks:
        print(f"No Mermaid blocks found in {args.input}", file=sys.stderr)
        return 1

    export_records: List[Dict[str, object]] = []
    if args.format != "url":
        args.output_dir.mkdir(parents=True, exist_ok=True)

    stem = args.input.stem
    for idx, (start_ln, code) in enumerate(blocks, start=1):
        urls = build_urls(code, theme=args.theme)
        record: Dict[str, object] = {
            "index": idx,
            "start_line": start_ln,
            "urls": urls,
        }

        if args.format != "url":
            out_path = args.output_dir / f"{stem}-diagram-{idx}.{args.format}"
            rendered_ok = False
            engine_used = args.engine

            if args.engine in {"auto", "mmdc"}:
                if render_with_mmdc(code, out_path, theme=args.theme, scale=args.scale):
                    rendered_ok = True
                    engine_used = "mmdc"
                elif args.engine == "mmdc":
                    print(f"Error: mmdc failed or is not installed for diagram #{idx}.", file=sys.stderr)
                    return 1

            if not rendered_ok and args.format in {"svg", "png"}:
                remote_url = (
                    urls["kroki_svg"]
                    if args.engine == "kroki" and args.format == "svg"
                    else (urls["mermaid_ink_svg"] if args.format == "svg" else urls["mermaid_ink_png"])
                )
                engine_used = "kroki" if args.engine == "kroki" else "mermaid-ink"
                try:
                    rendered_ok = download_remote(remote_url, out_path)
                except Exception as exc:
                    record["render_error"] = str(exc)

            record["output_file"] = str(out_path) if rendered_ok else None
            record["engine_used"] = engine_used if rendered_ok else None

        export_records.append(record)

    if args.json:
        print(json.dumps({"input": str(args.input), "diagrams": export_records}, indent=2))
    else:
        for rec in export_records:
            print(f"=== Diagram #{rec['index']} (Line {rec['start_line']}) ===")
            urls = rec["urls"]
            assert isinstance(urls, dict)
            print(f"  Mermaid Live Edit : {urls['mermaid_live_edit']}")
            print(f"  Mermaid.ink SVG   : {urls['mermaid_ink_svg']}")
            print(f"  Kroki.io SVG      : {urls['kroki_svg']}")
            if rec.get("output_file"):
                print(f"  Exported File     : {rec['output_file']} (via {rec['engine_used']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
