#!/usr/bin/env python3
from __future__ import annotations
import argparse,gc,json
from pathlib import Path
from v14_predicate_horizon_common import *
def probe(snapshot,profile,contract,refs):
 import torch,bitsandbytes as bnb
 from transformers import AutoModelForCausalLM,BitsAndBytesConfig
 from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training
 det=configure_determinism(91420260831);torch.cuda.empty_cache();torch.cuda.reset_peak_memory_stats();o=contract["optimization"];bnbc=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=o["bnb_quant_type"],bnb_4bit_use_double_quant=o["bnb_double_quant"],bnb_4bit_compute_dtype=torch.float16)
 model=AutoModelForCausalLM.from_pretrained(str(snapshot),quantization_config=bnbc,device_map={"":0},trust_remote_code=False,attn_implementation=o["attention_backend"],local_files_only=True);model.config.use_cache=False;model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True);model=get_peft_model(model,LoraConfig(r=profile["r"],lora_alpha=profile["alpha"],lora_dropout=profile["dropout"],bias="none",task_type="CAUSAL_LM",target_modules=profile["targets"]));init,n=hash_trainable_parameters(model);params=[p for p in model.parameters() if p.requires_grad];opt=bnb.optim.PagedAdamW8bit(params,lr=o["learning_rate"]);losses=[]
 # exact one optimizer update over first frozen accumulation window (8 microbatches)
 for ref in refs:
  ids=torch.tensor([ref["input_ids"]],dtype=torch.long,device="cuda");labels=torch.tensor([[tok if m else -100 for tok,m in zip(ref["input_ids"],ref["loss_mask"])]],dtype=torch.long,device="cuda");out=model(input_ids=ids,labels=labels,use_cache=False);loss=out.loss/8.0;loss.backward();losses.append(float(out.loss.detach().cpu()));del out,loss,labels,ids
 opt.step();opt.zero_grad(set_to_none=True);torch.cuda.synchronize();post,pn=hash_trainable_parameters(model);r={"selected_profile":profile["name"],"initial_trainable_sha256":init,"post_step_trainable_sha256":post,"microbatch_losses_hex":[x.hex() for x in losses],"trainable_parameters":n,"post_step_trainable_parameters":pn,"tokens":[x["tokens"] for x in refs],"determinism":det,"peak_allocated_bytes":int(torch.cuda.max_memory_allocated()),"peak_reserved_bytes":int(torch.cuda.max_memory_reserved())};del opt,params,model;gc.collect();torch.cuda.empty_cache();return r
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--project-root",type=Path,required=True);ap.add_argument("--lock",type=Path,required=True);ap.add_argument("--candidate",type=Path,required=True);ap.add_argument("--contract",type=Path,required=True);ap.add_argument("--host-lock",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();verify_lock(root,a.lock)
 if a.out.exists():raise SystemExit("REFUSE_OVERWRITE")
 a.out.mkdir(parents=True);host=loadj(a.host_lock);contract=loadj(a.contract)
 if host.get("status")!="HOST_REVERIFIED__TOKENIZER_REPLAY_PASS__PROFILE_REPEATABILITY_PENDING":raise SystemExit("HOST_NOT_READY")
 allrefs=loadjl(a.candidate/(DATASET+".token_reference.private.jsonl"));order,_=load_order(a.candidate,contract["seeds"][0]);refs=[allrefs[i] for i in order[:8]];profile=host["inherited_selected_profile"];runs=[probe(Path(host["base_snapshot_path"]),profile,contract,refs) for _ in range(2)];keys=["selected_profile","initial_trainable_sha256","post_step_trainable_sha256","microbatch_losses_hex","trainable_parameters"];mism={k:[r[k] for r in runs] for k in keys if len({json.dumps(r[k],sort_keys=True) for r in runs})!=1};rep={"schema":"cfe.v14.predicate-horizon-repeatability.v1","status":"REPEATABILITY_PASS" if not mism else "REPEATABILITY_FAIL","seed":91420260831,"reference_seed_order":contract["seeds"][0],"reference_ids":[x["id"] for x in refs],"required_equal_witnesses":keys,"mismatches":mism,"runs":runs,"input_lock_sha256":sha256_file(a.lock),"host_lock_sha256":sha256_file(a.host_lock)};dumpj(a.out/"REPEATABILITY_QUALIFICATION.json",rep)
 if mism:raise SystemExit(2)
 pl={"schema":"cfe.v14.predicate-horizon-profile-lock.v1","status":"PROFILE_INHERITED_AND_V14_REPEATABILITY_QUALIFIED","input_lock_sha256":sha256_file(a.lock),"host_lock_sha256":sha256_file(a.host_lock),"selected_profile":profile,"inheritance_from_v13_profile_lock_sha256":host["source_v13_profile_lock_sha256"],"inheritance_reason":f"Same exact base/runtime; v14 max {host['v14_max_tokens']} <= v13 qualified max {host['v13_qualified_max_tokens']}; fresh two-run full-accumulation-window repeatability PASS.","repeatability_qualification_sha256":sha256_file(a.out/"REPEATABILITY_QUALIFICATION.json")};dumpj(a.out/"PROFILE_LOCK.json",pl);print(json.dumps({"repeatability":rep,"profile_lock":pl},indent=2,sort_keys=True))
if __name__=="__main__":main()
