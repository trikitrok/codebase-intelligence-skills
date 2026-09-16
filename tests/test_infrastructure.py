from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "shared" / "scripts" / "codebase_intelligence.py"
SPEC = importlib.util.spec_from_file_location("cbi", HELPER)
assert SPEC and SPEC.loader
cbi = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cbi)


class RepositoryFixture:
    def __init__(self, root: Path):
        self.root = root
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture Author")
        self.git("config", "user.email", "fixture@example.test")

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.strip()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def commit(self, message: str) -> None:
        self.git("add", ".")
        self.git("commit", "-q", "-m", message)


class InfrastructureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "tests")
        self.base = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_repo(self) -> RepositoryFixture:
        root = self.base / "repo"
        root.mkdir()
        repo = RepositoryFixture(root)
        repo.write("src/a.py", "def alpha():\n    return 1\n")
        repo.write("src/b.py", "def beta():\n    return 1\n")
        repo.commit("initial")
        repo.write("src/a.py", "def alpha():\n    return 2\n")
        repo.write("src/b.py", "def beta():\n    return 2\n")
        repo.commit("change pair")
        return repo

    def history_args(self, repo: Path, **overrides: object) -> argparse.Namespace:
        values = {
            "repo": str(repo), "since": None, "max_commits": None,
            "max_changeset_size": 30, "min_shared_commits": 2,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def cache_args(self, repo: Path, store: Path, provider: str = "git", **overrides: object) -> argparse.Namespace:
        values = {
            "repo": str(repo), "store": str(store), "provider": provider,
            "provider_version": None, "since": None, "max_commits": None,
            "max_changeset_size": 30, "min_shared_commits": 2,
            "maat_analysis": None, "input": None,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def write_store(self, store: dict[str, object]) -> Path:
        path = self.base / "store.json"
        path.write_text(json.dumps(store), encoding="utf-8")
        return path

    def test_git_history_produces_normalized_observations(self) -> None:
        repo = self.make_repo()
        store = cbi.analyze_history(self.history_args(repo.root))
        self.assertEqual([], cbi.validate_store(store))
        types = {item["type"] for item in store["observations"]}
        self.assertTrue({"change_frequency", "churn", "ownership", "temporal_coupling"} <= types)
        coupling = next(item for item in store["observations"] if item["type"] == "temporal_coupling")
        self.assertEqual(2, coupling["metrics"]["shared_commits"])
        self.assertEqual(1.0, coupling["metrics"]["coupling"])
        self.assertIn("metric_definition", coupling["metrics"])

    def test_committed_history_cache_survives_dirty_tree_but_not_new_head(self) -> None:
        repo = self.make_repo()
        store = cbi.analyze_history(self.history_args(repo.root))
        store_path = self.write_store(store)
        repo.write("src/a.py", "dirty\n")
        args = self.cache_args(repo.root, store_path)
        self.assertTrue(cbi.cache_status(args)["valid"])
        repo.commit("new head")
        status = cbi.cache_status(args)
        self.assertFalse(status["valid"])
        self.assertIn("repository_head changed", status["reasons"])

    def test_normal_cache_workflow_requires_and_checks_analysis_parameters(self) -> None:
        repo = self.make_repo()
        store = cbi.analyze_history(self.history_args(repo.root, max_changeset_size=7))
        store_path = self.write_store(store)

        command = [
            "python3", str(HELPER), "cache-status", "--repo", str(repo.root),
            "--store", str(store_path), "--provider", "git",
        ]
        mismatch = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(1, mismatch.returncode)
        self.assertIn("parameters changed", json.loads(mismatch.stdout)["reasons"])

        match = subprocess.run(command + ["--max-changeset-size", "7"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(0, match.returncode)
        self.assertTrue(json.loads(match.stdout)["valid"])

        missing_request = subprocess.run(
            ["python3", str(HELPER), "cache-status", "--repo", str(repo.root), "--store", str(store_path)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.assertEqual(2, missing_request.returncode)
        self.assertIn("--provider", missing_request.stderr)

    def test_cache_invalidates_analyzer_and_schema(self) -> None:
        repo = self.make_repo()
        store = cbi.analyze_history(self.history_args(repo.root))
        store_path = self.write_store(store)
        changed = self.cache_args(repo.root, store_path)
        store["provenance"]["analyzer_version"] = "0.0.0"
        for item in store["observations"]:
            item["provenance"]["analyzer_version"] = "0.0.0"
        store_path.write_text(json.dumps(store), encoding="utf-8")
        self.assertIn("analyzer_version changed", cbi.cache_status(changed)["reasons"])
        store = cbi.analyze_history(self.history_args(repo.root))
        store_path.write_text(json.dumps(store), encoding="utf-8")
        store["schema_version"] = 2
        store_path.write_text(json.dumps(store), encoding="utf-8")
        self.assertFalse(cbi.cache_status(changed)["valid"])

    def test_external_provider_version_is_current_request_not_cached_value(self) -> None:
        repo = self.make_repo()
        csv_path = self.base / "coupling.csv"
        csv_path.write_text("entity,coupled,degree,average-revs\nsrc/a.py,src/b.py,75,4\n", encoding="utf-8")
        store = cbi.adapt_code_maat(argparse.Namespace(
            repo=str(repo.root), input=str(csv_path), analysis="coupling", provider_version="X",
        ))
        store_path = self.write_store(store)
        command = [
            "python3", str(HELPER), "cache-status", "--repo", str(repo.root),
            "--store", str(store_path), "--provider", "code-maat",
            "--maat-analysis", "coupling", "--input", str(csv_path),
        ]
        mismatch = subprocess.run(
            command + ["--provider-version", "Y"], text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.assertEqual(1, mismatch.returncode)
        self.assertIn("provider_version changed", json.loads(mismatch.stdout)["reasons"])
        match = subprocess.run(
            command + ["--provider-version", "X"], text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.assertEqual(0, match.returncode)
        missing = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(1, missing.returncode)
        self.assertIn("provider-version is required", json.loads(missing.stdout)["reasons"][0])

    def test_external_provider_input_and_analysis_invalidate_reuse(self) -> None:
        repo = self.make_repo()
        csv_path = self.base / "revisions.csv"
        csv_path.write_text("entity,n-revs\nsrc/a.py,2\n", encoding="utf-8")
        store = cbi.adapt_code_maat(argparse.Namespace(
            repo=str(repo.root), input=str(csv_path), analysis="revisions", provider_version="X",
        ))
        store_path = self.write_store(store)
        args = self.cache_args(
            repo.root, store_path, provider="code-maat", provider_version="X",
            maat_analysis="revisions", input=str(csv_path),
        )
        csv_path.write_text("entity,n-revs\nsrc/a.py,3\n", encoding="utf-8")
        self.assertIn("parameters changed", cbi.cache_status(args)["reasons"])
        args.maat_analysis = "authors"
        self.assertIn("parameters changed", cbi.cache_status(args)["reasons"])

    def test_store_rejects_observation_provenance_inconsistent_with_store(self) -> None:
        repo = self.make_repo()
        original = cbi.analyze_history(self.history_args(repo.root))
        for field, value in (
            ("repository_id", "other"), ("repository_head", "other"),
            ("provider", "other"), ("provider_version", "other"),
            ("analyzer_version", "other"), ("dirty", not original["provenance"]["dirty"]),
            ("working_tree_fingerprint", "other"), ("shallow", not original["provenance"]["shallow"]),
            ("parameters", {"other": True}), ("input_scope", "working_tree"),
            ("generated_at", "2000-01-01T00:00:00+00:00"),
        ):
            with self.subTest(field=field):
                corrupted = json.loads(json.dumps(original))
                corrupted["observations"][0]["provenance"][field] = value
                errors = cbi.validate_store(corrupted)
                self.assertTrue(any("must exactly match store provenance" in error for error in errors))
                path = self.write_store(corrupted)
                self.assertFalse(cbi.cache_status(self.cache_args(repo.root, path))["valid"])

    def test_store_rejects_repository_metadata_inconsistent_with_provenance(self) -> None:
        repo = self.make_repo()
        store = cbi.analyze_history(self.history_args(repo.root))
        store["repository"]["repository_head"] = "other"
        self.assertIn(
            "repository.repository_head must match provenance.repository_head",
            cbi.validate_store(store),
        )

    def test_evidence_subject_paths_must_be_repository_relative(self) -> None:
        repo = self.make_repo()
        original = cbi.analyze_history(self.history_args(repo.root))
        file_observation = next(item for item in original["observations"] if item["subject"]["type"] == "file")
        pair_observation = next(item for item in original["observations"] if item["subject"]["type"] == "file_pair")
        for invalid in ("/tmp/escape.py", "../escape.py", "src/../../escape.py", "C:/escape.py"):
            with self.subTest(path=invalid):
                corrupted = json.loads(json.dumps(original))
                index = original["observations"].index(file_observation)
                corrupted["observations"][index]["subject"]["path"] = invalid
                self.assertTrue(any("repository-relative path" in error for error in cbi.validate_store(corrupted)))
        corrupted = json.loads(json.dumps(original))
        index = original["observations"].index(pair_observation)
        corrupted["observations"][index]["subject"]["paths"] = ["src/a.py", "../escape.py"]
        self.assertTrue(any("repository-relative paths" in error for error in cbi.validate_store(corrupted)))

    def test_code_maat_adapter_rejects_invalid_repository_paths(self) -> None:
        repo = self.make_repo()
        for row in ("../escape.py,2", "/tmp/escape.py,2", "C:/escape.py,2"):
            with self.subTest(row=row):
                csv_path = self.base / "invalid.csv"
                csv_path.write_text(f"entity,n-revs\n{row}\n", encoding="utf-8")
                args = argparse.Namespace(repo=str(repo.root), input=str(csv_path), analysis="revisions", provider_version="X")
                with self.assertRaisesRegex(cbi.CBIError, "generated invalid Code Maat evidence"):
                    cbi.adapt_code_maat(args)

    def test_shallow_and_insufficient_history_are_reported(self) -> None:
        source = self.make_repo()
        shallow = self.base / "shallow"
        subprocess.run(
            ["git", "clone", "-q", "--depth", "1", source.root.as_uri(), str(shallow)],
            check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        store = cbi.analyze_history(self.history_args(shallow, min_shared_commits=1))
        self.assertTrue(store["repository"]["shallow"])
        self.assertTrue(any("shallow" in item.lower() for item in store["limitations"]))
        self.assertTrue(any("fewer than two" in item.lower() for item in store["limitations"]))

    def test_repository_without_git_history_fails_clearly(self) -> None:
        empty = self.base / "empty"
        empty.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=empty, check=True)
        with self.assertRaisesRegex(cbi.CBIError, "rev-parse HEAD"):
            cbi.repo_metadata(str(empty))

    def test_code_maat_adapter_and_malformed_output(self) -> None:
        repo = self.make_repo()
        good = self.base / "coupling.csv"
        good.write_text("entity,coupled,degree,average-revs\nsrc/a.py,src/b.py,75,4\n", encoding="utf-8")
        args = argparse.Namespace(repo=str(repo.root), input=str(good), analysis="coupling", provider_version="1.0.4")
        store = cbi.adapt_code_maat(args)
        metric = store["observations"][0]["metrics"]
        self.assertEqual([0, 100], metric["range"])
        self.assertIn("Code Maat", metric["metric_definition"])
        bad = self.base / "bad.csv"
        bad.write_text("wrong,columns\na,b\n", encoding="utf-8")
        args.input = str(bad)
        with self.assertRaisesRegex(cbi.CBIError, "malformed Code Maat row"):
            cbi.adapt_code_maat(args)

    def test_query_filters_before_returning_evidence(self) -> None:
        repo = self.make_repo()
        store = cbi.analyze_history(self.history_args(repo.root))
        store_path = self.base / "store.json"
        store_path.write_text(json.dumps(store), encoding="utf-8")
        args = argparse.Namespace(store=str(store_path), type=["change_frequency"], subject=None, metric="revisions", min=2, limit=1)
        result = cbi.query_store(args)
        self.assertEqual(1, result["count"])
        self.assertEqual("change_frequency", result["observations"][0]["type"])

    def test_reference_verifier_handles_valid_missing_and_escape_paths(self) -> None:
        repo = self.make_repo()
        refs = self.base / "refs.json"
        refs.write_text(json.dumps([
            {"path": "src/a.py", "symbol": "alpha"},
            {"path": "src/missing.py"},
            {"path": "../outside"},
        ]), encoding="utf-8")
        result = cbi.verify_references(argparse.Namespace(repo=str(repo.root), references=str(refs)))
        self.assertEqual(["VERIFIED", "CONTRADICTED", "CONTRADICTED"], [item["status"] for item in result["results"]])

    def test_discovery_supports_unknown_ecosystem_and_tool_availability(self) -> None:
        root = self.base / "unusual"
        root.mkdir()
        (root / "program.xyzzy").write_text("unusual language\n", encoding="utf-8")
        with mock.patch.object(cbi.shutil, "which", side_effect=lambda name: f"/tools/{name}" if name == "git" else None):
            result = cbi.discover(str(root))
        self.assertEqual([], result["ecosystems"])
        self.assertEqual("/tools/git", result["tools"]["git"])
        self.assertIn("radon", result["missing_tools"])

    def test_discovery_finds_nested_monorepo_manifests(self) -> None:
        root = self.base / "monorepo"
        (root / "services" / "web").mkdir(parents=True)
        (root / "services" / "web" / "package.json").write_text("{}\n", encoding="utf-8")
        result = cbi.discover(str(root))
        self.assertEqual(["services/web/package.json"], result["manifests"]["javascript-typescript"])


if __name__ == "__main__":
    unittest.main()
