from __future__ import annotations
import hashlib,json,os,random
from pathlib import Path
DATASET="PREDICATE_IDENTIFYING_V12"
HORIZONS={"H1":36,"H2":72,"H4":144}
def sha256_file(p:Path)->str:
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(8*1024*1024),b""):h.update(b)
 return h.hexdigest()
def sha256_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def loadj(p):return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def loadjl(p):return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
def dumpj(p,o):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def dumpjl(p,rows):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text("\n".join(json.dumps(r,sort_keys=True,separators=(",",":")) for r in rows)+"\n",encoding="utf-8",newline="\n")
def chatml(ms,gen=False):
 s="".join(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in ms)
 if gen:s+="<|im_start|>assistant\n"
 return s
def configure_determinism(seed:int):
 os.environ["CUBLAS_WORKSPACE_CONFIG"]=":4096:8"
 import numpy as np,torch
 random.seed(seed);np.random.seed(seed%(2**32));torch.manual_seed(seed);torch.cuda.manual_seed_all(seed);torch.use_deterministic_algorithms(True);torch.set_deterministic_debug_mode("error");torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True;torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 return {"seed":seed,"numpy_seed":seed%(2**32),"deterministic_algorithms":True,"deterministic_debug_mode":2,"cublas_workspace_config":os.environ.get("CUBLAS_WORKSPACE_CONFIG"),"cudnn_benchmark":False,"cudnn_deterministic":True,"matmul_allow_tf32":False}
def hash_trainable_parameters(model):
 h=hashlib.sha256();n=0
 for name,p in sorted(model.named_parameters(),key=lambda x:x[0]):
  if not p.requires_grad:continue
  a=p.detach().float().cpu().contiguous().numpy();h.update(name.encode());h.update(b"\0");h.update(a.tobytes());n+=p.numel()
 return h.hexdigest(),int(n)
def verify_lock(root:Path,lock_path:Path):
 lock=loadj(lock_path)
 if lock.get("status")!="LOCKED_PRE_RUNTIME__NO_V14_SCIENTIFIC_TRAINING":raise SystemExit("INPUT_LOCK_STATUS_INVALID")
 fail=[]
 for rel,meta in lock["files"].items():
  p=root/rel
  if not p.is_file():fail.append((rel,"missing"));continue
  if p.stat().st_size!=meta["bytes"]:fail.append((rel,"bytes"));continue
  if sha256_file(p)!=meta["sha256"]:fail.append((rel,"sha256"))
 if fail:raise SystemExit("INPUT_LOCK_VERIFY_FAIL "+repr(fail[:10]))
 return lock
def load_order(candidate:Path,seed:int):
 m=loadj(candidate/"MANIFEST.json");node=m["schedules"][str(seed)];order=node["order"];calc=sha256_bytes(json.dumps(order,separators=(",",":")).encode())
 if calc!=node["sha256"] or sorted(order)!=list(range(72)):raise RuntimeError("SCHEDULE_INVALID")
 return order,node["sha256"]
def parse_json_output(raw:str):
 raw=raw.strip();raw=raw.split("<|im_end|>",1)[0].strip() if "<|im_end|>" in raw else raw;raw=raw.strip("`").strip()
 try:return json.loads(raw)
 except:pass
 for i,c in enumerate(raw):
  if c not in "[{":continue
  for j in range(len(raw),i,-1):
   if raw[j-1] not in "]}":continue
   try:return json.loads(raw[i:j])
   except:pass
 return None
