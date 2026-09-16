#!/usr/bin/env python3
"""Validate suite structure and local links without third-party packages."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "codebase-onboarding", "codebase-tutorial", "codebase-architecture",
    "codebase-trace", "codebase-deep-dive", "codebase-change",
    "codebase-hotspots", "codebase-coupling", "codebase-verify",
}


def main() -> int:
    errors: list[str] = []
    portable_path = ROOT / "plugin.json"
    try:
        portable = json.loads(portable_path.read_text(encoding="utf-8"))
        if portable.get("name") != "codebase-intelligence" or not portable.get("$schema"):
            errors.append("portable plugin manifest is incomplete")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid portable plugin manifest: {exc}")

    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("name") != "codebase-intelligence":
            errors.append("plugin manifest name is incorrect")
        if manifest.get("skills") != "./skills/":
            errors.append("plugin manifest skills path is incorrect")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid plugin manifest: {exc}")

    actual = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if actual != EXPECTED:
        errors.append(f"skill set mismatch: expected {sorted(EXPECTED)}, found {sorted(actual)}")

    link_pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
    for name in sorted(EXPECTED):
        skill = ROOT / "skills" / name / "SKILL.md"
        agent = ROOT / "skills" / name / "agents" / "openai.yaml"
        if not skill.is_file():
            errors.append(f"missing {skill.relative_to(ROOT)}")
            continue
        text = skill.read_text(encoding="utf-8")
        frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not frontmatter:
            errors.append(f"{name}: missing YAML frontmatter")
        else:
            block = frontmatter.group(1)
            if f"name: {name}" not in block or "description:" not in block:
                errors.append(f"{name}: invalid name or description")
        if not agent.is_file() or "allow_implicit_invocation: false" not in agent.read_text(encoding="utf-8"):
            errors.append(f"{name}: explicit-only policy missing")
        for target in link_pattern.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (skill.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_file():
                errors.append(f"{name}: broken link {target}")

    for path in ROOT.rglob("*"):
        if path.is_file() and not any(part in {".git", "__pycache__"} for part in path.parts):
            try:
                placeholder = "[" + "TODO:"
                if placeholder in path.read_text(encoding="utf-8"):
                    errors.append(f"unfinished placeholder in {path.relative_to(ROOT)}")
            except UnicodeDecodeError:
                pass

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated portable/compatibility manifests, {len(EXPECTED)} skills, explicit invocation policies, and local links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
