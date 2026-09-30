#!/usr/bin/env python3
"""
Scaffold Vector Brand Assets (SVGs).

Generates spec-compliant, accessible SVG templates:
1. logo-primary.svg (Horizontal brand mark & wordmark)
2. logo-stacked.svg (Stacked icon + wordmark)
3. favicon.svg (Vector symbol optimized for 32x32)
4. app-icon.svg (512x512 squircle application icon)
5. og-image.svg (1200x630 OpenGraph social share card)
"""

import argparse
import os
import sys
from typing import Dict, Any


def generate_primary_logo_svg(name: str, primary_color: str, neutral_color: str) -> str:
    """Generate horizontal brand mark and wordmark SVG."""
    initial = name[0].upper() if name else "B"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 80" width="100%" height="100%" fill="none" role="img" aria-label="{name} Logo">
  <defs>
    <linearGradient id="brand-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary_color}" />
      <stop offset="100%" stop-color="#1d4ed8" />
    </linearGradient>
  </defs>
  <!-- Symbol Mark -->
  <g transform="translate(10, 10)">
    <rect width="60" height="60" rx="14" fill="url(#brand-grad)" />
    <path d="M 20 42 L 30 18 L 40 42 Z" fill="#ffffff" opacity="0.95" />
    <circle cx="30" cy="30" r="5" fill="#ffffff" />
  </g>
  <!-- Wordmark -->
  <text x="86" y="50" font-family="system-ui, -apple-system, sans-serif" font-size="32" font-weight="700" letter-spacing="-0.5px" fill="{neutral_color}">
    {name}
  </text>
</svg>
"""


def generate_stacked_logo_svg(name: str, primary_color: str, neutral_color: str) -> str:
    """Generate vertical/stacked brand mark and wordmark SVG."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 200" width="100%" height="100%" fill="none" role="img" aria-label="{name} Stacked Logo">
  <defs>
    <linearGradient id="brand-grad-stacked" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary_color}" />
      <stop offset="100%" stop-color="#1d4ed8" />
    </linearGradient>
  </defs>
  <!-- Centered Symbol Mark -->
  <g transform="translate(80, 20)">
    <rect width="80" height="80" rx="18" fill="url(#brand-grad-stacked)" />
    <path d="M 26 56 L 40 24 L 54 56 Z" fill="#ffffff" opacity="0.95" />
    <circle cx="40" cy="40" r="6" fill="#ffffff" />
  </g>
  <!-- Centered Wordmark -->
  <text x="120" y="148" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="700" letter-spacing="-0.5px" fill="{neutral_color}">
    {name}
  </text>
</svg>
"""


def generate_favicon_svg(primary_color: str) -> str:
    """Generate 32x32 vector favicon SVG."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" fill="none" role="img" aria-label="Favicon">
  <rect width="32" height="32" rx="7" fill="{primary_color}" />
  <path d="M 10 22 L 16 9 L 22 22 Z" fill="#ffffff" />
  <circle cx="16" cy="15" r="2.5" fill="{primary_color}" />
</svg>
"""


def generate_app_icon_svg(name: str, primary_color: str) -> str:
    """Generate 512x512 rounded squircle application icon SVG."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" fill="none" role="img" aria-label="{name} App Icon">
  <defs>
    <linearGradient id="app-icon-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary_color}" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000000" flood-opacity="0.3" />
    </filter>
  </defs>
  <!-- Squircle Canvas -->
  <rect width="512" height="512" rx="115" fill="url(#app-icon-grad)" />
  <!-- Icon Emblem -->
  <g transform="translate(136, 136)" filter="url(#shadow)">
    <rect width="240" height="240" rx="54" fill="#ffffff" opacity="0.12" stroke="#ffffff" stroke-width="4" stroke-opacity="0.25" />
    <path d="M 80 170 L 120 70 L 160 170 Z" fill="#ffffff" />
    <circle cx="120" cy="120" r="18" fill="{primary_color}" />
  </g>
</svg>
"""


def generate_og_card_svg(
    name: str, tagline: str, primary_color: str, neutral_color: str
) -> str:
    """Generate 1200x630 OpenGraph social share card SVG."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" fill="none" role="img" aria-label="{name} OpenGraph Card">
  <defs>
    <linearGradient id="og-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <radialGradient id="og-glow" cx="80%" cy="20%" r="50%">
      <stop offset="0%" stop-color="{primary_color}" stop-opacity="0.28" />
      <stop offset="100%" stop-color="{primary_color}" stop-opacity="0.0" />
    </radialGradient>
  </defs>
  <!-- Background -->
  <rect width="1200" height="630" fill="url(#og-bg)" />
  <rect width="1200" height="630" fill="url(#og-glow)" />
  
  <!-- Subtle Grid Accent -->
  <g stroke="#ffffff" stroke-opacity="0.04" stroke-width="1">
    <line x1="80" y1="0" x2="80" y2="630" />
    <line x1="1120" y1="0" x2="1120" y2="630" />
    <line x1="0" y1="550" x2="1200" y2="550" />
  </g>

  <!-- Brand Mark -->
  <g transform="translate(100, 100)">
    <rect width="64" height="64" rx="16" fill="{primary_color}" />
    <path d="M 22 45 L 32 19 L 42 45 Z" fill="#ffffff" />
    <circle cx="32" cy="32" r="5" fill="#ffffff" />
    <text x="84" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="34" font-weight="700" letter-spacing="-0.5px" fill="#ffffff">
      {name}
    </text>
  </g>

  <!-- Headline & Subtitle -->
  <g transform="translate(100, 260)">
    <text x="0" y="50" font-family="system-ui, -apple-system, sans-serif" font-size="56" font-weight="800" letter-spacing="-1.5px" fill="#ffffff">
      {name}
    </text>
    <text x="0" y="115" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="400" letter-spacing="-0.2px" fill="#94a3b8">
      {tagline}
    </text>
  </g>

  <!-- Footer Tag -->
  <g transform="translate(100, 510)">
    <rect width="140" height="34" rx="17" fill="{primary_color}" fill-opacity="0.15" stroke="{primary_color}" stroke-opacity="0.3" />
    <text x="70" y="22" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="{primary_color}">
      Official Platform
    </text>
  </g>
</svg>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold responsive SVG brand templates."
    )
    parser.add_argument("--name", default="Acme", help="Brand name")
    parser.add_argument(
        "--tagline",
        default="The developer platform for high-velocity teams",
        help="Brand tagline",
    )
    parser.add_argument(
        "--primary", default="#2563eb", help="Primary brand color (hex)"
    )
    parser.add_argument(
        "--neutral", default="#0f172a", help="Neutral dark color for wordmark (hex)"
    )
    parser.add_argument(
        "--out-dir", default="./brand-assets/svg", help="Output directory"
    )

    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    files_generated = [
        (
            "logo-primary.svg",
            generate_primary_logo_svg(args.name, args.primary, args.neutral),
        ),
        (
            "logo-stacked.svg",
            generate_stacked_logo_svg(args.name, args.primary, args.neutral),
        ),
        ("favicon.svg", generate_favicon_svg(args.primary)),
        ("app-icon.svg", generate_app_icon_svg(args.name, args.primary)),
        (
            "og-image.svg",
            generate_og_card_svg(args.name, args.tagline, args.primary, args.neutral),
        ),
    ]

    for fname, content in files_generated:
        fpath = os.path.join(args.out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

    print(
        f"Successfully generated {len(files_generated)} SVG assets in '{args.out_dir}':"
    )
    for fname, _ in files_generated:
        print(f"  - {fname}")


if __name__ == "__main__":
    main()
