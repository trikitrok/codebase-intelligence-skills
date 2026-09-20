#!/usr/bin/env python3
"""Offline structural validation for the contracted V3 tree."""
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={"codebase-onboarding","codebase-conversational-tutorial","codebase-architecture","codebase-trace","codebase-deep-dive","codebase-change","codebase-hotspots","codebase-coupling","codebase-verify"}
OBSOLETE=("codebase_intelligence.py","default-store","analyze-history","cache-status","rank-hotspots","adapt-code-maat","verify-references","core.md","source-first.md","tool-first.md","tool-providers.md","evidence-contract.md","verification.md","tutorial-workflow.md","Evidence v1")
def main():
    errors=[]
    manifests=[]
    for path in (ROOT/"plugin.json",ROOT/".codex-plugin/plugin.json"):
        try:
            data=json.loads(path.read_text())
            if data.get("name")!="codebase-intelligence": errors.append(f"invalid manifest name: {path}")
            if data.get("skills") != "./skills/": errors.append(f"skill exposure missing or inconsistent: {path}")
            manifests.append(data.get("skills"))
        except Exception as exc: errors.append(f"invalid manifest {path}: {exc}")
    if len(manifests)==2 and manifests[0] != manifests[1]: errors.append("portable and compatibility manifests expose different skills")
    actual={p.name for p in (ROOT/"skills").iterdir() if p.is_dir()}
    if actual!=EXPECTED: errors.append(f"skill set mismatch: {sorted(actual)}")
    links=re.compile(r"\[[^]]*\]\(([^)]+)\)")
    for name in EXPECTED:
        skill=ROOT/"skills"/name/"SKILL.md"; agent=skill.parent/"agents/openai.yaml"
        if not skill.is_file(): errors.append(f"missing {skill}"); continue
        text=skill.read_text()
        if not re.match(r"^---\n.*?name: "+re.escape(name)+r"\n.*?description:.*?\n---",text,re.S): errors.append(f"{name}: invalid frontmatter")
        if "allow_implicit_invocation: false" not in agent.read_text(): errors.append(f"{name}: explicit policy missing")
        if "../../shared/references/analysis-basics.md" not in text: errors.append(f"{name}: analysis basics not linked")
        if name in ("codebase-hotspots","codebase-coupling") and "../../shared/references/history-analysis.md" not in text: errors.append(f"{name}: history reference not linked")
        if name not in ("codebase-hotspots","codebase-coupling") and "history-analysis.md" in text: errors.append(f"{name}: history reference loaded unexpectedly")
        for target in links.findall(text):
            if "://" not in target and not target.startswith("#") and not (skill.parent/target.split("#",1)[0]).resolve().is_file(): errors.append(f"{name}: broken link {target}")
    for reference in (ROOT/"shared/references").glob("*.md"):
        text=reference.read_text()
        for target in links.findall(text):
            if "://" not in target and not target.startswith("#") and not (reference.parent/target.split("#",1)[0]).resolve().is_file(): errors.append(f"{reference.relative_to(ROOT)}: broken link {target}")
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.name != "validate_suite.py":
            try: text=path.read_text()
            except UnicodeDecodeError: continue
            if "[TODO:" in text: errors.append(f"unfinished placeholder: {path.relative_to(ROOT)}")
            if path.name not in {"SPEC.md","SPEC-V3.md","runtime-audit.md","v3-architecture.md","v3-conformance-audit.md"}:
                for obsolete in OBSOLETE:
                    if obsolete in text: errors.append(f"obsolete {obsolete} in {path.relative_to(ROOT)}")
    if (ROOT/"shared/scripts/codebase_intelligence.py").exists(): errors.append("obsolete V2 helper remains")
    if errors: print("\n".join("ERROR: "+x for x in errors)); return 1
    print("Validated V3 manifests, nine explicit skills, shared-reference loading, local links, and contracted machinery."); return 0
if __name__=="__main__": raise SystemExit(main())
