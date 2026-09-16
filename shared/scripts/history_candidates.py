#!/usr/bin/env python3
"""Bounded, local Git/Code Maat history candidate generation for V3."""
from __future__ import annotations
import argparse, csv, datetime as dt, fnmatch, hashlib, io, json, os, shutil, subprocess, sys, tempfile
from itertools import combinations
from pathlib import Path, PurePosixPath

DEFAULT_PARTS={".cache",".venv","__pycache__","build","cache","coverage","dist","generated","node_modules","target","vendor","venv"}
VERSION="3.0.0"
class Failure(Exception):
    def __init__(self,code,message): self.code,self.message=code,message

def command(args,cwd,check=True,text=True):
    try: return subprocess.run(args,cwd=cwd,check=check,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=text)
    except FileNotFoundError as exc: raise Failure("GIT_UNAVAILABLE" if args[0]=="git" else "CODE_MAAT_UNAVAILABLE",f"required command is unavailable: {args[0]}") from exc
    except OSError as exc: raise Failure("GIT_COMMAND_FAILED" if args[0]=="git" else "CODE_MAAT_COMMAND_FAILED",str(exc)) from exc
def git(root,*args,check=True,text=True):
    result=command(["git",*args],root,check,text)
    if check and result.returncode: raise Failure("GIT_COMMAND_FAILED",result.stderr.strip() or "Git command failed")
    return result
def root_for(value):
    requested=Path(value).resolve()
    if not requested.exists(): raise Failure("NOT_A_GIT_REPOSITORY",f"repository path does not exist: {requested}")
    probe=git(requested,"rev-parse","--show-toplevel",check=False)
    if probe.returncode: raise Failure("NOT_A_GIT_REPOSITORY",f"not a Git repository: {requested}")
    return Path(probe.stdout.strip()).resolve()
def normalized(path,allow_dot=False):
    path=path.replace("\\","/"); p=PurePosixPath(path)
    if "\0" in path or path.startswith("/") or (p==PurePosixPath(".") and not allow_dot) or ".." in p.parts: raise Failure("INVALID_REPOSITORY_PATH",f"invalid repository-relative path: {path}")
    return p.as_posix()
def relevant(path,excludes):
    return not any(x.lower() in DEFAULT_PARTS for x in PurePosixPath(path).parts) and not path.lower().endswith((".min.js",".map")) and not any(fnmatch.fnmatchcase(path,x) for x in excludes)
def tracked(root,excludes): return {normalized(x) for x in git(root,"ls-files","-z").stdout.split("\0") if x and relevant(normalized(x),excludes)}
def loc(root,excludes):
    result={}
    for path in tracked(root,excludes):
        target=root/path
        try:
            if target.is_symlink():
                try: target.resolve().relative_to(root)
                except ValueError: continue
            data=target.read_bytes()
            if b"\0" not in data: result[path]=len(data.splitlines())
        except OSError: pass
    return result
def history(root,args):
    cmd=["-c","core.quotePath=false","log","--name-status","-z",f"-M{args.rename_threshold}","--format=__CBI_V3__%H%x09%aI"]
    if args.since: cmd.append(f"--since={args.since}")
    if args.max_commits: cmd.append(f"--max-count={args.max_commits}")
    tokens=git(root,*cmd,text=False).stdout.split(b"\0"); commits=[]; current=None; i=0
    while i<len(tokens):
        token=tokens[i].decode("utf-8","surrogateescape").lstrip("\n")
        if token.startswith("__CBI_V3__"):
            if current: commits.append(current)
            head,_,date=token[10:].partition("\t"); current={"id":head,"date":date,"changes":[]}
        elif current and token:
            status=token
            if status[:1] in "RCA" and status[1:].isdigit() and i+1<len(tokens):
                old=normalized(tokens[i+1].decode("utf-8","surrogateescape")); i+=1
                if status[0]=="R" and i+1<len(tokens):
                    new=normalized(tokens[i+1].decode("utf-8","surrogateescape")); i+=1; current["changes"].append(("rename",old,new))
                elif status[0]=="C": current["changes"].append(("ambiguous",old))
                else: current["changes"].append(("path",old))
            elif status[:1] in "AMDMTUXB" and i+1<len(tokens):
                path=normalized(tokens[i+1].decode("utf-8","surrogateescape")); i+=1; current["changes"].append(("deleted" if status[:1]=="D" else "path",path))
        i+=1
    if current: commits.append(current)
    return commits
def quality(root,args,commits,eligible,bulk,bulk_touches,all_touches,paths_excluded,renames,resolved,unresolved):
    dates=[dt.datetime.fromisoformat(c["date"].replace("Z","+00:00")) for c in eligible if c["date"]]; shallow=git(root,"rev-parse","--is-shallow-repository",check=False).stdout.strip()=="true"
    start=min((x.date().isoformat() for x in dates),default=None); end=max((x.date().isoformat() for x in dates),default=None); active=(max(dates)-min(dates)).days if dates else 0; limitations=[]
    def add(code,message): limitations.append({"code":code,"message":message})
    if shallow: add("SHALLOW_HISTORY","Git reports a shallow repository; only available history was analyzed.")
    if len(eligible)<2: add("INSUFFICIENT_HISTORY","Fewer than two eligible commits remain for historical analysis.")
    if len(eligible)<args.low_sample_commits: add("LOW_SAMPLE_COMMITS",f"Only {len(eligible)} eligible commits meet the configured sample threshold.")
    if len(eligible)>=2 and active<args.low_sample_days: add("SHORT_HISTORY_SPAN","Eligible history covers fewer active days than the configured threshold.")
    if bulk: add("BULK_COMMITS_EXCLUDED","Commits exceeding the changeset cap were excluded from metrics.")
    cr=len(bulk)/len(commits) if commits else 0.0; tr=bulk_touches/all_touches if all_touches else 0.0
    if cr>=.5 or tr>=.5: add("HIGH_BULK_EXCLUSION","Bulk exclusions remove at least half of matched commits or relevant touches.")
    if unresolved: add("UNRESOLVED_RENAMES","Some historical rename/deletion mappings could not be resolved unambiguously.")
    return {"shallow":shallow,"matched_commits":len(commits),"eligible_commits":len(eligible),"history_start":start,"history_end":end,"active_days":active,"bulk_commits_excluded":len(bulk),"bulk_file_touches_excluded":bulk_touches,"bulk_commit_ratio":cr,"bulk_touch_ratio":tr,"paths_excluded":paths_excluded,"renames_detected":renames,"renames_resolved":resolved,"renames_unresolved":unresolved,"limitations":limitations}
def params_for(args,analysis):
    p={"since":args.since,"max_commits":args.max_commits,"max_changeset_size":args.max_changeset_size,"rename_threshold":args.rename_threshold,"default_exclusions":sorted(DEFAULT_PARTS),"explicit_excludes":args.exclude or [],"limit":args.limit,"low_sample_commits":args.low_sample_commits,"low_sample_days":args.low_sample_days}
    if analysis=="temporal_coupling": p.update(min_shared_commits=args.min_shared_commits,subjects=args.subject,include_deleted=args.include_deleted)
    return p
def base_result(root,args,analysis,provider,mode,scope,params,hq,definitions,candidates,total,version=None):
    if version is None: version=git(root,"--version").stdout.strip() if provider=="git" else (args.code_maat_version or "code-maat (version supplied by executable)")
    return {"schema_version":1,"result_kind":"codebase-intelligence-history-candidates","analysis":analysis,"provenance":{"provider":{"name":provider,"version":version,"mode":mode},"repository_head":git(root,"rev-parse","HEAD").stdout.strip(),"working_tree_dirty":bool(git(root,"status","--porcelain=v1","--untracked-files=all").stdout),"input_scope":scope,"parameters":params,"generated_at":dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()},"history_quality":hq,"metric_definitions":definitions,"total_candidates":total,"candidate_count":len(candidates),"truncated":total>len(candidates),"candidates":candidates}
def dense_rank(items,key):
    values=sorted({x[key] for x in items}); return {v:(i+1)/len(values) for i,v in enumerate(values)}
def prepare_history(root,args,analysis):
    commits=history(root,args); current=tracked(root,args.exclude or []); mapping={}; sets=[]; eligible=[]; bulk=[]; all_touches=bulk_touches=paths_excluded=renames=resolved=0; unresolved=set()
    for commit in commits:
        paths=[]
        for change in commit["changes"]:
            kind,path=change[0],change[1]
            if kind=="rename":
                renames+=1; destination=mapping.get(change[2],change[2]); mapping[path]=destination; mapping[change[2]]=destination; resolved+=1; paths.append(destination)
            elif kind=="ambiguous": unresolved.add(path); paths.append(path)
            else: paths.append(mapping.get(path,path))
        deleted_canonical={mapping.get(c[1],c[1]) for c in commit["changes"] if c[0]=="deleted"}
        selected=set()
        for path in paths:
            if not relevant(path,args.exclude or []): paths_excluded+=1; continue
            if path not in current and not (analysis=="temporal_coupling" and args.include_deleted):
                if path in deleted_canonical: continue
                unresolved.add(path); continue
            selected.add(path)
        all_touches+=len(selected)
        if len(selected)>args.max_changeset_size: bulk.append(commit); bulk_touches+=len(selected); sets.append(set()); continue
        sets.append(selected)
        if selected: eligible.append(commit)
    return current,commits,eligible,sets,quality(root,args,commits,eligible,bulk,bulk_touches,all_touches,paths_excluded,renames,resolved,len(unresolved))
def git_analysis(root,args,analysis):
    if git(root,"rev-parse","HEAD",check=False).returncode: raise Failure("NO_GIT_HISTORY","repository has no Git HEAD/history")
    current,commits,eligible,sets,hq=prepare_history(root,args,analysis); params=params_for(args,analysis)
    if analysis=="hotspots":
        counts={p:0 for p in current}
        for paths in sets:
            for p in paths:
                if p in counts: counts[p]+=1
        sizes=loc(root,args.exclude or []); candidates=[] if len(eligible)<2 else [{"path":p,"revisions":n,"size":sizes[p]} for p,n in counts.items() if n and p in sizes]; rr=dense_rank(candidates,"revisions") if candidates else {}; sr=dense_rank(candidates,"size") if candidates else {}
        for x in candidates: x.update(revision_rank=rr[x["revisions"]],size_rank=sr[x["size"]]); x["score"]=x["revision_rank"]*x["size_rank"]
        candidates.sort(key=lambda x:(-x["score"],-x["revisions"],-x["size"],x["path"])); total=len(candidates); candidates=candidates[:args.limit]
        defs={"revisions":{"unit":"commits_touching_file","definition":"Eligible non-bulk commits whose canonical touch set contains the path."},"size":{"name":"physical_loc","unit":"physical_lines","definition":"Current tracked text-file physical lines; blank lines count and final newline does not add a line."},"revision_rank":{"range":[0,1],"definition":"Normalized ascending dense rank; maximum is 1."},"size_rank":{"range":[0,1],"definition":"Normalized ascending dense rank; maximum is 1."},"score":{"range":[0,1],"definition":"Revision rank multiplied by size rank; candidate ranking only."}}
        return base_result(root,args,analysis,"git","built-in","committed_history+working_tree",params,hq,defs,candidates,total)
    counts={}; pairs={}
    for paths in sets:
        for p in paths: counts[p]=counts.get(p,0)+1
        for pair in combinations(sorted(paths),2): pairs[pair]=pairs.get(pair,0)+1
    candidates=[] if len(eligible)<2 else []
    for (left,right),shared in pairs.items():
        if shared>=args.min_shared_commits and (not args.subject or left in args.subject or right in args.subject): candidates.append({"paths":[left,right],"shared_commits":shared,"left_revisions":counts[left],"right_revisions":counts[right],"coupling":shared/min(counts[left],counts[right]),"average_revisions":None})
    candidates.sort(key=lambda x:(-x["shared_commits"],-x["coupling"],x["paths"][0],x["paths"][1])); total=len(candidates); candidates=candidates[:args.limit]
    defs={"shared_commits":{"unit":"commits","definition":"Eligible non-bulk commits touching both paths."},"coupling":{"unit":"ratio","range":[0,1],"definition":"Shared eligible commits divided by the smaller endpoint revision count."},"ordering":"Shared commits descending, coupling descending, then lexicographic paths."}
    return base_result(root,args,analysis,"git","built-in","committed_history",params,hq,defs,candidates,total)
def csv_rows(path,required):
    try:
        with open(path,newline="",encoding="utf-8") as handle:
            reader=csv.DictReader(handle)
            if not reader.fieldnames or not set(required)<=set(reader.fieldnames): raise Failure("MALFORMED_CODE_MAAT_CSV",f"missing required columns in {path}")
            return list(reader)
    except Failure: raise
    except (OSError,UnicodeError) as exc: raise Failure("MALFORMED_CODE_MAAT_CSV",str(exc)) from exc
def csv_text_rows(text,required):
    reader=csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or not set(required)<=set(reader.fieldnames): raise Failure("MALFORMED_CODE_MAAT_CSV","Code Maat output is missing required columns")
    return list(reader)
def csv_entity(value):
    try: return normalized(value)
    except Failure as exc: raise Failure("INVALID_CODE_MAAT_ENTITY",exc.message) from exc
def integer(value,label,minimum=0):
    try: result=int(value)
    except (TypeError,ValueError) as exc: raise Failure("RESULT_VALIDATION_FAILED",f"invalid {label}") from exc
    if result<minimum: raise Failure("RESULT_VALIDATION_FAILED",f"invalid {label}")
    return result
def optional_integer(row,name): return None if row.get(name) in (None,"") else integer(row[name],name)
def optional_number(row,name):
    if row.get(name) in (None,""): return None
    try: value=float(row[name])
    except (TypeError,ValueError) as exc: raise Failure("RESULT_VALIDATION_FAILED",f"invalid {name}") from exc
    if value < 0: raise Failure("RESULT_VALIDATION_FAILED",f"invalid {name}")
    return value
def validate_hotspot_rows(rev_rows,churn_rows):
    revisions={}; churn={}
    for row in rev_rows:
        p=csv_entity(row.get("entity"));
        if p in revisions: raise Failure("RESULT_VALIDATION_FAILED","duplicate hotspot entity")
        revisions[p]=integer(row.get("n-revs"),"n-revs")
    for row in churn_rows:
        p=csv_entity(row.get("entity"));
        if p in churn: raise Failure("RESULT_VALIDATION_FAILED","duplicate hotspot entity")
        churn[p]=integer(row.get("added"),"added")+integer(row.get("deleted"),"deleted")
    if set(revisions)!=set(churn): raise Failure("INCONSISTENT_CODE_MAAT_HOTSPOT_INPUTS","hotspot inputs contain different entities")
    return revisions,churn
def validate_coupling_rows(rows):
    parsed=[]; seen=set()
    for row in rows:
        left,right=csv_entity(row.get("entity")),csv_entity(row.get("coupled")); pair=tuple(sorted((left,right)))
        if left==right or pair in seen: raise Failure("RESULT_VALIDATION_FAILED","duplicate or self coupling pair")
        seen.add(pair)
        try: degree=float(row.get("degree"))
        except (TypeError,ValueError) as exc: raise Failure("RESULT_VALIDATION_FAILED","invalid coupling degree") from exc
        if not 0<=degree<=100: raise Failure("RESULT_VALIDATION_FAILED","invalid coupling degree")
        parsed.append((pair,degree,{"shared-revisions":optional_integer(row,"shared-revisions"),"entity-revisions":optional_integer(row,"entity-revisions"),"coupled-revisions":optional_integer(row,"coupled-revisions"),"average-revs":optional_number(row,"average-revs")}))
    return parsed
def imported_hq(root,args,analysis):
    if git(root,"rev-parse","HEAD",check=False).returncode: raise Failure("NO_GIT_HISTORY","repository has no Git HEAD/history")
    return prepare_history(root,args,analysis)[4]
def maat_params(args,analysis,prefix,inputs=()):
    result=params_for(args,analysis); result.update(code_maat_analyses=["revisions","entity-churn"] if analysis=="hotspots" else ["coupling"],code_maat_command=prefix)
    if inputs: result["input_sha256"]={str(p):hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in inputs}
    return result
def provider_result(root,args,analysis,revisions,churn,coupling,version,mode,inputs=(),prefix=()):
    current=tracked(root,args.exclude or []); hq=imported_hq(root,args,analysis); params=maat_params(args,analysis,prefix,inputs)
    if analysis=="hotspots":
        candidates=[{"path":p,"revisions":revisions[p],"size":churn[p]} for p in revisions if p in current and revisions[p]>0]; rr=dense_rank(candidates,"revisions") if candidates else {}; sr=dense_rank(candidates,"size") if candidates else {}
        for x in candidates: x.update(revision_rank=rr[x["revisions"]],size_rank=sr[x["size"]]); x["score"]=x["revision_rank"]*x["size_rank"]
        candidates.sort(key=lambda x:(-x["score"],-x["revisions"],-x["size"],x["path"])); defs={"revisions":{"unit":"Code Maat revisions","definition":"Provider-defined n-revs value."},"size":{"name":"absolute_entity_churn","unit":"lines","definition":"Code Maat added plus deleted entity churn."},"revision_rank":{"range":[0,1],"definition":"Normalized ascending dense rank; maximum is 1."},"size_rank":{"range":[0,1],"definition":"Normalized ascending dense rank; maximum is 1."},"score":{"range":[0,1],"definition":"Revision rank multiplied by size rank; candidate ranking only."}}
    else:
        candidates=[]
        for pair,degree,support in coupling:
            left,right=pair; allowed=(left in current and right in current) or (args.include_deleted and left not in (".","..") and right not in (".",".."))
            if not allowed or (args.subject and left not in args.subject and right not in args.subject): continue
            if support["shared-revisions"] is not None and support["shared-revisions"]<args.min_shared_commits: continue
            candidates.append({"paths":[left,right],"shared_commits":support["shared-revisions"],"left_revisions":support["entity-revisions"],"right_revisions":support["coupled-revisions"],"coupling":degree,"average_revisions":support["average-revs"]})
        support=bool(candidates) and all(x["shared_commits"] is not None for x in candidates); candidates.sort(key=(lambda x:(-x["shared_commits"],-x["coupling"],x["paths"][0],x["paths"][1])) if support else (lambda x:(-x["coupling"],x["paths"][0],x["paths"][1])))
        if not support: hq["limitations"].append({"code":"CODE_MAAT_SUPPORT_FILTER_UNAVAILABLE","message":"Code Maat output did not contain shared support."})
        defs={"shared_commits":{"unit":"commits or null","definition":"Provider-supplied shared revisions when present."},"coupling":{"unit":"percent","range":[0,100],"definition":"Code Maat provider-defined degree; not divided by 100."},"ordering":"Shared support descending, coupling descending, then paths." if support else "Coupling descending, then paths (shared support unavailable)."}
    if mode=="csv": hq["limitations"] += [{"code":"CODE_MAAT_INPUT_FILTERS_UNVERIFIED","message":"Imported CSV does not prove local history filtering."},{"code":"CODE_MAAT_RENAME_HANDLING_UNVERIFIED","message":"Imported CSV does not prove rename preprocessing."}]
    total=len(candidates); return base_result(root,args,analysis,"code-maat",mode,"committed_history",params,hq,defs,candidates[:args.limit],total,version)
def csv_provider(root,args,analysis):
    if not args.code_maat_version: raise Failure("CODE_MAAT_VERSION_UNKNOWN","--code-maat-version is required for Code Maat CSV input")
    if analysis=="hotspots":
        a,b=Path(args.code_maat_revisions_csv),Path(args.code_maat_churn_csv); revisions,churn=validate_hotspot_rows(csv_rows(a,["entity","n-revs"]),csv_rows(b,["entity","added","deleted"])); return provider_result(root,args,analysis,revisions,churn,None,args.code_maat_version,"csv",[a,b])
    path=Path(args.code_maat_coupling_csv); return provider_result(root,args,analysis,None,None,validate_coupling_rows(csv_rows(path,["entity","coupled","degree"])),args.code_maat_version,"csv",[path])
def executable_provider(root,args,analysis):
    prefix=args.code_maat_command or ["code-maat"]
    version=args.code_maat_version
    if not version:
        probe=command(prefix+["--version"],root,check=False)
        if probe.returncode==0 and probe.stdout.strip(): version=probe.stdout.strip().splitlines()[0]
    if not version: raise Failure("CODE_MAAT_VERSION_UNKNOWN","Code Maat version could not be determined")
    current,commits,eligible,sets,hq=prepare_history(root,args,analysis)
    with tempfile.TemporaryDirectory() as directory:
        log=Path(directory)/"history.log"; lines=[]
        for commit,paths in zip(commits,sets):
            if paths: lines.append(f"[{commit['id']}] {commit['date']}"); lines.extend(f"1\t0\t{p}" for p in sorted(paths))
        log.write_text("\n".join(lines)+("\n" if lines else ""),encoding="utf-8")
        def run(name):
            result=command(prefix+["--analysis",name,"--input",str(log)],root,check=False)
            if result.returncode: raise Failure("CODE_MAAT_COMMAND_FAILED",result.stderr.strip() or "Code Maat failed")
            return result.stdout
        if analysis=="hotspots":
            revisions,churn=validate_hotspot_rows(csv_text_rows(run("revisions"),["entity","n-revs"]),csv_text_rows(run("entity-churn"),["entity","added","deleted"]))
            result=provider_result(root,args,analysis,revisions,churn,None,version,"executable",prefix=prefix)
        else:
            coupling=validate_coupling_rows(csv_text_rows(run("coupling"),["entity","coupled","degree"]))
            result=provider_result(root,args,analysis,None,None,coupling,version,"executable",prefix=prefix)
            if not any(row[2]["shared-revisions"] is not None for row in coupling):
                hq["limitations"].append({"code":"CODE_MAAT_SUPPORT_FILTER_UNAVAILABLE","message":"Code Maat output did not contain shared support."})
        result["history_quality"]=hq; return result
def build_parser():
    p=argparse.ArgumentParser(description="Generate bounded Git or Code Maat history candidates."); p.add_argument("--version",action="version",version=VERSION); sub=p.add_subparsers(dest="command",required=True)
    def common(c):
        c.add_argument("--repo",default="."); c.add_argument("--provider",choices=["auto","git","code-maat"],default="auto"); c.add_argument("--limit",type=int,default=20); c.add_argument("--since"); c.add_argument("--max-commits",type=int); c.add_argument("--max-changeset-size",type=int,default=30); c.add_argument("--rename-threshold",type=int,default=50); c.add_argument("--exclude",action="append"); c.add_argument("--low-sample-commits",type=int,default=20); c.add_argument("--low-sample-days",type=int,default=30); c.add_argument("--output"); c.add_argument("--code-maat-command",type=json.loads); c.add_argument("--code-maat-version")
    h=sub.add_parser("hotspots"); common(h); h.add_argument("--code-maat-revisions-csv"); h.add_argument("--code-maat-churn-csv")
    t=sub.add_parser("temporal-coupling"); common(t); t.add_argument("--min-shared-commits",type=int,default=2); t.add_argument("--subject",action="append",default=[]); t.add_argument("--include-deleted",action="store_true"); t.add_argument("--code-maat-coupling-csv")
    return p
def validate_args(a):
    for name in ("limit","max_changeset_size","rename_threshold","low_sample_commits"):
        if getattr(a,name)<=0: raise Failure("USAGE","options must be positive")
    if not 1<=a.limit<=100 or not 1<=a.rename_threshold<=100 or a.low_sample_days<0: raise Failure("USAGE","option value is outside its allowed range")
    if a.max_commits is not None and a.max_commits<=0: raise Failure("USAGE","--max-commits must be positive")
    if a.command=="hotspots":
        if bool(a.code_maat_revisions_csv)!=bool(a.code_maat_churn_csv): raise Failure("USAGE","both hotspot CSV inputs are required together")
        if a.provider=="git" and (a.code_maat_revisions_csv or a.code_maat_churn_csv or a.code_maat_command or a.code_maat_version): raise Failure("USAGE","Code Maat options conflict with --provider git")
    else:
        if a.min_shared_commits<=0: raise Failure("USAGE","--min-shared-commits must be positive")
        if a.provider=="git" and (a.code_maat_coupling_csv or a.code_maat_command or a.code_maat_version): raise Failure("USAGE","Code Maat options conflict with --provider git")
        for s in a.subject: normalized(s)
def main(argv=None):
    try:
        a=build_parser().parse_args(argv); validate_args(a); root=root_for(a.repo); analysis="hotspots" if a.command=="hotspots" else "temporal_coupling"; csv_requested=bool((a.command=="hotspots" and a.code_maat_revisions_csv) or (a.command=="temporal-coupling" and a.code_maat_coupling_csv)); provider="code-maat" if csv_requested or a.provider=="code-maat" or (a.provider=="auto" and (a.code_maat_command or shutil.which("code-maat"))) else "git"
        if provider=="code-maat" and csv_requested: result=csv_provider(root,a,analysis)
        elif provider=="code-maat":
            try: result=executable_provider(root,a,analysis)
            except Failure as exc:
                if a.provider!="auto": raise
                result=git_analysis(root,a,analysis); result["history_quality"]["limitations"].append({"code":"CODE_MAAT_FAILED_FALLBACK_GIT","message":exc.message[:200]})
        else: result=git_analysis(root,a,analysis)
        output=json.dumps(result,separators=(",",":"),ensure_ascii=False)
        if a.output:
            target=Path(a.output).resolve()
            if target.exists() and target.is_dir(): raise Failure("INVALID_OUTPUT_PATH",f"output path is a directory: {target}")
            try: target.parent.mkdir(parents=True,exist_ok=True); tmp=target.with_name(target.name+".tmp"); tmp.write_text(output+"\n",encoding="utf-8"); os.replace(tmp,target)
            except OSError as exc: raise Failure("INVALID_OUTPUT_PATH",str(exc)) from exc
        print(output)
        return 0
    except Failure as exc:
        print(json.dumps({"error":{"code":exc.code,"message":exc.message}}),file=sys.stderr); return 2 if exc.code=="USAGE" else 1
    except (TypeError,ValueError,json.JSONDecodeError) as exc:
        print(json.dumps({"error":{"code":"USAGE","message":str(exc)}}),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
