#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from v14_predicate_horizon_common import *
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--project-root",type=Path,required=True);ap.add_argument("--candidate",type=Path,required=True);ap.add_argument("--seed",type=int,required=True);ap.add_argument("--contract",type=Path,required=True);ap.add_argument("--lock",type=Path,required=True);ap.add_argument("--host-lock",type=Path,required=True);ap.add_argument("--profile-lock",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve()
 if a.out.exists():raise SystemExit("REFUSE_OVERWRITE")
 a.out.mkdir(parents=True);verify_lock(root,a.lock);contract=loadj(a.contract);host=loadj(a.host_lock);prof=loadj(a.profile_lock)
 if a.seed not in contract["seeds"]:raise SystemExit("SEED_NOT_FROZEN")
 if sha256_file(a.candidate/"MANIFEST.json")!=contract["bindings"]["candidate_manifest_sha256"]:raise SystemExit("CANDIDATE_BINDING_FAIL")
 if prof.get("status")!="PROFILE_INHERITED_AND_V14_REPEATABILITY_QUALIFIED" or prof.get("input_lock_sha256")!=sha256_file(a.lock) or prof.get("host_lock_sha256")!=sha256_file(a.host_lock):raise SystemExit("PROFILE_BINDING_FAIL")
 rows=loadjl(a.candidate/(DATASET+".token_reference.private.jsonl"));order,order_sha=load_order(a.candidate,a.seed);ordered=[rows[i] for i in order]
 import torch
 from torch.utils.data import Dataset,SequentialSampler
 from transformers import AutoModelForCausalLM,BitsAndBytesConfig,Trainer,TrainingArguments,TrainerCallback
 from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training
 det=configure_determinism(a.seed);opt=contract["optimization"];seq=contract["sequence"];profile=prof["selected_profile"];bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=opt["bnb_quant_type"],bnb_4bit_use_double_quant=opt["bnb_double_quant"],bnb_4bit_compute_dtype=torch.float16)
 model=AutoModelForCausalLM.from_pretrained(host["base_snapshot_path"],quantization_config=bnb,device_map={"":0},trust_remote_code=False,attn_implementation=opt["attention_backend"],local_files_only=True);model.config.use_cache=False;model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=opt["gradient_checkpointing"]);model=get_peft_model(model,LoraConfig(r=profile["r"],lora_alpha=profile["alpha"],lora_dropout=profile["dropout"],bias="none",task_type="CAUSAL_LM",target_modules=profile["targets"]));init_sha,ntrain=hash_trainable_parameters(model)
 class DS(Dataset):
  def __len__(self):return len(ordered)
  def __getitem__(self,i):
   r=ordered[i];ids=torch.tensor(r["input_ids"],dtype=torch.long);mask=torch.tensor(r["loss_mask"],dtype=torch.bool);labels=ids.clone();labels[~mask]=-100;return {"input_ids":ids,"attention_mask":torch.ones_like(ids),"labels":labels}
 def collate(xs):
  if len(xs)!=1:raise RuntimeError("MICROBATCH_CONTRACT")
  return {k:v.unsqueeze(0) for k,v in xs[0].items()}
 class SeqTrainer(Trainer):
  def _get_train_sampler(self,train_dataset=None):return SequentialSampler(train_dataset if train_dataset is not None else self.train_dataset)
 saved={}
 step_to_name={v:k for k,v in HORIZONS.items()}
 class HorizonSaver(TrainerCallback):
  def on_step_end(self,args,state,control,**kwargs):
   step=int(state.global_step)
   if step in step_to_name and step_to_name[step] not in saved:
    name=step_to_name[step];dest=a.out/"checkpoints"/name/"adapter";kwargs["model"].save_pretrained(dest,safe_serialization=True);hs,n=hash_trainable_parameters(kwargs["model"]);files={p.relative_to(dest).as_posix():{"bytes":p.stat().st_size,"sha256":sha256_file(p)} for p in sorted(dest.rglob("*")) if p.is_file()};saved[name]={"global_step":step,"trainable_sha256":hs,"trainable_parameters":n,"adapter_files":files}
   return control
 args=TrainingArguments(output_dir=str(a.out/"trainer_tmp"),overwrite_output_dir=False,num_train_epochs=seq["epochs"],per_device_train_batch_size=seq["microbatch"],gradient_accumulation_steps=seq["gradient_accumulation_steps"],learning_rate=opt["learning_rate"],lr_scheduler_type=opt["lr_scheduler_type"],warmup_ratio=0.0,weight_decay=opt["weight_decay"],max_grad_norm=opt["max_grad_norm"],optim=opt["optimizer"],fp16=True,bf16=False,gradient_checkpointing=opt["gradient_checkpointing"],logging_steps=1,save_strategy="no",do_eval=False,report_to=[],remove_unused_columns=False,dataloader_num_workers=0,dataloader_pin_memory=False,seed=a.seed,data_seed=a.seed,disable_tqdm=False)
 torch.cuda.reset_peak_memory_stats();t0=time.time();trainer=SeqTrainer(model=model,args=args,train_dataset=DS(),data_collator=collate,callbacks=[HorizonSaver()]);result=trainer.train();torch.cuda.synchronize();elapsed=time.time()-t0
 if int(trainer.state.global_step)!=144:raise RuntimeError(("GLOBAL_STEP",trainer.state.global_step,144))
 if set(saved)!=set(HORIZONS):raise RuntimeError(("MISSING_HORIZON_CHECKPOINT",saved.keys()))
 final_sha,nfinal=hash_trainable_parameters(model);run={"schema":"cfe.v14.predicate-horizon-train-run.v1","status":"TRAINING_EXECUTED__SCIENTIFIC_EFFECT_UNQUALIFIED","seed":a.seed,"dataset":DATASET,"input_lock_sha256":sha256_file(a.lock),"host_lock_sha256":sha256_file(a.host_lock),"profile_lock_sha256":sha256_file(a.profile_lock),"contract_sha256":sha256_file(a.contract),"candidate_manifest_sha256":sha256_file(a.candidate/"MANIFEST.json"),"token_reference_sha256":sha256_file(a.candidate/(DATASET+".token_reference.private.jsonl")),"base_snapshot_manifest_sha256":host["base_snapshot_manifest_sha256"],"profile":profile,"determinism":det,"initial_trainable_sha256":init_sha,"initial_trainable_parameters":ntrain,"final_trainable_sha256":final_sha,"final_trainable_parameters":nfinal,"row_order":order,"row_order_sha256":order_sha,"global_step":int(trainer.state.global_step),"train_runtime_seconds":elapsed,"train_result":result.metrics,"log_history":trainer.state.log_history,"peak_allocated_bytes":int(torch.cuda.max_memory_allocated()),"peak_reserved_bytes":int(torch.cuda.max_memory_reserved()),"checkpoints":saved}
 dumpj(a.out/"RUN_MANIFEST.json",run);print(json.dumps(run,indent=2,sort_keys=True),flush=True)
if __name__=="__main__":main()
