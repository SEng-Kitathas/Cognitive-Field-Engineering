#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, time
from pathlib import Path
from v12_factor_primitive_common import *

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--arm',choices=ARMS,required=True);ap.add_argument('--seed',type=int,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve()
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 a.out.mkdir(parents=True);lock=verify_lock(root,a.lock);contract=loadj(a.contract);host=loadj(a.host_lock);prof=loadj(a.profile_lock)
 if a.seed not in contract['seeds']:raise SystemExit('SEED_NOT_FROZEN')
 if prof.get('status')!='PROFILE_INHERITED_AND_REPEATABILITY_QUALIFIED' or prof.get('input_lock_sha256')!=sha256_file(a.lock) or prof.get('host_lock_sha256')!=sha256_file(a.host_lock):raise SystemExit('PROFILE_BINDING_FAIL')
 pred_name=DATASET_FOR_ARM[a.arm];pred=loadjl(a.candidate/(pred_name+'.token_reference.private.jsonl'));pol=loadjl(a.candidate/(POLICY_DATASET+'.token_reference.private.jsonl'))
 if len(pred)!=72 or len(pol)!=72:raise SystemExit('TOKENREF_COUNT')
 sched=build_logical_schedule(a.seed);ordered=[]
 for kind,ix in sched:ordered.append(pred[ix] if kind=='P' else pol[ix])
 sched_sha=sha256_bytes(json.dumps(sched,separators=(',',':')).encode());expected=loadj(a.candidate/'TOKEN_SCHEDULE_AUDIT.json')['schedules'][str(a.seed)]['sha256']
 if sched_sha!=expected:raise SystemExit(('SCHEDULE_SHA_MISMATCH',sched_sha,expected))
 import torch
 from torch.utils.data import Dataset,SequentialSampler
 from transformers import AutoModelForCausalLM,BitsAndBytesConfig,Trainer,TrainingArguments
 from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training
 det=configure_determinism(a.seed);optc=contract['optimization'];seq=contract['sequence'];profile=prof['selected_profile'];bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=optc['bnb_quant_type'],bnb_4bit_use_double_quant=optc['bnb_double_quant'],bnb_4bit_compute_dtype=torch.float16)
 model=AutoModelForCausalLM.from_pretrained(host['base_snapshot_path'],quantization_config=bnb,device_map={'':0},trust_remote_code=False,attn_implementation=optc['attention_backend'],local_files_only=True)
 if getattr(model.config,'_attn_implementation',optc['attention_backend'])!=optc['attention_backend']:raise RuntimeError('ATTENTION_BACKEND_MISMATCH')
 model.config.use_cache=False;model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=optc['gradient_checkpointing']);model=get_peft_model(model,LoraConfig(r=profile['r'],lora_alpha=profile['alpha'],lora_dropout=profile['dropout'],bias='none',task_type='CAUSAL_LM',target_modules=profile['targets']))
 init_sha,ntrain=hash_trainable_parameters(model)
 class DS(Dataset):
  def __len__(self):return len(ordered)
  def __getitem__(self,i):
   r=ordered[i];ids=torch.tensor(r['input_ids'],dtype=torch.long);mask=torch.tensor(r['loss_mask'],dtype=torch.bool);labels=ids.clone();labels[~mask]=-100;return {'input_ids':ids,'attention_mask':torch.ones_like(ids),'labels':labels}
 def collate(xs):
  if len(xs)!=1:raise RuntimeError('MICROBATCH_CONTRACT')
  return {k:v.unsqueeze(0) for k,v in xs[0].items()}
 class SeqTrainer(Trainer):
  def _get_train_sampler(self,train_dataset=None):return SequentialSampler(train_dataset if train_dataset is not None else self.train_dataset)
 args=TrainingArguments(output_dir=str(a.out/'trainer_tmp'),overwrite_output_dir=False,num_train_epochs=seq['epochs'],per_device_train_batch_size=seq['microbatch'],gradient_accumulation_steps=seq['gradient_accumulation_steps'],learning_rate=optc['learning_rate'],lr_scheduler_type=optc['lr_scheduler_type'],warmup_ratio=0.0,weight_decay=optc['weight_decay'],max_grad_norm=optc['max_grad_norm'],optim=optc['optimizer'],fp16=True,bf16=False,gradient_checkpointing=optc['gradient_checkpointing'],logging_steps=1,save_strategy='no',do_eval=False,report_to=[],remove_unused_columns=False,dataloader_num_workers=0,dataloader_pin_memory=False,seed=a.seed,data_seed=a.seed,disable_tqdm=False)
 torch.cuda.reset_peak_memory_stats();t0=time.time();trainer=SeqTrainer(model=model,args=args,train_dataset=DS(),data_collator=collate);result=trainer.train();torch.cuda.synchronize();elapsed=time.time()-t0
 if int(trainer.state.global_step)!=int(seq['expected_optimizer_steps']):raise RuntimeError(('GLOBAL_STEP',trainer.state.global_step,seq['expected_optimizer_steps']))
 adapter=a.out/'adapter';model.save_pretrained(adapter,safe_serialization=True);final_sha,nfinal=hash_trainable_parameters(model);files={p.relative_to(adapter).as_posix():{'bytes':p.stat().st_size,'sha256':sha256_file(p)} for p in sorted(adapter.rglob('*')) if p.is_file()}
 run={'schema':'cfe.v12.factor-primitive-train-run.v1','status':'TRAINING_EXECUTED__SCIENTIFIC_EFFECT_UNQUALIFIED','arm':a.arm,'seed':a.seed,'predicate_dataset':pred_name,'policy_dataset':POLICY_DATASET,'input_lock_sha256':sha256_file(a.lock),'host_lock_sha256':sha256_file(a.host_lock),'profile_lock_sha256':sha256_file(a.profile_lock),'contract_sha256':sha256_file(a.contract),'candidate_manifest_sha256':sha256_file(a.candidate/'MANIFEST.json'),'predicate_token_reference_sha256':sha256_file(a.candidate/(pred_name+'.token_reference.private.jsonl')),'policy_token_reference_sha256':sha256_file(a.candidate/(POLICY_DATASET+'.token_reference.private.jsonl')),'base_snapshot_manifest_sha256':host['base_snapshot_manifest_sha256'],'profile':profile,'determinism':det,'initial_trainable_sha256':init_sha,'initial_trainable_parameters':ntrain,'final_trainable_sha256':final_sha,'final_trainable_parameters':nfinal,'logical_schedule':sched,'logical_schedule_sha256':sched_sha,'global_step':int(trainer.state.global_step),'expected_global_step':seq['expected_optimizer_steps'],'train_runtime_seconds':elapsed,'train_result':result.metrics,'log_history':trainer.state.log_history,'peak_allocated_bytes':int(torch.cuda.max_memory_allocated()),'peak_reserved_bytes':int(torch.cuda.max_memory_reserved()),'adapter_files':files}
 dumpj(a.out/'RUN_MANIFEST.json',run);print(json.dumps(run,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
