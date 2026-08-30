#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, random, statistics, time
from collections import defaultdict
from pathlib import Path

FAMILIES=("bounded_transport","warrant_vs_taint")

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def loadjl(p:Path): return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]

def configure(seed:int):
    import torch, numpy as np
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark=False
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--live-root',type=Path,required=True)
    ap.add_argument('--run-root',type=Path,required=True)
    ap.add_argument('--arm',required=True)
    ap.add_argument('--seed',type=int,default=2026082501)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--row-indices',type=str,default='')
    a=ap.parse_args()
    if a.out.exists(): raise SystemExit('REFUSE_OVERWRITE')
    a.out.parent.mkdir(parents=True,exist_ok=True)
    live=a.live_root; run=a.run_root
    host=json.loads((run/'host/HOST_LOCK.json').read_text(encoding='utf-8'))
    plock=json.loads((run/'profile/PROFILE_LOCK.json').read_text(encoding='utf-8'))
    contract=json.loads((live/'experiments/first_screen_v09/training_contract.json').read_text(encoding='utf-8'))
    profile=plock['selected_profile']; opt=contract['optimization']
    side=loadjl(live/'pilot/first_screen_v09'/f'{a.arm}.sidecar.private.jsonl')
    rows=loadjl(live/'pilot/first_screen_v09'/f'{a.arm}.jsonl')
    refs=loadjl(live/'pilot/first_screen_v09/token_reference_q3'/f'{a.arm}.token_reference.private.jsonl')
    if not(len(side)==len(rows)==len(refs)==72): raise AssertionError('ROW_COUNT')
    configure(a.seed)
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig,get_peft_model,prepare_model_for_kbit_training
    if not torch.cuda.is_available(): raise SystemExit('CUDA_REQUIRED')
    bnbc=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=opt['bnb_quant_type'],bnb_4bit_use_double_quant=opt['bnb_double_quant'],bnb_4bit_compute_dtype=torch.float16)
    snap=Path(host['base_snapshot_path'])
    tok=AutoTokenizer.from_pretrained(str(snap),use_fast=False,trust_remote_code=False,local_files_only=True)
    model=AutoModelForCausalLM.from_pretrained(str(snap),quantization_config=bnbc,device_map={'':0},trust_remote_code=False,attn_implementation=opt['attention_backend'])
    model.config.use_cache=False
    model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True)
    model=get_peft_model(model,LoraConfig(r=profile['r'],lora_alpha=profile['alpha'],lora_dropout=profile['dropout'],bias='none',task_type='CAUSAL_LM',target_modules=profile['targets']))
    model.train()
    params=[p for p in model.parameters() if p.requires_grad]
    pcount=sum(p.numel() for p in params)
    if pcount!=20971520: raise RuntimeError(('TRAINABLE_COUNT',pcount))
    im_end=tok.convert_tokens_to_ids('<|im_end|>'); im_start=tok.convert_tokens_to_ids('<|im_start|>')
    if (im_end,im_start)!=(32000,32001): raise RuntimeError(('SPECIAL_IDS',im_end,im_start))
    ah=tok('<|im_start|>assistant\n',add_special_tokens=False)['input_ids']
    uh=tok('<|im_start|>user\n',add_special_tokens=False)['input_ids']
    def chatml(ms): return ''.join(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in ms)
    def assistant_segments(ids):
        segs=[];i=0
        while i<len(ids):
            if ids[i:i+len(ah)]==ah:
                st=i+len(ah); en=ids.index(im_end,st); segs.append((st,en+1)); i=en+1
            else:i+=1
        return segs
    def flat_grad_cpu():
        chunks=[]
        for p in params:
            g=p.grad
            if g is None: chunks.append(torch.zeros(p.numel(),dtype=torch.float32))
            else: chunks.append(g.detach().float().reshape(-1).cpu())
        return torch.cat(chunks)
    def cosine(x,y):
        nx=float(torch.linalg.vector_norm(x)); ny=float(torch.linalg.vector_norm(y))
        return float(torch.dot(x,y)/(nx*ny)) if nx and ny else float('nan')
    selected=set(int(x) for x in a.row_indices.split(',') if x.strip()) if a.row_indices else None
    out_rows=[]; fam_summary=defaultdict(list); t0=time.time(); processed=0
    for idx,(r,s,ref) in enumerate(zip(rows,side,refs)):
        fam=s['family']
        if fam not in FAMILIES: continue
        if selected is not None and idx not in selected: continue
        ids=tok(chatml(r['messages']),add_special_tokens=True,return_attention_mask=False)['input_ids']
        if ids!=ref['input_ids']: raise RuntimeError(('TOKEN_REPLAY_MISMATCH',idx))
        segs=assistant_segments(ids)
        if len(segs)!=4: raise RuntimeError(('ASSISTANT_SEGMENTS',idx,segs))
        x=torch.tensor(ids,dtype=torch.long,device='cuda').unsqueeze(0)
        att=torch.ones_like(x)
        grads=[]; losses=[]; norms=[]
        for j,(st,en) in enumerate(segs):
            model.zero_grad(set_to_none=True)
            labels=torch.full_like(x,-100); labels[0,st:en]=x[0,st:en]
            out=model(input_ids=x,attention_mask=att,labels=labels)
            loss=out.loss
            loss.backward()
            g=flat_grad_cpu(); grads.append(g); losses.append(float(loss.detach().cpu())); norms.append(float(torch.linalg.vector_norm(g)))
            del out,loss
            torch.cuda.empty_cache()
        pair=[]
        for i in range(4):
            for j in range(i+1,4): pair.append(cosine(grads[i],grads[j]))
        mean_cos=statistics.mean(pair); neg=sum(c<0 for c in pair)
        # sum-gradient coherence: ||sum g|| / sum ||g||, in [0,1]
        gs=grads[0]+grads[1]+grads[2]+grads[3]
        coherence=float(torch.linalg.vector_norm(gs))/sum(norms)
        rec={'row_index':idx,'pair_id':s['pair_id'],'family':fam,'domain':s['domain'],'arm':a.arm,'seed':a.seed,'losses':losses,'gradient_norms':norms,'pairwise_cosines':pair,'mean_pairwise_cosine':mean_cos,'negative_pair_count':neg,'sum_gradient_coherence':coherence,'member_neighborhood_ids':s['member_neighborhood_ids'],'cell_keys':s['cell_keys']}
        out_rows.append(rec); fam_summary[fam].append(rec); processed+=1
        print(json.dumps({'processed':processed,'row_index':idx,'family':fam,'mean_cos':mean_cos,'neg_pairs':neg,'coherence':coherence}),flush=True)
        del grads,gs,x,att
    summary={}
    for fam,recs in fam_summary.items():
        allc=[c for r in recs for c in r['pairwise_cosines']]
        summary[fam]={'sequences':len(recs),'pairwise_cosines':len(allc),'mean_pairwise_cosine':statistics.mean(allc),'median_pairwise_cosine':statistics.median(allc),'negative_cosine_fraction':sum(c<0 for c in allc)/len(allc),'mean_sum_gradient_coherence':statistics.mean(r['sum_gradient_coherence'] for r in recs),'mean_sequence_loss':statistics.mean(x for r in recs for x in r['losses'])}
    report={'schema':'cfe.v10.diagnostic-gradient-replay.v1','status':'DIAGNOSTIC_REPLAY_COMPLETE__NOT_HISTORICAL_GRADIENT_RECONSTRUCTION','arm':a.arm,'seed':a.seed,'families':list(FAMILIES),'selected_row_indices':sorted(selected) if selected is not None else None,'base_snapshot_manifest_sha256':host['base_snapshot_manifest_sha256'],'profile_lock_sha256':sha256_file(run/'profile/PROFILE_LOCK.json'),'source_arm_jsonl_sha256':sha256_file(live/'pilot/first_screen_v09'/f'{a.arm}.jsonl'),'source_sidecar_sha256':sha256_file(live/'pilot/first_screen_v09'/f'{a.arm}.sidecar.private.jsonl'),'trainable_parameters':pcount,'measurement':'Per-assistant-response LoRA gradient on the full frozen four-pair sequence at initialized NF4+LoRA state; loss masked to one assistant segment at a time; no optimizer steps.','interpretation_ceiling':['Measures initial-state gradient conflict potential only.','Does not reconstruct historical gradients after updates.','Post-hoc diagnostic; cannot confirm a preregistered mechanism.'],'summary':summary,'rows':out_rows,'elapsed_seconds':time.time()-t0}
    a.out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':report['status'],'summary':summary,'elapsed_seconds':report['elapsed_seconds'],'sha256':sha256_file(a.out)},indent=2,sort_keys=True))

if __name__=='__main__':main()
