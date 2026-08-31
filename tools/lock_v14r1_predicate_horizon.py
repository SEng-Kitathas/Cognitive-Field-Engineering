#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json
def H(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(8*1024*1024),b""):h.update(b)
 return h.hexdigest()
def main(root,out):
 rels=[
 "state/next_steps/V14_PREDICATE_DOSE_HORIZON_PREREG_2026-08-31.json",
 "state/next_steps/V14_PREDICATE_DOSE_HORIZON_TRAINING_CONTRACT_2026-08-31.json",
 "state/next_steps/V14R1_PREDICATE_HORIZON_IDENTITY_RECOVERY_AMENDMENT_2026-08-31.json",
 "state/qualification/V14_PREDICATE_HORIZON_STATIC_HOSTILE_2026-08-31.json",
 "state/qualification/V14_PREDICATE_HORIZON_BASELINE_INHERITANCE_20260831.json",
 "state/analysis/V13_OPTIMIZER_INTERFERENCE_FINAL_DISPOSITION_2026-08-31.json",
 "state/analysis/V14_PREDICATE_HORIZON_IDENTITY_INVALIDATION_2026-08-31.json",
 "tools/audit_v14_predicate_horizon_candidate.py","tools/v14_predicate_horizon_common.py",
 "tools/train_v14_predicate_horizon.py","tools/evaluate_v14_predicate_horizon.py",
 "tools/run_v14_predicate_horizon_campaign.py","tools/prepare_v14_predicate_horizon_runtime.py",
 "tools/qualify_v14_predicate_horizon_repeatability.py","tools/finalize_v14r1_predicate_horizon_preexecution.py",
 "tools/lock_v14r1_predicate_horizon.py"]
 cand=root/"state/candidates/v14_predicate_horizon_20260831"
 for p in sorted(cand.iterdir()):
  if p.is_file(): rels.append(p.relative_to(root).as_posix())
 files={}
 for rel in rels:
  p=root/rel
  if not p.is_file():raise SystemExit("MISSING "+rel)
  files[rel]={"bytes":p.stat().st_size,"sha256":H(p)}
 lock={"schema":"cfe.v14r1.predicate-horizon-input-lock.v1","status":"V14R1_LOCKED_PRE_RUNTIME__NO_SCIENTIFIC_TRAINING","file_count":len(files),"files":files,"anchors":{"preregistration_sha256":files["state/next_steps/V14_PREDICATE_DOSE_HORIZON_PREREG_2026-08-31.json"]["sha256"],"training_contract_sha256":files["state/next_steps/V14_PREDICATE_DOSE_HORIZON_TRAINING_CONTRACT_2026-08-31.json"]["sha256"],"recovery_amendment_sha256":files["state/next_steps/V14R1_PREDICATE_HORIZON_IDENTITY_RECOVERY_AMENDMENT_2026-08-31.json"]["sha256"],"current_v13_final_disposition_sha256":files["state/analysis/V13_OPTIMIZER_INTERFERENCE_FINAL_DISPOSITION_2026-08-31.json"]["sha256"],"candidate_manifest_sha256":files["state/candidates/v14_predicate_horizon_20260831/MANIFEST.json"]["sha256"]},"scientific_training_authorized":False,"scientific_difference":"developmental exposure horizon only; recovery identity changes provenance anchor only","mutation_rule":"Any locked-byte change invalidates V14R1 and requires another identity.","excluded_prior_outputs":"All state/analysis/V14_PREDICATE_HORIZON_CAMPAIGN_* outputs are provenance-only and cannot enter V14R1 science."}
 if out.exists():raise SystemExit("REFUSE_OVERWRITE")
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(lock,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n");print(json.dumps({"status":lock["status"],"file_count":len(files),"lock_sha256":H(out)},indent=2))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--root",type=Path,default=Path.cwd());ap.add_argument("--out",type=Path,required=True);a=ap.parse_args();main(a.root.resolve(),a.out)
