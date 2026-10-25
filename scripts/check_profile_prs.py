#!/usr/bin/env python3
"""Check that pull requests linked from a profile README are merged."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "readme", nargs="?", type=Path,
        default=Path(__file__).resolve().parents[1] / "README.md",
    )
    parser.add_argument("--author", help="Also require this GitHub login as PR author")
    args = parser.parse_args()
    try:
        text = args.readme.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Cannot read README: {exc}", file=sys.stderr)
        return 2

    links = sorted(set(re.findall(
        r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/pull/([1-9][0-9]*)\b",
        text,
    )))
    if not links:
        print("No GitHub pull request links found.", file=sys.stderr)
        return 1

    failed = False
    for repo, number in links:
        label = f"{repo}#{number}"
        try:
            response = subprocess.run(
                ["gh", "api", "--hostname", "github.com", f"repos/{repo}/pulls/{number}"],
                check=True, capture_output=True, text=True, timeout=30,
            )
            pr = json.loads(response.stdout)
            merged = pr["merged_at"] is not None
            author = pr["user"]["login"]
        except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError) as exc:
            print(f"Could not verify {label}: {exc}", file=sys.stderr)
            return 2

        valid = merged and (not args.author or author.lower() == args.author.lower())
        failed |= not valid
        status = "MERGED" if merged else "NOT MERGED"
        print(f"{'PASS' if valid else 'FAIL'} {label}: {status}, author={author}")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
