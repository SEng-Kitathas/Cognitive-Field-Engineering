#!/usr/bin/env python3
from __future__ import annotations
import argparse,gc,json
from pathlib import Path
from v12_factor_primitive_common import *

def probe(snapshot,profile,contract,ref):
 import torch,bitsandbytes as bnb
 from transformers import AutoModelForCausalLM,BitsAndBytesConfig
 from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training
 det=configure_determinism(91220260830);torch.cuda.empty_cache();torch.cuda.reset_peak_memory_stats();o=contract['optimization'];bnbc=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=o['bnb_quant_type'],bnb_4bit_use_double_quant=o['bnb_double_quant'],bnb_4bit_compute_dtype=torch.float16)
 model=AutoModelForCausalLM.from_pretrained(str(snapshot),quantization_config=bnbc,device_map={'':0},trust_remote_code=False,attn_implementation=o['attention_backend'],local_files_only=True);model.config.use_cache=False;model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True);model=get_peft_model(model,LoraConfig(r=profile['r'],lora_alpha=profile['alpha'],lora_dropout=profile['dropout'],bias='none',task_type='CAUSAL_LM',target_modules=profile['targets']));init,n=hash_trainable_parameters(model)
 ids=torch.tensor([ref['input_ids']],dtype=torch.long,device='cuda');labels=torch.tensor([[tok if m else -100 for tok,m in zip(ref['input_ids'],ref['loss_mask'])]],dtype=torch.long,device='cuda');opt=bnb.optim.PagedAdamW8bit([p for p in model.parameters() if p.requires_grad],lr=o['learning_rate']);out=model(input_ids=ids,labels=labels,use_cache=False);loss=out.loss;loss.backward();opt.step();opt.zero_grad(set_to_none=True);torch.cuda.synchronize();post,pn=hash_trainable_parameters(model);lv=float(loss.detach().cpu());r={'selected_profile':profile['name'],'initial_trainable_sha256':init,'post_step_trainable_sha256':post,'loss':lv,'loss_hex':lv.hex(),'trainable_parameters':n,'post_step_trainable_parameters':pn,'tokens':ref['tokens'],'determinism':det,'peak_allocated_bytes':int(torch.cuda.max_memory_allocated()),'peak_reserved_bytes':int(torch.cuda.max_memory_reserved())};del opt,out,loss,labels,ids,model;gc.collect();torch.cuda.empty_cache();return r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();verify_lock(root,a.lock)
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 a.out.mkdir(parents=True);host=loadj(a.host_lock);contract=loadj(a.contract)
 if host.get('status')!='HOST_REVERIFIED__TOKENIZER_REPLAY_PASS__PROFILE_REPEATABILITY_PENDING':raise SystemExit('HOST_NOT_READY')
 refs=[]
 for name in ['PREDICATE_NARROW_V12','PREDICATE_IDENTIFYING_V12','POLICY_Z_SHARED']:refs.extend(loadjl(a.candidate/(name+'.token_reference.private.jsonl')))
 ref=max(refs,key=lambda r:r['tokens']);profile=host['inherited_selected_profile'];runs=[probe(Path(host['base_snapshot_path']),profile,contract,ref) for _ in range(2)];keys=['selected_profile','initial_trainable_sha256','post_step_trainable_sha256','loss_hex','trainable_parameters'];mism={k:[r[k] for r in runs] for k in keys if len({json.dumps(r[k],sort_keys=True) for r in runs})!=1}
 rep={'schema':'cfe.v12.factor-primitive-repeatability.v1','status':'REPEATABILITY_PASS' if not mism else 'REPEATABILITY_FAIL','seed':91220260830,'reference_id':ref['id'],'reference_tokens':ref['tokens'],'required_equal_witnesses':keys,'mismatches':mism,'runs':runs,'input_lock_sha256':sha256_file(a.lock),'host_lock_sha256':sha256_file(a.host_lock)};dumpj(a.out/'REPEATABILITY_QUALIFICATION.json',rep)
 if mism:raise SystemExit(2)
 pl={'schema':'cfe.v12.factor-primitive-profile-lock.v1','status':'PROFILE_INHERITED_AND_REPEATABILITY_QUALIFIED','input_lock_sha256':sha256_file(a.lock),'host_lock_sha256':sha256_file(a.host_lock),'selected_profile':profile,'inheritance_from_v11_profile_lock_sha256':host['v11_profile_lock_sha256'],'inheritance_reason':f"Same exact base/runtime; v12 max {host['v12_max_tokens']} <= v11 qualified max {host['v11_qualified_max_tokens']}; fresh two-run one-step repeatability PASS.",'repeatability_qualification_sha256':sha256_file(a.out/'REPEATABILITY_QUALIFICATION.json')};dumpj(a.out/'PROFILE_LOCK.json',pl);print(json.dumps({'repeatability':rep,'profile_lock':pl},indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
