#!/usr/bin/env python3
"""Deterministic evidence helpers for the Codebase Intelligence skills.

The CLI is intentionally standard-library-only. It records observations, not
semantic conclusions, and never installs tools or changes the analyzed repo.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from itertools import combinations
from typing import Any, Iterable


SCHEMA_VERSION = 1
ANALYZER_VERSION = "0.1.0"
HISTORY_PROVIDER = "codebase-intelligence-git"
LOC_DEFINITION_VERSION = "physical-lines-v1"
IGNORED_PATH_PARTS = frozenset({
    ".git", ".cache", ".venv", "__pycache__", "build", "cache", "coverage",
    "dist", "generated", "node_modules", "target", "vendor", "venv",
})
EVIDENCE_TYPES = {
    "change_frequency",
    "churn",
    "temporal_coupling",
    "ownership",
    "complexity",
    "static_dependency",
    "test_coverage",
}
SUBJECT_TYPES = {
    "repository",
    "component",
    "directory",
    "file",
    "symbol",
    "file_pair",
    "component_pair",
}


class CBIError(Exception):
    """Expected user-facing failure."""


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise CBIError(f"required command is unavailable: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or f"exit {exc.returncode}"
        raise CBIError(f"command failed ({' '.join(command)}): {detail}") from exc


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], repo, check=check)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="surrogateescape")).hexdigest()


def ensure_repo(path: str) -> tuple[Path, Path]:
    requested = Path(path).resolve()
    if not requested.exists():
        raise CBIError(f"repository path does not exist: {requested}")
    probe = git(requested, "rev-parse", "--show-toplevel", check=False)
    if probe.returncode != 0:
        raise CBIError(f"not a Git repository: {requested}")
    return requested, Path(probe.stdout.strip()).resolve()


def repository_id(root: Path) -> str:
    remote = git(root, "config", "--get", "remote.origin.url", check=False).stdout.strip()
    first = git(root, "rev-list", "--max-parents=0", "HEAD", check=False).stdout.splitlines()
    stable = remote or (first[-1] if first else str(root))
    return sha256_text(stable)[:20]


def dirty_fingerprint(root: Path) -> tuple[bool, str]:
    status = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    digest = hashlib.sha256(status.encode("utf-8", errors="surrogateescape"))
    for entry in sorted(filter(None, status.split("\0"))):
        rel = entry[3:] if len(entry) > 3 else ""
        candidate = root / rel
        if candidate.is_file():
            digest.update(rel.encode("utf-8", errors="surrogateescape"))
            try:
                digest.update(candidate.read_bytes())
            except OSError:
                digest.update(b"<unreadable>")
    return bool(status), digest.hexdigest()


def repo_metadata(repo: str) -> dict[str, Any]:
    requested, root = ensure_repo(repo)
    head = git(root, "rev-parse", "HEAD").stdout.strip()
    shallow_probe = git(root, "rev-parse", "--is-shallow-repository", check=False)
    shallow = shallow_probe.returncode == 0 and shallow_probe.stdout.strip() == "true"
    dirty, fingerprint = dirty_fingerprint(root)
    count_probe = git(root, "rev-list", "--count", "HEAD", check=False)
    commit_count = int(count_probe.stdout.strip()) if count_probe.returncode == 0 else 0
    return {
        "repository_id": repository_id(root),
        "requested_path": str(requested),
        "repository_root": str(root),
        "repository_head": head,
        "dirty": dirty,
        "working_tree_fingerprint": fingerprint,
        "shallow": shallow,
        "commit_count": commit_count,
    }


MANIFESTS: dict[str, tuple[str, ...]] = {
    "python": ("pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", "Pipfile"),
    "javascript-typescript": ("package.json", "deno.json", "deno.jsonc"),
    "java-kotlin": ("pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"),
    "go": ("go.mod",),
    "rust": ("Cargo.toml",),
    "dotnet": ("*.sln", "*.csproj", "*.fsproj"),
    "ruby": ("Gemfile", "*.gemspec"),
    "php": ("composer.json",),
    "c-cpp": ("CMakeLists.txt", "meson.build", "Makefile"),
    "swift": ("Package.swift",),
}

EXTENSIONS = {
    ".py": "python",
    ".js": "javascript-typescript",
    ".jsx": "javascript-typescript",
    ".ts": "javascript-typescript",
    ".tsx": "javascript-typescript",
    ".java": "java-kotlin",
    ".kt": "java-kotlin",
    ".kts": "java-kotlin",
    ".go": "go",
    ".rs": "rust",
    ".cs": "dotnet",
    ".fs": "dotnet",
    ".rb": "ruby",
    ".php": "php",
    ".c": "c-cpp",
    ".h": "c-cpp",
    ".cc": "c-cpp",
    ".cpp": "c-cpp",
    ".swift": "swift",
}

TOOL_CAPABILITIES: dict[str, tuple[str, ...]] = {
    "version-control": ("git",),
    "fast-text-search": ("rg", "grep"),
    "python-native": ("ruff", "pytest", "coverage", "radon", "import-linter"),
    "javascript-typescript-native": ("eslint", "tsc", "vitest", "jest", "dependency-cruiser", "madge"),
    "java-kotlin-native": ("jdeps", "mvn", "gradle"),
    "go-native": ("go", "golangci-lint"),
    "rust-native": ("cargo", "rustc"),
    "dotnet-native": ("dotnet",),
    "c-cpp-native": ("clang", "clang-scan-deps", "cmake"),
}


def discover(repo: str) -> dict[str, Any]:
    root = Path(repo).resolve()
    if not root.exists():
        raise CBIError(f"path does not exist: {root}")
    counts: dict[str, int] = {}
    ignored = {".git", "node_modules", "vendor", "dist", "build", "target", ".venv", "venv"}
    manifests: dict[str, list[str]] = {}
    for directory, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in ignored)
        for name in sorted(files):
            ecosystem = EXTENSIONS.get(Path(name).suffix.lower())
            if ecosystem:
                counts[ecosystem] = counts.get(ecosystem, 0) + 1
            for manifest_ecosystem, patterns in MANIFESTS.items():
                if any(fnmatch.fnmatch(name, pattern) for pattern in patterns):
                    relative = (Path(directory) / name).relative_to(root).as_posix()
                    manifests.setdefault(manifest_ecosystem, []).append(relative)
    manifests = {name: sorted(set(paths)) for name, paths in manifests.items()}
    ecosystems = sorted(set(counts) | set(manifests))
    tool_names = sorted({name for names in TOOL_CAPABILITIES.values() for name in names})
    tools = {name: shutil.which(name) for name in tool_names}
    return {
        "repository": str(root),
        "ecosystems": ecosystems,
        "source_file_counts": dict(sorted(counts.items())),
        "manifests": manifests,
        "tools": {name: value for name, value in tools.items() if value},
        "missing_tools": [name for name, value in tools.items() if not value],
        "note": "Availability is observational; inspect project configuration before selecting or proposing a provider.",
    }


def parse_git_history(root: Path, since: str | None, max_commits: int | None) -> list[dict[str, Any]]:
    command = [
        "git",
        "-c",
        "core.quotePath=false",
        "log",
        "--no-renames",
        "--numstat",
        "--format=__CBI_COMMIT__%H%x09%aN",
    ]
    if since:
        command.append(f"--since={since}")
    if max_commits:
        command.append(f"--max-count={max_commits}")
    output = run(command, root).stdout
    commits: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in output.splitlines():
        if line.startswith("__CBI_COMMIT__"):
            if current is not None:
                commits.append(current)
            header = line[len("__CBI_COMMIT__"):].split("\t", 1)
            current = {"commit": header[0], "author": header[1] if len(header) > 1 else "", "files": {}}
            continue
        if not line or current is None:
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        added, deleted, path = parts
        current["files"][path] = {
            "added": None if added == "-" else int(added),
            "deleted": None if deleted == "-" else int(deleted),
        }
    if current is not None:
        commits.append(current)
    return commits


def provenance(meta: dict[str, Any], provider: str, provider_version: str, parameters: dict[str, Any], scope: str) -> dict[str, Any]:
    return {
        "provider": provider,
        "provider_version": provider_version,
        "analyzer_version": ANALYZER_VERSION,
        "repository_id": meta["repository_id"],
        "repository_head": meta["repository_head"],
        "dirty": meta["dirty"],
        "working_tree_fingerprint": meta["working_tree_fingerprint"],
        "shallow": meta["shallow"],
        "input_scope": scope,
        "parameters": parameters,
        "generated_at": utc_now(),
    }


def history_parameters(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "since": args.since,
        "max_commits": args.max_commits,
        "max_changeset_size": args.max_changeset_size,
        "min_shared_commits": args.min_shared_commits,
        "loc_definition": LOC_DEFINITION_VERSION,
        "loc_ignored_path_parts": sorted(IGNORED_PATH_PARTS),
    }


def relevant_repository_path(path: str) -> bool:
    """Keep the fallback language-neutral while removing obvious noise."""
    parts = PurePosixPath(path).parts
    lowered = {part.lower() for part in parts}
    name = parts[-1].lower() if parts else ""
    return not lowered & IGNORED_PATH_PARTS and not name.endswith((".min.js", ".map"))


def tracked_loc(root: Path) -> dict[str, int]:
    """Count physical text lines in current tracked files, deterministically.

    A line is each record returned by bytes.splitlines(); blank lines count and
    a final newline does not create an extra line. Binary files and obvious
    generated/vendor/build/cache paths are excluded.
    """
    output = git(root, "ls-files", "-z").stdout
    result: dict[str, int] = {}
    for raw_path in filter(None, output.split("\0")):
        path = raw_path.replace("\\", "/")
        if not relevant_repository_path(path):
            continue
        candidate = root / path
        try:
            content = candidate.read_bytes()
        except OSError:
            continue
        if b"\0" in content:
            continue
        result[path] = len(content.splitlines())
    return result


def descending_rank(value: float, values: list[float]) -> float:
    """Return a deterministic 0..1 rank, with the largest value at 1."""
    if len(values) <= 1:
        return 1.0
    ordered = sorted(values)
    return ordered.index(value) / (len(ordered) - 1)


def rank_hotspots(store: dict[str, Any], limit: int | None = 20) -> dict[str, Any]:
    """Rank candidates without turning a metric into a semantic conclusion.

    Git fallback: revision frequency x current physical LOC. Code Maat:
    provider revisions x provider absolute entity churn. Each axis is ranked
    within the candidate set before multiplication, so one huge but rarely
    changed file cannot dominate by size alone.
    """
    errors = validate_store(store)
    if errors:
        raise CBIError("invalid evidence store: " + "; ".join(errors))
    by_path: dict[str, dict[str, dict[str, Any]]] = {}
    for item in store["observations"]:
        subject = item["subject"]
        if subject.get("type") != "file":
            continue
        path = subject["path"]
        by_path.setdefault(path, {})[item["type"]] = item
    provider = store["provenance"]["provider"]
    size_type = "complexity" if provider == HISTORY_PROVIDER else "churn"
    size_metric = "loc" if size_type == "complexity" else "absolute_churn"
    candidates = []
    for path, observations in by_path.items():
        frequency = observations.get("change_frequency")
        size = observations.get(size_type)
        if not frequency or not size:
            continue
        revisions = frequency["metrics"].get("revisions")
        size_value = size["metrics"].get(size_metric)
        if not isinstance(revisions, (int, float)) or not isinstance(size_value, (int, float)):
            continue
        candidates.append({"path": path, "revisions": revisions, size_metric: size_value})
    revision_values = [float(item["revisions"]) for item in candidates]
    size_values = [float(item[size_metric]) for item in candidates]
    for item in candidates:
        item["revision_rank"] = descending_rank(float(item["revisions"]), revision_values)
        item["size_rank"] = descending_rank(float(item[size_metric]), size_values)
        item["hotspot_score"] = item["revision_rank"] * item["size_rank"]
    candidates.sort(key=lambda item: (-item["hotspot_score"], -item["revisions"], -item[size_metric], item["path"]))
    if limit is not None:
        candidates = candidates[:limit]
    definition = (
        "descending percentile rank of commits touching file multiplied by "
        "descending percentile rank of current physical LOC"
        if provider == HISTORY_PROVIDER else
        "descending percentile rank of provider revisions multiplied by "
        "descending percentile rank of provider absolute entity churn"
    )
    return {"provider": provider, "metric_definition": definition, "count": len(candidates), "candidates": candidates}


def code_maat_parameters(input_path: str, analysis: str) -> dict[str, Any]:
    resolved = Path(input_path).resolve()
    try:
        input_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()
    except OSError as exc:
        raise CBIError(f"cannot read Code Maat CSV: {exc}") from exc
    return {"analysis": analysis, "input_sha256": input_hash}


def code_maat_hotspot_parameters(revisions_input: str, churn_input: str) -> dict[str, Any]:
    return {
        "analysis": "hotspots",
        "revisions_input_sha256": code_maat_parameters(revisions_input, "revisions")["input_sha256"],
        "entity_churn_input_sha256": code_maat_parameters(churn_input, "entity-churn")["input_sha256"],
    }


def observation(kind: str, subject: dict[str, Any], metrics: dict[str, Any], prov: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "type": kind,
        "subject": subject,
        "metrics": metrics,
        "provenance": prov,
    }


def analyze_history(args: argparse.Namespace) -> dict[str, Any]:
    _, root = ensure_repo(args.repo)
    meta = repo_metadata(str(root))
    parameters = history_parameters(args)
    commits = parse_git_history(root, args.since, args.max_commits)
    loc_by_file = tracked_loc(root)
    per_file: dict[str, dict[str, Any]] = {}
    pair_shared: dict[tuple[str, str], int] = {}
    for item in commits:
        paths = sorted(path for path in item["files"] if relevant_repository_path(path))
        for path in paths:
            stats = per_file.setdefault(path, {"revisions": 0, "added": 0, "deleted": 0, "binary_revisions": 0, "authors": {}})
            stats["revisions"] += 1
            changes = item["files"][path]
            if changes["added"] is None or changes["deleted"] is None:
                stats["binary_revisions"] += 1
            else:
                stats["added"] += changes["added"]
                stats["deleted"] += changes["deleted"]
            author = item["author"] or "<unknown>"
            stats["authors"][author] = stats["authors"].get(author, 0) + 1
        if len(paths) <= args.max_changeset_size:
            for pair in combinations(paths, 2):
                pair_shared[pair] = pair_shared.get(pair, 0) + 1

    prov = provenance(meta, HISTORY_PROVIDER, ANALYZER_VERSION, parameters, "committed_history+working_tree")
    observations: list[dict[str, Any]] = []
    for path in sorted(per_file):
        if not relevant_repository_path(path):
            continue
        stats = per_file[path]
        subject = {"type": "file", "path": path}
        observations.append(observation("change_frequency", subject, {"revisions": stats["revisions"], "unit": "commits_touching_file"}, prov))
        observations.append(observation("churn", subject, {
            "lines_added": stats["added"],
            "lines_deleted": stats["deleted"],
            "absolute_churn": stats["added"] + stats["deleted"],
            "binary_revisions_excluded": stats["binary_revisions"],
            "unit": "lines",
        }, prov))
        author_rows = sorted(stats["authors"].items(), key=lambda row: (-row[1], row[0]))
        primary_name, primary_revisions = author_rows[0]
        observations.append(observation("ownership", subject, {
            "authors": len(author_rows),
            "primary_author": primary_name,
            "primary_author_revisions": primary_revisions,
            "primary_share": primary_revisions / stats["revisions"],
            "revisions_by_author": dict(author_rows),
            "metric_definition": "commit touches attributed to Git author name",
        }, prov))
        if path in loc_by_file:
            observations.append(observation("complexity", subject, {
                "loc": loc_by_file[path],
                "unit": "physical_lines",
                "metric_definition": "current tracked text-line count; blank lines count",
                "proxy": "language-agnostic size/complexity proxy",
            }, prov))
    for (left, right), shared in sorted(pair_shared.items()):
        if shared < args.min_shared_commits:
            continue
        left_revs = per_file[left]["revisions"]
        right_revs = per_file[right]["revisions"]
        coupling = shared / min(left_revs, right_revs)
        observations.append(observation("temporal_coupling", {"type": "file_pair", "paths": [left, right]}, {
            "shared_commits": shared,
            "left_revisions": left_revs,
            "right_revisions": right_revs,
            "coupling": coupling,
            "range": [0, 1],
            "metric_definition": "shared_commits / min(left_revisions, right_revisions)",
            "excluded_large_changesets_over": args.max_changeset_size,
        }, prov))
    limitations = []
    if meta["shallow"]:
        limitations.append("Git history is shallow; historical observations cover only available commits.")
    if len(commits) < 2:
        limitations.append("Fewer than two commits matched; historical patterns are insufficient for trend interpretation.")
    store = {
        "schema_version": SCHEMA_VERSION,
        "store_kind": "codebase-intelligence-evidence",
        "provenance": prov,
        "repository": meta,
        "limitations": limitations,
        "observations": observations,
    }
    errors = validate_store(store)
    if errors:
        raise CBIError("generated invalid Git evidence: " + "; ".join(errors))
    return store


def load_json(path: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise CBIError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise CBIError(f"invalid JSON in {path}: {exc}") from exc


def write_json(data: Any, path: str | None) -> None:
    rendered = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def valid_repository_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\x00" in value or "\\" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or path == PurePosixPath(".") or ".." in path.parts:
        return False
    return path.as_posix() == value


def provenance_errors(value: Any, prefix: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{prefix} must be an object"]
    required = {
        "provider", "provider_version", "analyzer_version", "repository_id",
        "repository_head", "dirty", "working_tree_fingerprint", "shallow",
        "parameters", "input_scope", "generated_at",
    }
    missing = sorted(required - set(value))
    errors = [f"{prefix} missing: {', '.join(missing)}"] if missing else []
    for field in (
        "provider", "provider_version", "analyzer_version", "repository_id",
        "repository_head", "working_tree_fingerprint", "input_scope", "generated_at",
    ):
        if field in value and (not isinstance(value[field], str) or not value[field]):
            errors.append(f"{prefix}.{field} must be a non-empty string")
    for field in ("dirty", "shallow"):
        if field in value and not isinstance(value[field], bool):
            errors.append(f"{prefix}.{field} must be a boolean")
    if "parameters" in value and not isinstance(value["parameters"], dict):
        errors.append(f"{prefix}.parameters must be an object")
    return errors


def validate_observation(item: Any, index: int, store_provenance: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    prefix = f"observations[{index}]"
    if not isinstance(item, dict):
        return [f"{prefix} must be an object"]
    if item.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{prefix}.schema_version must equal {SCHEMA_VERSION}")
    if item.get("type") not in EVIDENCE_TYPES:
        errors.append(f"{prefix}.type is unsupported: {item.get('type')!r}")
    subject = item.get("subject")
    if not isinstance(subject, dict) or subject.get("type") not in SUBJECT_TYPES:
        errors.append(f"{prefix}.subject must contain a supported type")
    elif subject["type"] == "file":
        if not valid_repository_path(subject.get("path")):
            errors.append(f"{prefix}.subject.path must be a normalized repository-relative path")
    elif subject["type"] in {"directory", "symbol"}:
        if "path" in subject and not valid_repository_path(subject.get("path")):
            errors.append(f"{prefix}.subject.path must be a normalized repository-relative path")
        if not any(key in subject for key in ("path", "name")):
            errors.append(f"{prefix}.subject lacks path/name")
    elif subject["type"] == "component" and (not isinstance(subject.get("name"), str) or not subject["name"]):
        errors.append(f"{prefix}.subject.name must be a non-empty string")
    elif subject["type"] == "file_pair":
        values = subject.get("paths")
        if not isinstance(values, list) or len(values) != 2:
            errors.append(f"{prefix}.subject.paths must identify exactly two files")
        elif any(not valid_repository_path(value) for value in values):
            errors.append(f"{prefix}.subject.paths must contain normalized repository-relative paths")
    elif subject["type"] == "component_pair":
        values = subject.get("names")
        if not isinstance(values, list) or len(values) != 2 or any(not isinstance(value, str) or not value for value in values):
            errors.append(f"{prefix}.subject.names must identify exactly two components")
    if not isinstance(item.get("metrics"), dict):
        errors.append(f"{prefix}.metrics must be an object")
    prov = item.get("provenance")
    errors.extend(provenance_errors(prov, f"{prefix}.provenance"))
    if isinstance(prov, dict) and store_provenance is not None and prov != store_provenance:
        errors.append(f"{prefix}.provenance must exactly match store provenance")
    return errors


def validate_store(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["store must be an object"]
    errors: list[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must equal {SCHEMA_VERSION}")
    if data.get("store_kind") != "codebase-intelligence-evidence":
        errors.append("store_kind must be codebase-intelligence-evidence")
    store_provenance = data.get("provenance")
    errors.extend(provenance_errors(store_provenance, "provenance"))
    repository = data.get("repository")
    if not isinstance(repository, dict):
        errors.append("repository must be an object")
    elif isinstance(store_provenance, dict):
        for repository_field, provenance_field in (
            ("repository_id", "repository_id"),
            ("repository_head", "repository_head"),
            ("dirty", "dirty"),
            ("working_tree_fingerprint", "working_tree_fingerprint"),
            ("shallow", "shallow"),
        ):
            if repository.get(repository_field) != store_provenance.get(provenance_field):
                errors.append(f"repository.{repository_field} must match provenance.{provenance_field}")
    items = data.get("observations")
    if not isinstance(items, list):
        errors.append("observations must be an array")
        return errors
    for index, item in enumerate(items):
        errors.extend(validate_observation(item, index, store_provenance if isinstance(store_provenance, dict) else None))
    return errors


def expected_cache_provenance(args: argparse.Namespace) -> dict[str, Any]:
    if args.provider == "git":
        return {
            "provider": HISTORY_PROVIDER,
            "provider_version": ANALYZER_VERSION,
            "parameters": history_parameters(args),
            "input_scope": "committed_history+working_tree",
        }
    if args.provider == "code-maat":
        if not args.provider_version:
            raise CBIError("--provider-version is required for Code Maat cache validation")
        if not args.maat_analysis or not args.input:
            raise CBIError("--maat-analysis and --input are required for Code Maat cache validation")
        if args.maat_analysis == "hotspots" and not getattr(args, "churn_input", None):
            raise CBIError("--churn-input is required for Code Maat hotspot cache validation")
        return {
            "provider": "code-maat",
            "provider_version": args.provider_version,
            "parameters": code_maat_hotspot_parameters(args.input, args.churn_input) if args.maat_analysis == "hotspots" else code_maat_parameters(args.input, args.maat_analysis),
            "input_scope": "committed_history",
        }
    raise CBIError(f"unsupported cache provider: {args.provider}")


def cache_status(args: argparse.Namespace) -> dict[str, Any]:
    data = load_json(args.store)
    errors = validate_store(data)
    if errors:
        return {"valid": False, "reasons": errors}
    try:
        meta = repo_metadata(args.repo)
    except CBIError as exc:
        return {"valid": False, "reasons": [str(exc)]}
    prov = data["provenance"]
    try:
        expected_analysis = expected_cache_provenance(args)
    except CBIError as exc:
        return {"valid": False, "reasons": [str(exc)]}
    reasons: list[str] = []
    expected = {
        "repository_id": meta["repository_id"],
        "repository_head": meta["repository_head"],
        "analyzer_version": ANALYZER_VERSION,
        **expected_analysis,
    }
    for field, value in expected.items():
        if prov.get(field) != value:
            reasons.append(f"{field} changed")
    scope = prov.get("input_scope")
    if scope != "committed_history":
        if prov.get("dirty") != meta["dirty"] or prov.get("working_tree_fingerprint") != meta["working_tree_fingerprint"]:
            reasons.append("working tree inputs changed")
    return {"valid": not reasons, "reasons": reasons, "input_scope": scope}


def subject_text(subject: dict[str, Any]) -> str:
    return " ".join(str(value) for key, value in sorted(subject.items()) if key != "type")


def query_store(args: argparse.Namespace) -> dict[str, Any]:
    data = load_json(args.store)
    errors = validate_store(data)
    if errors:
        raise CBIError("invalid evidence store: " + "; ".join(errors))
    items = data["observations"]
    if args.type:
        items = [item for item in items if item["type"] in set(args.type)]
    if args.subject:
        needle = args.subject.lower()
        items = [item for item in items if needle in subject_text(item["subject"]).lower()]
    if args.metric:
        filtered = []
        for item in items:
            value = item["metrics"].get(args.metric)
            if isinstance(value, (int, float)) and (args.min is None or value >= args.min):
                filtered.append(item)
        items = filtered
        items.sort(key=lambda item: (-float(item["metrics"][args.metric]), subject_text(item["subject"])))
    if args.limit is not None:
        items = items[: args.limit]
    return {"schema_version": SCHEMA_VERSION, "count": len(items), "observations": items}


def maat_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    return maat_rows_for(args.input)


def maat_rows_for(input_path: str) -> list[dict[str, str]]:
    try:
        with Path(input_path).open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                raise CBIError("Code Maat CSV has no header")
            return list(reader)
    except OSError as exc:
        raise CBIError(f"cannot read Code Maat CSV: {exc}") from exc


def need(row: dict[str, str], names: Iterable[str], row_number: int) -> str:
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name].strip()
    raise CBIError(f"malformed Code Maat row {row_number}: expected one of {', '.join(names)}")


def adapt_code_maat(args: argparse.Namespace) -> dict[str, Any]:
    _, root = ensure_repo(args.repo)
    meta = repo_metadata(str(root))
    if args.analysis == "hotspots" and not getattr(args, "churn_input", None):
        raise CBIError("--churn-input is required for Code Maat hotspot adaptation")
    params = code_maat_hotspot_parameters(args.input, args.churn_input) if args.analysis == "hotspots" else code_maat_parameters(args.input, args.analysis)
    prov = provenance(meta, "code-maat", args.provider_version, params, "committed_history")
    observations: list[dict[str, Any]] = []
    if args.analysis == "hotspots":
        revisions = {
            need(row, ("entity", "module"), row_number): int(need(row, ("n-revs", "revisions"), row_number))
            for row_number, row in enumerate(maat_rows(args), start=2)
        }
        churn_rows = {
            need(row, ("entity", "module"), row_number): row
            for row_number, row in enumerate(maat_rows_for(args.churn_input), start=2)
        }
        if set(revisions) != set(churn_rows):
            raise CBIError("Code Maat hotspot inputs must contain the same entities")
        for path in sorted(revisions):
            row = churn_rows[path]
            added = int(need(row, ("added",), 0))
            deleted = int(need(row, ("deleted",), 0))
            observations.extend((
                observation("change_frequency", {"type": "file", "path": path}, {
                    "revisions": revisions[path], "unit": "Code Maat revisions",
                    "metric_definition": "provider-defined Code Maat revisions",
                }, prov),
                observation("churn", {"type": "file", "path": path}, {
                    "lines_added": added, "lines_deleted": deleted,
                    "absolute_churn": added + deleted, "unit": "lines",
                    "metric_definition": "Code Maat entity-churn absolute line counts",
                }, prov),
            ))
    else:
        for row_number, row in enumerate(maat_rows(args), start=2):
            if args.analysis == "revisions":
                path = need(row, ("entity", "module"), row_number)
                revisions = int(need(row, ("n-revs", "revisions"), row_number))
                observations.append(observation("change_frequency", {"type": "file", "path": path}, {
                    "revisions": revisions,
                    "unit": "Code Maat revisions",
                    "metric_definition": "provider-defined Code Maat revisions",
                }, prov))
            elif args.analysis == "entity-churn":
                path = need(row, ("entity", "module"), row_number)
                added = int(need(row, ("added",), row_number))
                deleted = int(need(row, ("deleted",), row_number))
                observations.append(observation("churn", {"type": "file", "path": path}, {
                    "lines_added": added,
                    "lines_deleted": deleted,
                    "absolute_churn": added + deleted,
                    "unit": "lines",
                    "metric_definition": "Code Maat entity-churn absolute line counts",
                }, prov))
            elif args.analysis == "authors":
                path = need(row, ("entity", "module"), row_number)
                authors = int(need(row, ("n-authors", "authors"), row_number))
                revisions = int(need(row, ("n-revs", "revisions"), row_number))
                observations.append(observation("ownership", {"type": "file", "path": path}, {
                    "authors": authors,
                    "revisions": revisions,
                    "metric_definition": "Code Maat distinct authors and revisions",
                }, prov))
            elif args.analysis == "coupling":
                left = need(row, ("entity",), row_number)
                right = need(row, ("coupled",), row_number)
                degree = float(need(row, ("degree",), row_number))
                metrics: dict[str, Any] = {
                    "coupling": degree,
                    "range": [0, 100],
                    "unit": "percent",
                    "metric_definition": "Code Maat coupling degree; provider semantics preserved",
                }
                if row.get("average-revs"):
                    metrics["average_revisions"] = float(row["average-revs"])
                for source, destination in (("shared-revisions", "shared_revisions"), ("entity-revisions", "left_revisions"), ("coupled-revisions", "right_revisions")):
                    if row.get(source):
                        metrics[destination] = int(row[source])
                observations.append(observation("temporal_coupling", {"type": "file_pair", "paths": [left, right]}, metrics, prov))
    store = {
        "schema_version": SCHEMA_VERSION,
        "store_kind": "codebase-intelligence-evidence",
        "provenance": prov,
        "repository": meta,
        "limitations": [],
        "observations": observations,
    }
    errors = validate_store(store)
    if errors:
        raise CBIError("generated invalid Code Maat evidence: " + "; ".join(errors))
    return store


def verify_references(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.repo).resolve()
    references = load_json(args.references)
    if not isinstance(references, list):
        raise CBIError("references file must contain a JSON array")
    results = []
    for index, ref in enumerate(references):
        if not isinstance(ref, dict) or not isinstance(ref.get("path"), str):
            raise CBIError(f"reference {index} must contain a string path")
        path = ref["path"]
        candidate = (root / path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            results.append({**ref, "status": "CONTRADICTED", "reason": "path escapes repository root"})
            continue
        if not candidate.is_file():
            results.append({**ref, "status": "CONTRADICTED", "reason": "file does not exist"})
            continue
        symbol = ref.get("symbol")
        if symbol:
            content = candidate.read_text(encoding="utf-8", errors="replace")
            pattern = re.compile(rf"(?<![\w$]){re.escape(str(symbol))}(?![\w$])")
            matches = [line_no for line_no, line in enumerate(content.splitlines(), 1) if pattern.search(line)]
            if not matches:
                results.append({**ref, "status": "CONTRADICTED", "reason": "symbol text not found"})
                continue
            results.append({**ref, "status": "VERIFIED", "matching_lines": matches[:20], "check": "lexical symbol occurrence"})
        else:
            results.append({**ref, "status": "VERIFIED", "check": "file existence"})
    return {"repository": str(root), "results": results}


def default_store(args: argparse.Namespace) -> dict[str, str]:
    meta = repo_metadata(args.repo)
    path = Path(os.environ.get("TMPDIR", "/tmp")) / "codebase-intelligence" / meta["repository_id"] / "evidence-v1.json"
    return {"path": str(path), "storage": "ephemeral machine-local cache"}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--version", action="version", version=ANALYZER_VERSION)
    sub = result.add_subparsers(dest="command", required=True)

    command = sub.add_parser("repo-meta", help="print Git repository provenance")
    command.add_argument("--repo", default=".")

    command = sub.add_parser("discover", help="detect ecosystems, manifests, and available tools")
    command.add_argument("--repo", default=".")

    command = sub.add_parser("default-store", help="print an ephemeral evidence-store path")
    command.add_argument("--repo", default=".")

    command = sub.add_parser("analyze-history", help="produce normalized Git-history evidence")
    command.add_argument("--repo", default=".")
    command.add_argument("--output")
    command.add_argument("--since")
    command.add_argument("--max-commits", type=int)
    command.add_argument("--max-changeset-size", type=int, default=30)
    command.add_argument("--min-shared-commits", type=int, default=2)

    command = sub.add_parser("validate", help="validate an evidence store")
    command.add_argument("--store", required=True)

    command = sub.add_parser("cache-status", help="validate evidence provenance against current inputs")
    command.add_argument("--repo", default=".")
    command.add_argument("--store", required=True)
    command.add_argument("--provider", required=True, choices=("git", "code-maat"))
    command.add_argument("--provider-version")
    command.add_argument("--since")
    command.add_argument("--max-commits", type=int)
    command.add_argument("--max-changeset-size", type=int, default=30)
    command.add_argument("--min-shared-commits", type=int, default=2)
    command.add_argument("--maat-analysis", choices=("revisions", "entity-churn", "authors", "coupling", "hotspots"))
    command.add_argument("--input", help="current Code Maat CSV input")
    command.add_argument("--churn-input", help="current Code Maat entity-churn CSV for hotspot cache validation")

    command = sub.add_parser("query", help="filter and rank evidence without dumping the full store")
    command.add_argument("--store", required=True)
    command.add_argument("--type", action="append", choices=sorted(EVIDENCE_TYPES))
    command.add_argument("--subject")
    command.add_argument("--metric")
    command.add_argument("--min", type=float)
    command.add_argument("--limit", type=int, default=20)

    command = sub.add_parser("rank-hotspots", help="rank bounded hotspot candidates from normalized evidence")
    command.add_argument("--store", required=True)
    command.add_argument("--limit", type=int, default=20)

    command = sub.add_parser("adapt-code-maat", help="normalize a Code Maat CSV")
    command.add_argument("--repo", default=".")
    command.add_argument("--input", required=True)
    command.add_argument("--output")
    command.add_argument("--analysis", required=True, choices=("revisions", "entity-churn", "authors", "coupling", "hotspots"))
    command.add_argument("--churn-input", help="Code Maat entity-churn CSV for hotspot adaptation")
    command.add_argument("--provider-version", required=True)

    command = sub.add_parser("verify-references", help="verify repository-relative paths and lexical symbols")
    command.add_argument("--repo", default=".")
    command.add_argument("--references", required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "repo-meta":
            data = repo_metadata(args.repo)
        elif args.command == "discover":
            data = discover(args.repo)
        elif args.command == "default-store":
            data = default_store(args)
        elif args.command == "analyze-history":
            data = analyze_history(args)
            write_json(data, args.output)
            return 0
        elif args.command == "validate":
            errors = validate_store(load_json(args.store))
            data = {"valid": not errors, "errors": errors}
            write_json(data, None)
            return 0 if not errors else 1
        elif args.command == "cache-status":
            data = cache_status(args)
            write_json(data, None)
            return 0 if data["valid"] else 1
        elif args.command == "query":
            data = query_store(args)
        elif args.command == "rank-hotspots":
            data = rank_hotspots(load_json(args.store), args.limit)
        elif args.command == "adapt-code-maat":
            data = adapt_code_maat(args)
            write_json(data, args.output)
            return 0
        elif args.command == "verify-references":
            data = verify_references(args)
        else:
            raise CBIError(f"unsupported command: {args.command}")
        write_json(data, None)
        return 0
    except (CBIError, ValueError) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
