#!/usr/bin/env python3
"""
Export a multi-page info-card HTML file into ordered PNG files.

This is the default rendering path for info-card-designer:
- one `card.html` containing multiple fixed-size page containers
- one PNG per page, exported in DOM order
- zero-padded filenames so lexicographic sorting stays stable

Usage:
  python export_pages.py /path/to/card.html
  python export_pages.py /path/to/card.html --selector ".card-page" --clean
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_SELECTOR = ".card-page"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export multi-page info-card HTML into ordered PNG files."
    )
    parser.add_argument("html_path", help="Path to the generated card.html file")
    parser.add_argument(
        "--out-dir",
        help="Output directory for PNG files. Defaults to the HTML file directory.",
    )
    parser.add_argument(
        "--selector",
        default=DEFAULT_SELECTOR,
        help=f"CSS selector for page containers. Default: {DEFAULT_SELECTOR!r}",
    )
    parser.add_argument(
        "--prefix",
        default="card",
        help="Filename prefix for generated PNGs. Default: card",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=900,
        help="Viewport width in CSS pixels. Default: 900",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1125,
        help="Viewport height in CSS pixels. Default: 1125",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=2,
        help="Playwright device scale factor. Default: 2",
    )
    parser.add_argument(
        "--wait-ms",
        type=int,
        default=2000,
        help="Additional wait time after page load for fonts/layout. Default: 2000",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=30000,
        help="Navigation and ready timeout. Default: 30000",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing generated PNGs with the same prefix before export.",
    )
    return parser.parse_args(argv)


def clean_existing_outputs(out_dir: Path, prefix: str) -> None:
    pattern = re.compile(rf"^{re.escape(prefix)}-\d+\.png$", re.IGNORECASE)
    for child in out_dir.iterdir():
        if child.is_file() and pattern.match(child.name):
            child.unlink()


def export_pages(args: argparse.Namespace) -> list[Path]:
    html_path = Path(args.html_path).expanduser().resolve()
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")
    if html_path.suffix.lower() != ".html":
        raise ValueError(f"Expected an HTML file, got: {html_path}")

    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else html_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        clean_existing_outputs(out_dir, args.prefix)

    from playwright.sync_api import sync_playwright

    saved_paths: list[Path] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        page.goto(html_path.as_uri(), wait_until="load", timeout=args.timeout_ms)
        page.wait_for_timeout(args.wait_ms)
        page.evaluate(
            """
            () => {
              if (!document.fonts || !document.fonts.ready) {
                return Promise.resolve();
              }
              return document.fonts.ready;
            }
            """
        )

        locator = page.locator(args.selector)
        page_count = locator.count()
        if page_count == 0:
            raise RuntimeError(
                f"No page containers found with selector {args.selector!r} in {html_path}"
            )

        digits = max(2, len(str(page_count)))
        for index in range(page_count):
            target = locator.nth(index)
            target.scroll_into_view_if_needed(timeout=args.timeout_ms)
            filename = f"{args.prefix}-{index + 1:0{digits}d}.png"
            out_path = out_dir / filename
            target.screenshot(path=str(out_path))
            saved_paths.append(out_path)

        browser.close()

    return saved_paths


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    paths = export_pages(args)
    print(f"Exported {len(paths)} page(s):")
    for path in paths:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
