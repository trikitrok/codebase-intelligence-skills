import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("history_candidates", ROOT / "shared/scripts/history_candidates.py")
module = importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(module)


class Repo:
    def __init__(self, root):
        self.root = root; self.run("init", "-q"); self.run("config", "user.name", "Fixture"); self.run("config", "user.email", "fixture@example.test")
    def run(self, *args, check=True, env=None):
        return subprocess.run(["git", *args], cwd=self.root, check=check, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env).stdout
    def write(self, path, text):
        p = self.root / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8")
    def binary(self, path, data=b"\0binary"):
        p = self.root / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    def commit(self, message):
        self.run("add", "."); self.run("commit", "-qm", message)


class HistoryCandidatesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.base = Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()
    def repo(self):
        path = self.base / f"repo{len(list(self.base.iterdir()))}"; path.mkdir(); return Repo(path)
    def run_cli(self, repo, *args, env=None):
        return subprocess.run([sys.executable, str(ROOT / "shared/scripts/history_candidates.py"), *args, "--repo", str(repo.root)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    def data(self, result): self.assertEqual(0, result.returncode, result.stderr); return json.loads(result.stdout)
    def fake(self, coupling=False, fail=False):
        script = self.base / "fake-code-maat.py"; log = self.base / "maat-input.log"
        script.write_text("""#!/usr/bin/env python3
import pathlib, sys
if sys.argv[1:] == ['--version']:
    print('fake-code-maat 1.0'); raise SystemExit
args=sys.argv[1:]; input_path=pathlib.Path(args[args.index('--input')+1]); log=pathlib.Path(__import__('os').environ['FAKE_LOG']); log.write_text(input_path.read_text())
if __import__('os').environ.get('FAKE_FAIL'): print('boom', file=sys.stderr); raise SystemExit(9)
analysis=args[args.index('--analysis')+1]
if analysis == 'revisions': print('entity,n-revs\\na,2\\nb,1\\n')
elif analysis == 'entity-churn': print('entity,added,deleted\\na,5,1\\nb,1,0\\n')
else: print('entity,coupled,degree,shared-revisions,entity-revisions,coupled-revisions,average-revs\\na,b,80,3,4,5,4.5\\na,c,90,1,2,2,2\\n')
""", encoding="utf-8"); script.chmod(script.stat().st_mode | stat.S_IEXEC); return script, log

    # 1, 12, 13, 14: revisions, dense ties, stable order, bounded totals.
    def test_hotspot_count_rank_order_limit_and_provenance(self):
        r=self.repo()
        for p in ("a","b","c"): r.write(Path(p), "x\n\n")
        r.commit("one"); r.write(Path("a"), "y\n\n"); r.write(Path("b"), "y\n\n"); r.commit("two")
        r.write(Path("a"), "z\n\n"); r.write(Path("b"), "z\n\n"); r.commit("three")
        d=self.data(self.run_cli(r,"hotspots","--low-sample-commits","1","--limit","2"))
        self.assertEqual(["a","b"], [x["path"] for x in d["candidates"]]); self.assertEqual(3,d["candidates"][0]["revisions"]); self.assertEqual(3,d["total_candidates"]); self.assertTrue(d["truncated"]); self.assertEqual(2,d["candidate_count"]); self.assertEqual(1.0,d["candidates"][0]["revision_rank"]); self.assertNotIn("provenance",d["candidates"][0])

    # 2: blank/final-newline/empty/binary/outside symlink physical LOC.
    def test_physical_loc_and_symlink_safety(self):
        r=self.repo(); r.write(Path("blank"), "\n\n"); r.write(Path("none"), ""); r.write(Path("no-final"), "a\nb"); r.binary(Path("binary")); outside=self.base/"outside"; outside.write_text("x\n"); (r.root/"outside-link").symlink_to(outside); r.commit("one"); r.write(Path("blank"), "\n\n!"); r.commit("two")
        d=self.data(self.run_cli(r,"hotspots","--low-sample-commits","1"))
        sizes={x["path"]:x["size"] for x in d["candidates"]}; self.assertEqual(3,sizes["blank"]); self.assertEqual(0,sizes["none"]); self.assertEqual(2,sizes["no-final"]); self.assertNotIn("binary",sizes); self.assertNotIn("outside-link",sizes)

    # 3, 4, 18: all default exclusions, repeatable globs, tests are ordinary paths.
    def test_default_and_explicit_filters_keep_tests(self):
        r=self.repo()
        for p in ("vendor/v","build/b","cache/c","dist/d","generated/g","node_modules/n","target/t","venv/e",".venv/f","__pycache__/p","coverage/q","x.min.js","x.map","tests/keep.py","src/keep.py","src/no.py"): r.write(Path(p),"x\n")
        r.commit("one"); r.write(Path("tests/keep.py"),"y\n"); r.write(Path("src/keep.py"),"y\n"); r.commit("two")
        d=self.data(self.run_cli(r,"hotspots","--low-sample-commits","1","--exclude","src/no.py","--exclude","tests/*.tmp"))
        paths={x["path"] for x in d["candidates"]}; self.assertEqual({"tests/keep.py","src/keep.py"},paths); self.assertGreaterEqual(d["history_quality"]["paths_excluded"],2); self.assertIn("default_exclusions",d["provenance"]["parameters"])

    # 5, 6, 7: bulk behavior and both quality ratios/codes.
    def test_bulk_excludes_hotspot_and_temporal_metrics(self):
        r=self.repo(); r.write(Path("a"),"1\n"); r.write(Path("b"),"1\n"); r.commit("one")
        for i in range(4): r.write(Path(f"bulk{i}"),"x\n")
        r.write(Path("a"),"2\n"); r.write(Path("b"),"2\n"); r.commit("bulk")
        r.write(Path("a"),"3\n"); r.write(Path("b"),"3\n"); r.commit("three")
        h=self.data(self.run_cli(r,"hotspots","--low-sample-commits","1","--max-changeset-size","2")); t=self.data(self.run_cli(r,"temporal-coupling","--low-sample-commits","1","--max-changeset-size","2"))
        self.assertEqual(2,h["candidates"][0]["revisions"]); self.assertEqual(2,t["candidates"][0]["shared_commits"]); self.assertEqual(1,h["history_quality"]["bulk_commits_excluded"]); self.assertGreater(h["history_quality"]["bulk_commit_ratio"],0); self.assertGreater(h["history_quality"]["bulk_touch_ratio"],0); self.assertIn("BULK_COMMITS_EXCLUDED",[x["code"] for x in h["history_quality"]["limitations"]])

    # 8, 9, 10, 11: rename chain, ordinary deletion, unresolved/copy, include-deleted.
    def test_rename_deletion_and_include_deleted(self):
        r=self.repo(); r.write(Path("old"),"x\n"); r.commit("one"); r.run("mv","old","mid"); r.commit("two"); r.run("mv","mid","new"); r.commit("three")
        h=self.data(self.run_cli(r,"hotspots","--low-sample-commits","1")); self.assertIn("new",[x["path"] for x in h["candidates"]]); self.assertEqual(3,next(x["revisions"] for x in h["candidates"] if x["path"]=="new")); self.assertNotIn("UNRESOLVED_RENAMES",[x["code"] for x in h["history_quality"]["limitations"]])
        deleted=self.repo(); deleted.write(Path("old"),"x\n"); deleted.commit("one"); deleted.run("mv","old","gone"); deleted.commit("rename"); deleted.run("rm","gone"); deleted.commit("delete")
        hd=self.data(self.run_cli(deleted,"hotspots","--low-sample-commits","1")); self.assertIn("UNRESOLVED_RENAMES",[x["code"] for x in hd["history_quality"]["limitations"]]); self.assertEqual(1,hd["history_quality"]["renames_unresolved"])
        included=self.repo(); included.write(Path("old"),"x\n"); included.write(Path("a"),"x\n"); included.commit("one"); included.run("rm","old"); included.write(Path("a"),"y\n"); included.commit("delete-and-change")
        t=self.data(self.run_cli(included,"temporal-coupling","--low-sample-commits","1","--include-deleted")); self.assertEqual([["a","old"]], [x["paths"] for x in t["candidates"]])

    # 15, 16, 17: support formula, endpoint revisions, support-first and exact subjects.
    def test_temporal_formula_order_and_exact_subject(self):
        r=self.repo()
        for p in ("a","b","c"): r.write(Path(p),"x\n")
        r.commit("one"); r.write(Path("a"),"y\n"); r.write(Path("b"),"y\n"); r.commit("two"); r.write(Path("a"),"z\n"); r.write(Path("b"),"z\n"); r.write(Path("c"),"y\n"); r.commit("three")
        d=self.data(self.run_cli(r,"temporal-coupling","--low-sample-commits","1","--min-shared-commits","2","--subject","a"))
        self.assertEqual([["a","b"],["a","c"]],[x["paths"] for x in d["candidates"]]); self.assertEqual(3,d["candidates"][0]["shared_commits"]); self.assertEqual(3,d["candidates"][0]["left_revisions"]); self.assertAlmostEqual(1.0,d["candidates"][0]["coupling"]); self.assertEqual([],self.data(self.run_cli(r,"temporal-coupling","--low-sample-commits","1","--subject","a-prefix"))["candidates"])

    # 19, 20, 21: shallow, insufficient, low sample and short span.
    def test_history_quality_limitations_and_empty_insufficient(self):
        r=self.repo(); r.write(Path("a"),"x\n"); r.write(Path("b"),"x\n"); r.commit("one"); d=self.data(self.run_cli(r,"temporal-coupling")); self.assertEqual([],d["candidates"]); self.assertIn("INSUFFICIENT_HISTORY",[x["code"] for x in d["history_quality"]["limitations"]])
        r.write(Path("a"),"y\n"); r.write(Path("b"),"y\n"); r.commit("two"); d=self.data(self.run_cli(r,"hotspots")); codes=[x["code"] for x in d["history_quality"]["limitations"]]; self.assertIn("LOW_SAMPLE_COMMITS",codes); self.assertIn("SHORT_HISTORY_SPAN",codes)
        shallow=self.base/"shallow"; subprocess.run(["git","clone","-q","--depth","1",f"file://{r.root}",str(shallow)],check=True); sr=type("R",(),{"root":shallow})(); sd=self.data(self.run_cli(sr,"hotspots")); self.assertIn("SHALLOW_HISTORY",[x["code"] for x in sd["history_quality"]["limitations"]])

    # 22, 39: dirty/input-scope provenance and result-level-only provenance.
    def test_provenance_dirty_scope_and_parameters(self):
        r=self.repo(); r.write(Path("a"),"x\n"); r.write(Path("b"),"x\n"); r.commit("one"); r.write(Path("a"),"y\n"); r.write(Path("b"),"y\n"); r.commit("two"); r.write(Path("untracked"),"x")
        d=self.data(self.run_cli(r,"hotspots","--low-sample-commits","1","--since","2000-01-01","--max-commits","5","--rename-threshold","60")); self.assertTrue(d["provenance"]["working_tree_dirty"]); self.assertEqual("committed_history+working_tree",d["provenance"]["input_scope"]); self.assertEqual("2000-01-01",d["provenance"]["parameters"]["since"]); self.assertNotIn("untracked",str(d)); self.assertTrue(all("provenance" not in x for x in d["candidates"]))

    # 23, 24, 25: empty/non-Git/missing Git.
    def test_operational_git_failures_are_structured(self):
        empty=self.base/"empty"; empty.mkdir(); subprocess.run(["git","init","-q"],cwd=empty,check=True); e=self.run_cli(type("R",(),{"root":empty})(),"hotspots"); self.assertEqual("NO_GIT_HISTORY",json.loads(e.stderr)["error"]["code"])
        plain=self.base/"plain"; plain.mkdir(); e=self.run_cli(type("R",(),{"root":plain})(),"hotspots"); self.assertEqual("NOT_A_GIT_REPOSITORY",json.loads(e.stderr)["error"]["code"])
        r=self.repo(); r.write(Path("a"),"x\n"); r.commit("one"); e=self.run_cli(r,"hotspots",env={**os.environ,"PATH":str(self.base)}); self.assertEqual("GIT_UNAVAILABLE",json.loads(e.stderr)["error"]["code"])

    # 26, 27, 28, 29, 30, 31: native CSV parsing, ranges, support, hashes, filtering limitations.
    def test_csv_validation_support_semantics_hashes_and_filters(self):
        r=self.repo(); r.write(Path("a"),"x\n"); r.write(Path("b"),"x\n"); r.commit("one"); r.write(Path("a"),"y\n"); r.write(Path("b"),"y\n"); r.commit("two")
        rev=self.base/"r.csv"; churn=self.base/"c.csv"; pair=self.base/"p.csv"; rev.write_text("entity,n-revs\na,2\nb,1\n"); churn.write_text("entity,added,deleted\na,5,1\nb,1,0\n"); pair.write_text("entity,coupled,degree,shared-revisions,entity-revisions,coupled-revisions,average-revs\na,b,75,2,4,3,3.5\n")
        d=self.data(self.run_cli(r,"hotspots","--provider","code-maat","--code-maat-version","x","--code-maat-revisions-csv",str(rev),"--code-maat-churn-csv",str(churn))); self.assertEqual(hashlib.sha256(rev.read_bytes()).hexdigest(),d["provenance"]["parameters"]["input_sha256"][str(rev)]); self.assertIn("CODE_MAAT_INPUT_FILTERS_UNVERIFIED",[x["code"] for x in d["history_quality"]["limitations"]])
        d=self.data(self.run_cli(r,"temporal-coupling","--provider","code-maat","--code-maat-version","x","--min-shared-commits","2","--code-maat-coupling-csv",str(pair))); self.assertEqual(75,d["candidates"][0]["coupling"]); self.assertEqual(4,d["candidates"][0]["left_revisions"]); self.assertEqual(3,d["candidates"][0]["right_revisions"])
        bad=self.base/"bad.csv"; bad.write_text("entity,coupled,degree\na,b,101\n"); e=self.run_cli(r,"temporal-coupling","--provider","code-maat","--code-maat-version","x","--code-maat-coupling-csv",str(bad)); self.assertEqual("RESULT_VALIDATION_FAILED",json.loads(e.stderr)["error"]["code"])
        mismatch=self.base/"mismatch.csv"; mismatch.write_text("entity,added,deleted\na,1,0\n"); e=self.run_cli(r,"hotspots","--provider","code-maat","--code-maat-version","x","--code-maat-revisions-csv",str(rev),"--code-maat-churn-csv",str(mismatch)); self.assertEqual("INCONSISTENT_CODE_MAAT_HOTSPOT_INPUTS",json.loads(e.stderr)["error"]["code"])

    # 32, 33, 34, 35, 37: fake executable, no shell, fallback, explicit failure, precedence, clean stdout.
    def test_executable_filtering_support_and_provider_behavior(self):
        r=self.repo(); r.write(Path("a"),"x\n"); r.write(Path("b"),"x\n"); r.write(Path("vendor/no"),"x\n"); r.commit("one"); r.write(Path("a"),"y\n"); r.write(Path("b"),"y\n"); r.commit("two"); script,log=self.fake(); env={**os.environ,"FAKE_LOG":str(log)}
        d=self.data(self.run_cli(r,"hotspots","--provider","code-maat","--code-maat-command",json.dumps([str(script)]),"--code-maat-version","fake",env=env)); self.assertEqual("executable",d["provenance"]["provider"]["mode"]); self.assertNotIn("vendor/no",log.read_text()); self.assertIn("[",log.read_text()); self.assertEqual(0,d["history_quality"]["bulk_commits_excluded"])
        d=self.data(self.run_cli(r,"temporal-coupling","--provider","code-maat","--code-maat-command",json.dumps([str(script)]),"--code-maat-version","fake","--min-shared-commits","2",env=env)); self.assertEqual(80,d["candidates"][0]["coupling"]); self.assertEqual(3,d["candidates"][0]["shared_commits"]); self.assertEqual("Shared support descending, coupling descending, then paths.",d["metric_definitions"]["ordering"])
        badenv={**env,"FAKE_FAIL":"1"}; d=self.data(self.run_cli(r,"hotspots","--code-maat-command",json.dumps([str(script)]),"--low-sample-commits","1",env=badenv)); self.assertEqual("git",d["provenance"]["provider"]["name"]); self.assertIn("CODE_MAAT_FAILED_FALLBACK_GIT",[x["code"] for x in d["history_quality"]["limitations"]])
        e=self.run_cli(r,"hotspots","--provider","code-maat","--code-maat-command",json.dumps([str(script)]),"--code-maat-version","fake",env=badenv); self.assertEqual("CODE_MAAT_COMMAND_FAILED",json.loads(e.stderr)["error"]["code"]); self.assertEqual("",e.stdout)
        rev=self.base/"precedence-r.csv"; churn=self.base/"precedence-c.csv"; rev.write_text("entity,n-revs\na,2\n"); churn.write_text("entity,added,deleted\na,1,0\n")
        d=self.data(self.run_cli(r,"hotspots","--code-maat-command",json.dumps([str(script)]),"--code-maat-version","fake","--code-maat-revisions-csv",str(rev),"--code-maat-churn-csv",str(churn),env=env)); self.assertEqual("csv",d["provenance"]["provider"]["mode"])

    # 36, 38: conflicts, invalid args, structured provider/output errors.
    def test_argument_and_structured_output_errors(self):
        r=self.repo(); r.write(Path("a"),"x\n"); r.commit("one"); e=self.run_cli(r,"hotspots","--provider","git","--code-maat-version","x"); self.assertEqual(2,e.returncode); self.assertEqual("USAGE",json.loads(e.stderr)["error"]["code"])
        e=self.run_cli(r,"temporal-coupling","--min-shared-commits","0"); self.assertEqual(2,e.returncode); self.assertEqual("USAGE",json.loads(e.stderr)["error"]["code"])
        e=self.run_cli(r,"hotspots","--output",str(r.root)); self.assertEqual(1,e.returncode); self.assertEqual("INVALID_OUTPUT_PATH",json.loads(e.stderr)["error"]["code"]); self.assertEqual("",e.stdout)

    # 40: explicit output is byte-for-byte JSON equivalent to stdout.
    def test_output_file_matches_stdout(self):
        r=self.repo(); r.write(Path("a"),"x\n"); r.write(Path("b"),"x\n"); r.commit("one"); r.write(Path("a"),"y\n"); r.write(Path("b"),"y\n"); r.commit("two"); output=self.base/"result.json"; result=self.run_cli(r,"hotspots","--low-sample-commits","1","--output",str(output)); self.assertEqual(result.stdout.strip(),output.read_text().strip())


if __name__ == "__main__": unittest.main()
