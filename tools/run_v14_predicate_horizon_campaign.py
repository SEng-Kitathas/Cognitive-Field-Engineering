#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess,sys,time
from pathlib import Path
from v14_predicate_horizon_common import *
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--project-root",type=Path,required=True);ap.add_argument("--candidate",type=Path,required=True);ap.add_argument("--contract",type=Path,required=True);ap.add_argument("--lock",type=Path,required=True);ap.add_argument("--host-lock",type=Path,required=True);ap.add_argument("--profile-lock",type=Path,required=True);ap.add_argument("--preexec",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();contract=loadj(a.contract);verify_lock(root,a.lock);pre=loadj(a.preexec)
 if pre.get("status")!="V14_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED":raise SystemExit("PREEXEC_NOT_AUTHORIZED")
 if a.out.exists():raise SystemExit("REFUSE_EXISTING_CAMPAIGN_ROOT")
 a.out.mkdir(parents=True);receipt={"schema":"cfe.v14.predicate-horizon-campaign.v1","status":"RUNNING","started":time.time(),"input_lock_sha256":sha256_file(a.lock),"preexec_sha256":sha256_file(a.preexec),"jobs":[]};dumpj(a.out/"CAMPAIGN_RECEIPT.json",receipt)
 for seed in contract["seeds"]:
  job=a.out/str(seed);tr=job/"train";print("TRAIN",seed,flush=True);cmd=[sys.executable,str(root/"tools/train_v14_predicate_horizon.py"),"--project-root",str(root),"--candidate",str(a.candidate),"--seed",str(seed),"--contract",str(a.contract),"--lock",str(a.lock),"--host-lock",str(a.host_lock),"--profile-lock",str(a.profile_lock),"--out",str(tr)];cp=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors="replace");job.mkdir(parents=True,exist_ok=True);(job/"train.stdout.log").write_text(cp.stdout,encoding="utf-8");(job/"train.stderr.log").write_text(cp.stderr,encoding="utf-8")
  if cp.returncode!=0:receipt["status"]="BLOCKED";receipt["jobs"].append({"seed":seed,"status":"TRAIN_FAILED","rc":cp.returncode,"stderr_tail":cp.stderr[-5000:]});dumpj(a.out/"CAMPAIGN_RECEIPT.json",receipt);raise SystemExit(cp.returncode)
  evals={}
  for h in ["H1","H2","H4"]:
   ev=job/h/"eval";print("EVAL",seed,h,flush=True);cmd=[sys.executable,str(root/"tools/evaluate_v14_predicate_horizon.py"),"--project-root",str(root),"--candidate",str(a.candidate),"--seed",str(seed),"--horizon",h,"--adapter",str(tr/"checkpoints"/h/"adapter"),"--run-manifest",str(tr/"RUN_MANIFEST.json"),"--contract",str(a.contract),"--lock",str(a.lock),"--host-lock",str(a.host_lock),"--out",str(ev)];ep=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors="replace");(job/h).mkdir(parents=True,exist_ok=True);(job/h/"eval.stdout.log").write_text(ep.stdout,encoding="utf-8");(job/h/"eval.stderr.log").write_text(ep.stderr,encoding="utf-8")
   if ep.returncode!=0:receipt["status"]="BLOCKED";receipt["jobs"].append({"seed":seed,"status":"EVAL_FAILED","horizon":h,"rc":ep.returncode,"stderr_tail":ep.stderr[-5000:]});dumpj(a.out/"CAMPAIGN_RECEIPT.json",receipt);raise SystemExit(ep.returncode)
   em=loadj(ev/"EVAL_MANIFEST.json");m=em["metrics"]["PREDICATE_DIRECT"];evals[h]={"eval_manifest_sha256":sha256_file(ev/"EVAL_MANIFEST.json"),"balanced_accuracy":m["balanced_accuracy"],"overall_accuracy":m["overall"]["accuracy"],"false_accuracy":m["by_truth"]["false"]["accuracy"],"true_accuracy":m["by_truth"]["true"]["accuracy"]}
  receipt["jobs"].append({"seed":seed,"status":"COMPLETE","run_manifest_sha256":sha256_file(tr/"RUN_MANIFEST.json"),"horizons":evals});dumpj(a.out/"CAMPAIGN_RECEIPT.json",receipt)
 # aggregate
 seeds=contract["seeds"];agg={"schema":"cfe.v14.predicate-horizon-aggregate.v1","status":"COMPLETE__HOSTILE_INTERPRETATION_REQUIRED","seeds":{},"summary":{},"dispositions":{}}
 vals={h:[] for h in HORIZONS};false={h:[] for h in HORIZONS};true={h:[] for h in HORIZONS};overall={h:[] for h in HORIZONS}
 for seed in seeds:
  agg["seeds"][str(seed)]={}
  for h in HORIZONS:
   m=loadj(a.out/str(seed)/h/"eval"/"EVAL_MANIFEST.json")["metrics"]["PREDICATE_DIRECT"];agg["seeds"][str(seed)][h]=m;vals[h].append(m["balanced_accuracy"]);false[h].append(m["by_truth"]["false"]["accuracy"]);true[h].append(m["by_truth"]["true"]["accuracy"]);overall[h].append(m["overall"]["accuracy"])
 d41=[vals["H4"][i]-vals["H1"][i] for i in range(6)];d21=[vals["H2"][i]-vals["H1"][i] for i in range(6)];d24=[vals["H2"][i]-vals["H4"][i] for i in range(6)]
 mean=lambda xs:sum(xs)/len(xs);pool=lambda xs:mean(xs)
 h4_improves=mean(d41)>0 and sum(x>0 for x in d41)>=4 and pool(false["H4"])>=pool(false["H1"]) and pool(true["H4"])>=pool(true["H1"]) and mean(vals["H4"])>=0.75 and sum(x>=0.65 for x in false["H4"])>=4 and sum(x>=0.65 for x in true["H4"])>=4 and sum(x>=0.75 for x in overall["H4"])>=4
 h2_opt=mean(d21)>0 and mean(d24)>0 and sum(x>0 for x in d21)>=4 and mean(vals["H2"])>=0.75 and sum(x>=0.65 for x in false["H2"])>=4 and sum(x>=0.65 for x in true["H2"])>=4 and sum(x>=0.75 for x in overall["H2"])>=4
 two_sided_h2=sum(false["H2"][i]>=0.65 and true["H2"][i]>=0.65 for i in range(6));two_sided_h4=sum(false["H4"][i]>=0.65 and true["H4"][i]>=0.65 for i in range(6));rotation=(abs(pool(false["H2"])-pool(false["H1"]))>=0.20 or abs(pool(true["H2"])-pool(true["H1"]))>=0.20 or abs(pool(false["H4"])-pool(false["H1"]))>=0.20 or abs(pool(true["H4"])-pool(true["H1"]))>=0.20) and not (h4_improves or h2_opt);weak=(not h4_improves) and (not h2_opt) and two_sided_h2<4 and two_sided_h4<4
 agg["summary"]={"balanced_accuracy_by_horizon":{h:{"seed_values":vals[h],"mean":mean(vals[h])} for h in HORIZONS},"false_accuracy_by_horizon":{h:{"seed_values":false[h],"mean":mean(false[h])} for h in HORIZONS},"true_accuracy_by_horizon":{h:{"seed_values":true[h],"mean":mean(true[h])} for h in HORIZONS},"H4_minus_H1_seed_deltas":d41,"H4_minus_H1_mean_delta":mean(d41),"H4_wins_vs_H1":sum(x>0 for x in d41),"H2_minus_H1_seed_deltas":d21,"H2_minus_H1_mean_delta":mean(d21),"H2_wins_vs_H1":sum(x>0 for x in d21),"H2_minus_H4_mean_delta":mean(d24),"two_sided_seed_count_H2":two_sided_h2,"two_sided_seed_count_H4":two_sided_h4}
 agg["dispositions"]={"HORIZON_IMPROVES_COMPETENCE":h4_improves,"INTERMEDIATE_HORIZON_OPTIMUM":h2_opt,"DOSE_ROTATES_BASIN_WITHOUT_COMPETENCE":rotation,"DOSE_HORIZON_WEAKENED":weak,"next_branch":"HOSTILE_INTERPRETATION_REQUIRED"};dumpj(a.out/"AGGREGATE.json",agg);receipt["status"]="COMPLETE";receipt["completed"]=time.time();receipt["aggregate_sha256"]=sha256_file(a.out/"AGGREGATE.json");dumpj(a.out/"CAMPAIGN_RECEIPT.json",receipt);print(json.dumps(agg,indent=2,sort_keys=True),flush=True)
if __name__=="__main__":main()
