#!/usr/bin/env python3
from __future__ import annotations
import argparse,platform,sys,json
from pathlib import Path
from v14_predicate_horizon_common import *
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--project-root",type=Path,required=True);ap.add_argument("--lock",type=Path,required=True);ap.add_argument("--candidate",type=Path,required=True);ap.add_argument("--v10-run-root",type=Path,required=True);ap.add_argument("--v13-host-lock",type=Path,required=True);ap.add_argument("--v13-profile-lock",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();verify_lock(root,a.lock)
 if a.out.exists():raise SystemExit("REFUSE_OVERWRITE")
 a.out.mkdir(parents=True);oldh=loadj(a.v13_host_lock);oldp=loadj(a.v13_profile_lock);oldbase=loadj(a.v10_run_root/"host/base_snapshot_manifest.json");snap=Path(oldh["base_snapshot_path"]);fail=[]
 for rel,meta in oldbase["files"].items():
  p=snap/rel
  if not p.is_file() or p.stat().st_size!=meta["bytes"] or sha256_file(p)!=meta["sha256"]:fail.append(rel)
 if fail:raise SystemExit("BASE_SNAPSHOT_REVERIFY_FAIL "+repr(fail))
 import torch,transformers,peft,bitsandbytes,numpy
 crit={"python":sys.version,"platform":platform.platform(),"torch":torch.__version__,"torch_cuda":torch.version.cuda,"transformers":transformers.__version__,"peft":peft.__version__,"bitsandbytes":bitsandbytes.__version__,"numpy":numpy.__version__,"cuda_available":torch.cuda.is_available(),"gpu_name":torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,"gpu_total_memory_bytes":torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else None,"compute_capability":list(torch.cuda.get_device_capability(0)) if torch.cuda.is_available() else None,"executable":sys.executable}
 for k in ["torch","torch_cuda","transformers","peft","bitsandbytes","numpy","cuda_available","gpu_name","gpu_total_memory_bytes","compute_capability"]:
  if crit[k]!=oldh["runtime_critical"][k]:raise SystemExit(f"CRITICAL_RUNTIME_DRIFT {k} current={crit[k]!r} prior={oldh['runtime_critical'][k]!r}")
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(str(snap),use_fast=False,trust_remote_code=False,local_files_only=True);rows=loadjl(a.candidate/(DATASET+".jsonl"));refs=loadjl(a.candidate/(DATASET+".token_reference.private.jsonl"));mism=[]
 for i,(r,ref) in enumerate(zip(rows,refs)):
  ids=tok(chatml(r["messages"]),add_special_tokens=True,return_attention_mask=False)["input_ids"]
  if ids!=ref["input_ids"]:mism.append({"row":i,"id":r["id"]})
 if mism:dumpj(a.out/"TOKENIZER_MISMATCHES.json",mism);raise SystemExit(("TOKENIZER_REPLAY_FAIL",len(mism)))
 newmax=max(r["tokens"] for r in refs);oldmax=int(oldh["v13_max_tokens"])
 if newmax>oldmax:raise SystemExit(("PROFILE_LENGTH_INHERIT_FAIL",newmax,oldmax))
 host={"schema":"cfe.v14.predicate-horizon-host-lock.v1","status":"HOST_REVERIFIED__TOKENIZER_REPLAY_PASS__PROFILE_REPEATABILITY_PENDING","input_lock_sha256":sha256_file(a.lock),"base_snapshot_manifest_sha256":oldh["base_snapshot_manifest_sha256"],"base_snapshot_path":str(snap),"hf_repo":oldh["hf_repo"],"hf_revision":oldh["hf_revision"],"snapshot_file_count":len(oldbase["files"]),"snapshot_all_files_reverified":True,"runtime_critical":crit,"source_v13_host_lock_sha256":sha256_file(a.v13_host_lock),"runtime_tokenizer_exact_match":True,"tokenizer_replay":{DATASET:{"rows":len(rows),"mismatches":0,"max_tokens":newmax}},"v13_qualified_max_tokens":oldmax,"v14_max_tokens":newmax,"profile_inheritance_length_gate":newmax<=oldmax,"inherited_selected_profile":oldp["selected_profile"],"source_v13_profile_lock_sha256":sha256_file(a.v13_profile_lock),"laws":["SAME SOURCE != SAME EXECUTABLE ENVIRONMENT","OLD PROFILE FIT != NEW LOCK REPEATABILITY","TOKEN REFERENCE PRESENT != LIVE TOKENIZER MATCH"]};dumpj(a.out/"HOST_LOCK.json",host);dumpj(a.out/"RUNTIME_ENVIRONMENT_CRITICAL.json",crit);print(json.dumps(host,indent=2,sort_keys=True))
if __name__=="__main__":main()
