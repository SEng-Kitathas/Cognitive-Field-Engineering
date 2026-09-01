from __future__ import annotations
import json,hashlib,random,os
from pathlib import Path
ARMS=('CYCLIC_SPACED','WINDOW_MASSED')
def sha256_file(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def loadj(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def loadjl(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def dumpj(p,o):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def dumpjl(p,rows):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text('\n'.join(json.dumps(r,sort_keys=True,separators=(',',':')) for r in rows)+'\n',encoding='utf-8',newline='\n')
def chatml(ms,gen=False):
 s=''.join(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in ms)
 if gen:s+='<|im_start|>assistant\n'
 return s
def schedule_for(candidate_manifest,seed,arm):
 order=candidate_manifest['schedules'][str(seed)]['order'];wins=[order[i:i+8] for i in range(0,72,8)]
 if len(wins)!=9 or any(len(w)!=8 for w in wins):raise RuntimeError('WINDOW_SHAPE_FAIL')
 wseq=[w for _ in range(16) for w in range(9)] if arm=='CYCLIC_SPACED' else [w for w in range(9) for _ in range(16)]
 return [r for wi in wseq for r in wins[wi]],wseq,wins
def configure_determinism(seed):
 os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
 import numpy as np,torch
 random.seed(seed);np.random.seed(seed%(2**32));torch.manual_seed(seed);torch.cuda.manual_seed_all(seed);torch.use_deterministic_algorithms(True);torch.set_deterministic_debug_mode('error');torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True;torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 return {'seed':seed,'deterministic_algorithms':True,'cublas_workspace_config':os.environ.get('CUBLAS_WORKSPACE_CONFIG')}
def hash_trainable_parameters(model):
 h=hashlib.sha256();n=0
 for name,p in sorted(model.named_parameters(),key=lambda x:x[0]):
  if p.requires_grad:
   a=p.detach().float().cpu().contiguous().numpy();h.update(name.encode());h.update(b'\0');h.update(a.tobytes());n+=p.numel()
 return h.hexdigest(),int(n)
def parse_json_output(raw):
 raw=raw.strip();raw=raw.split('<|im_end|>',1)[0].strip() if '<|im_end|>' in raw else raw;raw=raw.strip('`').strip()
 try:return json.loads(raw)
 except:pass
 for i,c in enumerate(raw):
  if c not in '[{':continue
  for j in range(len(raw),i,-1):
   if raw[j-1] not in ']}':continue
   try:return json.loads(raw[i:j])
   except:pass
 return None
