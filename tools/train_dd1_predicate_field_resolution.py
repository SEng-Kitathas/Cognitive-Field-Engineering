#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from dd1_predicate_field_resolution_common import *
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--arm',choices=ARMS,required=True);ap.add_argument('--seed',type=int,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve()
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 a.out.mkdir(parents=True);verify_lock(root,a.lock);c=loadj(a.contract);host=loadj(a.host_lock);prof=loadj(a.profile_lock)
 if a.seed not in c['seeds'] or a.arm not in c['arms']:raise SystemExit('NOT_FROZEN')
 if sha256_file(a.candidate/'MANIFEST.json')!=c['bindings']['candidate_manifest_sha256']:raise SystemExit('CANDIDATE_BINDING_FAIL')
 if sha256_file(a.host_lock)!=c['bindings']['host_lock_sha256'] or sha256_file(a.profile_lock)!=c['bindings']['profile_lock_sha256']:raise SystemExit('RUNTIME_BINDING_FAIL')
 stem=DATASET_FOR_ARM[a.arm];refs=loadjl(a.candidate/(stem+'.token_reference.private.jsonl'));man=loadj(a.candidate/'MANIFEST.json');order=man['schedules'][str(a.seed)]['order'];ordered=[refs[i] for i in order]
 import torch
 from torch.utils.data import Dataset,SequentialSampler
 from transformers import AutoModelForCausalLM,BitsAndBytesConfig,Trainer,TrainingArguments
 from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training
 det=configure_determinism(a.seed);opt=c['optimization'];seq=c['sequence'];profile=prof['selected_profile'];bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=opt['bnb_quant_type'],bnb_4bit_use_double_quant=opt['bnb_double_quant'],bnb_4bit_compute_dtype=torch.float16)
 model=AutoModelForCausalLM.from_pretrained(host['base_snapshot_path'],quantization_config=bnb,device_map={'':0},trust_remote_code=False,attn_implementation=opt['attention_backend'],local_files_only=True);model.config.use_cache=False;model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=opt['gradient_checkpointing']);model=get_peft_model(model,LoraConfig(r=profile['r'],lora_alpha=profile['alpha'],lora_dropout=profile['dropout'],bias='none',task_type='CAUSAL_LM',target_modules=profile['targets']));init_sha,ntrain=hash_trainable_parameters(model)
 class DS(Dataset):
  def __len__(self):return len(ordered)
  def __getitem__(self,i):
   r=ordered[i];ids=torch.tensor(r['input_ids'],dtype=torch.long);mask=torch.tensor(r['loss_mask'],dtype=torch.bool);labels=ids.clone();labels[~mask]=-100;return {'input_ids':ids,'attention_mask':torch.ones_like(ids),'labels':labels}
 def collate(xs):
  if len(xs)!=1:raise RuntimeError('MICROBATCH_CONTRACT')
  return {k:v.unsqueeze(0) for k,v in xs[0].items()}
 class ST(Trainer):
  def _get_train_sampler(self,train_dataset=None):return SequentialSampler(train_dataset if train_dataset is not None else self.train_dataset)
 args=TrainingArguments(output_dir=str(a.out/'trainer_tmp'),num_train_epochs=seq['epochs'],per_device_train_batch_size=1,gradient_accumulation_steps=8,learning_rate=opt['learning_rate'],lr_scheduler_type=opt['lr_scheduler_type'],warmup_ratio=0.0,weight_decay=opt['weight_decay'],max_grad_norm=opt['max_grad_norm'],optim=opt['optimizer'],fp16=True,bf16=False,gradient_checkpointing=opt['gradient_checkpointing'],logging_steps=1,save_strategy='no',do_eval=False,report_to=[],remove_unused_columns=False,dataloader_num_workers=0,dataloader_pin_memory=False,seed=a.seed,data_seed=a.seed,disable_tqdm=False)
 torch.cuda.reset_peak_memory_stats();t0=time.time();tr=ST(model=model,args=args,train_dataset=DS(),data_collator=collate);res=tr.train();torch.cuda.synchronize();elapsed=time.time()-t0
 if int(tr.state.global_step)!=144:raise RuntimeError(('GLOBAL_STEP',tr.state.global_step))
 final_sha,nfinal=hash_trainable_parameters(model);ad=a.out/'adapter';model.save_pretrained(ad,safe_serialization=True);files={p.relative_to(ad).as_posix():{'bytes':p.stat().st_size,'sha256':sha256_file(p)} for p in sorted(ad.rglob('*')) if p.is_file()};run={'schema':'cfe.dd1.train-run.v1','status':'TRAINING_COMPLETE__EFFECT_UNQUALIFIED','arm':a.arm,'seed':a.seed,'initial_trainable_sha256':init_sha,'final_trainable_sha256':final_sha,'trainable_parameters':ntrain,'final_trainable_parameters':nfinal,'global_step':int(tr.state.global_step),'contract_sha256':sha256_file(a.contract),'input_lock_sha256':sha256_file(a.lock),'candidate_manifest_sha256':sha256_file(a.candidate/'MANIFEST.json'),'token_reference_sha256':sha256_file(a.candidate/(stem+'.token_reference.private.jsonl')),'row_order_sha256':man['schedules'][str(a.seed)]['sha256'],'runtime_seconds':elapsed,'train_result':res.metrics,'adapter_files':files,'peak_allocated_bytes':int(torch.cuda.max_memory_allocated()),'peak_reserved_bytes':int(torch.cuda.max_memory_reserved()),'determinism':det};dumpj(a.out/'RUN_MANIFEST.json',run);print(json.dumps(run,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
