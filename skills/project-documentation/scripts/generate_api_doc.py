#!/usr/bin/env python3
"""
generate_api_doc.py - Generate Diátaxis-compliant API reference markdown from OpenAPI 3.0/3.1 specs.

Features:
- Parses OpenAPI 3.0 and 3.1 specifications (JSON or YAML).
- Groups endpoints by OpenAPI tags or URL paths.
- Renders HTTP method badges, summary descriptions, and operation IDs.
- Formats request parameters (path, query, header) into clear markdown tables.
- Renders request body schemas and realistic JSON example payloads.
- Formats responses with status codes, descriptions, and RFC 9457 Problem Details schemas.
- Produces valid YAML frontmatter compliant with DocOps quality gates.

Usage:
    python generate_api_doc.py --spec ./openapi.json --output ./docs/reference/api.md
    python generate_api_doc.py --spec ./openapi.yaml --output ./docs/reference/api.md --rfc9457
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def slugify(text: str) -> str:
    """Generate markdown-compatible heading slug."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def parse_spec_file(spec_path: Path) -> Dict[str, Any]:
    """Parse JSON or YAML OpenAPI specification."""
    if not spec_path.exists():
        raise FileNotFoundError(f"OpenAPI spec file not found: {spec_path}")

    content = spec_path.read_text(encoding="utf-8", errors="replace")
    suffix = spec_path.suffix.lower()

    if suffix in (".yaml", ".yml"):
        if not HAS_YAML:
            raise ImportError(
                "PyYAML is required to parse YAML files. Install it via 'pip install pyyaml' "
                "or convert your spec to JSON."
            )
        return yaml.safe_load(content)
    else:
        # Default to JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError as err:
            if HAS_YAML:
                # Try parsing as YAML in case it's a YAML file with .json or other extension
                try:
                    return yaml.safe_load(content)
                except Exception:
                    pass
            raise ValueError(f"Failed to parse OpenAPI JSON specification: {err}")


def resolve_ref(ref: str, root_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve local JSON pointer reference like #/components/schemas/Pet."""
    if not ref.startswith("#/"):
        return {}
    parts = ref.lstrip("#/").split("/")
    curr = root_spec
    for p in parts:
        if isinstance(curr, dict) and p in curr:
            curr = curr[p]
        else:
            return {}
    return curr if isinstance(curr, dict) else {}


def generate_example_from_schema(schema: Dict[str, Any], root_spec: Dict[str, Any], depth: int = 0) -> Any:
    """Generate a realistic mock JSON object from a JSON Schema / OpenAPI schema definition."""
    if depth > 5:
        return {}

    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], root_spec)

    # If schema has an explicit example, return it
    if "example" in schema:
        return schema["example"]

    stype = schema.get("type", "object")
    sformat = schema.get("format", "")

    if stype == "string":
        if "enum" in schema and schema["enum"]:
            return schema["enum"][0]
        if sformat == "date-time":
            return "2026-09-30T12:00:00Z"
        if sformat == "date":
            return "2026-09-30"
        if sformat == "email":
            return "user@example.com"
        if sformat == "uuid":
            return "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        if sformat == "uri" or sformat == "url":
            return "https://api.example.com/v1/resource"
        return "sample_string"

    if stype == "integer":
        return schema.get("default", 42)

    if stype == "number":
        return schema.get("default", 19.99)

    if stype == "boolean":
        return schema.get("default", True)

    if stype == "array":
        items_schema = schema.get("items", {})
        item_example = generate_example_from_schema(items_schema, root_spec, depth + 1)
        return [item_example]

    if stype == "object" or "properties" in schema:
        obj = {}
        props = schema.get("properties", {})
        for prop_name, prop_schema in props.items():
            obj[prop_name] = generate_example_from_schema(prop_schema, root_spec, depth + 1)
        return obj

    return {}


def format_schema_table(schema: Dict[str, Any], root_spec: Dict[str, Any], prefix: str = "") -> List[Tuple[str, str, str, str]]:
    """Flatten schema properties into a list of (field_name, type, required, description) tuples."""
    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], root_spec)

    rows = []
    props = schema.get("properties", {})
    required_fields = set(schema.get("required", []))

    for name, prop in props.items():
        if "$ref" in prop:
            prop = resolve_ref(prop["$ref"], root_spec)

        full_name = f"{prefix}{name}"
        ftype = prop.get("type", "any")
        if ftype == "array":
            item_type = prop.get("items", {}).get("type", "object")
            ftype = f"array[{item_type}]"
        elif "format" in prop:
            ftype = f"{ftype} ({prop['format']})"

        is_req = "Yes" if name in required_fields else "No"
        desc = prop.get("description", "-").replace("\n", " ").strip()
        rows.append((full_name, ftype, is_req, desc))

        # Nested objects
        if prop.get("type") == "object" and "properties" in prop:
            rows.extend(format_schema_table(prop, root_spec, prefix=f"{full_name}."))

    return rows


def generate_rfc9457_example(status_code: str, title: str, detail: str) -> Dict[str, Any]:
    """Generate standard RFC 9457 Problem Details payload."""
    status_int = int(status_code) if status_code.isdigit() else 400
    return {
        "type": f"https://api.example.com/errors/rfc9457/{status_code}",
        "title": title,
        "status": status_int,
        "detail": detail,
        "instance": f"/api/errors/urn:uuid:{status_code}00000-0000-0000-0000-000000000000",
    }


def render_markdown(
    spec: Dict[str, Any],
    title_override: Optional[str] = None,
    group_by: str = "tags",
    use_rfc9457: bool = True,
) -> str:
    """Render OpenAPI specification dictionary to comprehensive Markdown reference."""
    info = spec.get("info", {})
    title = title_override or info.get("title", "API Reference")
    version = info.get("version", "1.0.0")
    description = info.get("description", "Comprehensive API reference and endpoint specifications.")

    # Frontmatter
    lines = [
        "---",
        f'title: "{title} (v{version})"',
        f'description: "{description.splitlines()[0] if description else "API Reference"}"',
        "---",
        "",
        f"# {title}",
        "",
        f"> **Specification Version**: `v{version}`",
        "",
    ]

    # Servers
    servers = spec.get("servers", [])
    if servers:
        lines.append("## Base Servers")
        lines.append("")
        for s in servers:
            s_url = s.get("url", "")
            s_desc = s.get("description", "Production environment")
            lines.append(f"- `{s_url}` ({s_desc})")
        lines.append("")

    if description:
        lines.append("## Overview")
        lines.append("")
        lines.append(description)
        lines.append("")

    # Extract all operations
    paths = spec.get("paths", {})
    operations = []
    HTTP_METHODS = ["get", "post", "put", "delete", "patch", "options", "head"]

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        # Common path-level parameters
        common_params = path_item.get("parameters", [])

        for method in HTTP_METHODS:
            if method in path_item:
                op = path_item[method]
                if not isinstance(op, dict):
                    continue
                # Merge parameters
                op_params = list(common_params) + op.get("parameters", [])
                operations.append({
                    "path": path,
                    "method": method.upper(),
                    "summary": op.get("summary", f"{method.upper()} {path}"),
                    "description": op.get("description", ""),
                    "tags": op.get("tags", ["General"]),
                    "operationId": op.get("operationId", f"{method}_{path}"),
                    "parameters": op_params,
                    "requestBody": op.get("requestBody", {}),
                    "responses": op.get("responses", {}),
                })

    if not operations:
        lines.append("> No endpoints found in specification.")
        return "\n".join(lines)

    # Group operations
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    if group_by == "tags":
        for op in operations:
            for tag in op["tags"]:
                grouped.setdefault(tag, []).append(op)
    else:
        for op in operations:
            grouped.setdefault(op["path"], []).append(op)

    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    for group_name, ops in grouped.items():
        lines.append(f"- **[{group_name}](#{slugify(group_name)})**")
        for op in ops:
            op_title = f"{op['method']} {op['path']}"
            op_anchor = slugify(f"{op['method']} {op['path']}")
            lines.append(f"  - [`{op['method']}` {op['path']}](#{op_anchor}) - *{op['summary']}*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Render Groups and Endpoints
    for group_name, ops in grouped.items():
        lines.append(f"## {group_name}")
        lines.append("")

        for op in ops:
            m = op["method"]
            p = op["path"]
            op_anchor_heading = f"### {m} {p}"
            lines.append(op_anchor_heading)
            lines.append("")
            lines.append(f"`{m}` **`{p}`**")
            lines.append("")

            if op["summary"]:
                lines.append(f"**{op['summary']}**")
                lines.append("")
            if op["description"]:
                lines.append(op["description"])
                lines.append("")

            # Parameters table
            raw_params = op["parameters"]
            if raw_params:
                lines.append("#### Request Parameters")
                lines.append("")
                lines.append("| Name | In | Type | Required | Description |")
                lines.append("| :--- | :--- | :--- | :---: | :--- |")

                for param in raw_params:
                    if "$ref" in param:
                        param = resolve_ref(param["$ref"], spec)
                    p_name = param.get("name", "")
                    p_in = param.get("in", "query")
                    p_req = "Yes" if param.get("required", False) else "No"
                    p_desc = param.get("description", "-").replace("\n", " ").strip()
                    p_schema = param.get("schema", {})
                    p_type = p_schema.get("type", "string")
                    if "format" in p_schema:
                        p_type = f"{p_type} ({p_schema['format']})"
                    lines.append(f"| `{p_name}` | `{p_in}` | {p_type} | {p_req} | {p_desc} |")
                lines.append("")

            # Request Body
            req_body = op["requestBody"]
            if req_body:
                if "$ref" in req_body:
                    req_body = resolve_ref(req_body["$ref"], spec)

                lines.append("#### Request Body")
                lines.append("")
                b_desc = req_body.get("description", "")
                if b_desc:
                    lines.append(f"{b_desc}")
                    lines.append("")

                content_map = req_body.get("content", {})
                for c_type, c_data in content_map.items():
                    lines.append(f"**Content-Type**: `{c_type}`")
                    lines.append("")
                    b_schema = c_data.get("schema", {})

                    # Schema property table
                    rows = format_schema_table(b_schema, spec)
                    if rows:
                        lines.append("| Property | Type | Required | Description |")
                        lines.append("| :--- | :--- | :---: | :--- |")
                        for r_name, r_type, r_req, r_desc in rows:
                            lines.append(f"| `{r_name}` | `{r_type}` | {r_req} | {r_desc} |")
                        lines.append("")

                    # Example JSON
                    if "example" in c_data:
                        ex = c_data["example"]
                    elif "examples" in c_data:
                        first_k = next(iter(c_data["examples"]))
                        ex = c_data["examples"][first_k].get("value", {})
                    else:
                        ex = generate_example_from_schema(b_schema, spec)

                    if ex:
                        lines.append("```json")
                        lines.append(json.dumps(ex, indent=2))
                        lines.append("```")
                        lines.append("")

            # Responses
            responses = op["responses"]
            if responses:
                lines.append("#### Responses")
                lines.append("")

                for status_code, resp in responses.items():
                    if "$ref" in resp:
                        resp = resolve_ref(resp["$ref"], spec)

                    status_desc = resp.get("description", "Response")
                    lines.append(f"##### HTTP `{status_code}` - {status_desc}")
                    lines.append("")

                    r_content = resp.get("content", {})
                    if r_content:
                        for rc_type, rc_data in r_content.items():
                            lines.append(f"**Content-Type**: `{rc_type}`")
                            lines.append("")
                            r_schema = rc_data.get("schema", {})

                            rows = format_schema_table(r_schema, spec)
                            if rows:
                                lines.append("| Property | Type | Required | Description |")
                                lines.append("| :--- | :--- | :---: | :--- |")
                                for r_name, r_type, r_req, r_desc in rows:
                                    lines.append(f"| `{r_name}` | `{r_type}` | {r_req} | {r_desc} |")
                                lines.append("")

                            if "example" in rc_data:
                                r_ex = rc_data["example"]
                            elif "examples" in rc_data:
                                first_k = next(iter(rc_data["examples"]))
                                r_ex = rc_data["examples"][first_k].get("value", {})
                            else:
                                r_ex = generate_example_from_schema(r_schema, spec)

                            if r_ex:
                                lines.append("```json")
                                lines.append(json.dumps(r_ex, indent=2))
                                lines.append("```")
                                lines.append("")
                    else:
                        # If error status code and no content provided, provide RFC 9457 Problem Details example
                        if use_rfc9457 and status_code.startswith(("4", "5")):
                            lines.append("**RFC 9457 Problem Details Schema** (`application/problem+json`):")
                            lines.append("")
                            rfc_ex = generate_rfc9457_example(
                                status_code,
                                status_desc,
                                f"An error occurred executing {m} {p}."
                            )
                            lines.append("```json")
                            lines.append(json.dumps(rfc_ex, indent=2))
                            lines.append("```")
                            lines.append("")

            lines.append("---")
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Diátaxis-compliant API reference markdown from OpenAPI 3.0/3.1 specs."
    )
    parser.add_argument(
        "--spec",
        required=True,
        help="Path to OpenAPI 3.0/3.1 JSON or YAML specification file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Target output markdown file path (defaults to stdout)",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Optional override for documentation title",
    )
    parser.add_argument(
        "--group-by",
        choices=["tags", "paths"],
        default="tags",
        help="Group operations by tags or paths (default: tags)",
    )
    parser.add_argument(
        "--rfc9457",
        action="store_true",
        default=True,
        help="Generate RFC 9457 Problem Details schemas for 4xx/5xx responses (default: True)",
    )

    args = parser.parse_args()

    spec_path = Path(args.spec)
    try:
        spec_data = parse_spec_file(spec_path)
    except Exception as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        return 1

    markdown_out = render_markdown(
        spec=spec_data,
        title_override=args.title,
        group_by=args.group_by,
        use_rfc9457=args.rfc9457,
    )

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown_out, encoding="utf-8")
        print(f"[PASS] Successfully generated API reference documentation at: {out_path}")
    else:
        print(markdown_out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
