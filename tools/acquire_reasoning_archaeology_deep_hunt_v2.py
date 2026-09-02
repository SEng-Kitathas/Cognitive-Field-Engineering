#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, time
from pathlib import Path
import requests

SOURCES = [
  ("1977_mitchell_version_spaces","https://www.ijcai.org/Proceedings/77-1/Papers/048.pdf","1977_Mitchell_Version_Spaces.pdf"),
  ("1977_hearsay_focus_attention","https://www.ijcai.org/Proceedings/77-1/Papers/004.pdf","1977_Hayes_Roth_Lesser_HEARSAY_Focus.pdf"),
  ("1979_reid_multiple_hypothesis_tracking","https://graphics.stanford.edu/courses/cs428-03-spring/Papers/readings/CollaborativeProcessing/Reid_MHT_ieee_trans_ac_1979.pdf","1979_Reid_Multiple_Hypothesis_Tracking.pdf"),
  ("1986_dekleer_atms","https://www.dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf","1986_deKleer_ATMS.pdf"),
  ("1986_dekleer_problem_solving_atms","https://www.dekleer.org/Publications/Problem%20Solving%20with%20the%20ATMS.pdf","1986_deKleer_Problem_Solving_ATMS.pdf"),
  ("1986_dekleer_back_to_backtracking","https://www.dekleer.org/Publications/Back%20to%20Backtracking.pdf","1986_deKleer_Williams_Back_to_Backtracking.pdf"),
  ("1987_dekleer_williams_gde","https://www.dekleer.org/Publications/gde-2006.pdf","1987_deKleer_Williams_GDE_reprint.pdf"),
  ("1987_soar_knowledge_level_learning","https://cdn.aaai.org/AAAI/1987/AAAI87-089.pdf","1987_Rosenbloom_Laird_Newell_Knowledge_Level_Learning_Soar.pdf"),
  ("1993_ginsberg_dynamic_backtracking","https://arxiv.org/pdf/cs/9308101","1993_Ginsberg_Dynamic_Backtracking.pdf"),
  ("1993_prosser_conflict_backjumping","https://cse.unl.edu/~choueiry/Documents/Hybrid-Prosser.pdf","1993_Prosser_Hybrid_CSP.pdf"),
  ("1996_grasp_sat","https://homepage.cs.uiowa.edu/~tinelli/classes/295/Spring03/papers/Sil96.pdf","1996_MarquesSilva_Sakallah_GRASP.pdf"),
  ("2009_settles_active_learning","https://minds.wisconsin.edu/bitstream/handle/1793/60660/TR1648.pdf","2009_Settles_Active_Learning_Survey.pdf"),
  ("2024_belief_r","https://aclanthology.org/2024.emnlp-main.586.pdf","2024_Belief_R.pdf"),
  ("2024_llm_rational_metareasoning","https://arxiv.org/pdf/2410.05563","2024_Rational_Metareasoning_LLM.pdf"),
  ("2025_hypothesis_driven_tom","https://arxiv.org/pdf/2502.11881","2025_Hypothesis_Driven_ToM.pdf"),
  ("2025_active_reasoning_arbench","https://raw.githubusercontent.com/mlresearch/v267/main/assets/zhou25e/zhou25e.pdf","2025_AR_Bench.pdf"),
  ("2025_kup_knowledge_update","https://aclanthology.org/2025.findings-acl.1326.pdf","2025_KUP_Knowledge_Update.pdf"),
  ("2026_stale_memory_validity","https://arxiv.org/pdf/2605.06527","2026_STALE.pdf"),
  ("2026_reasoning_trajectories_geometry","https://aclanthology.org/2026.acl-long.1237.pdf","2026_LLM_Reasoning_Trajectories.pdf"),
  ("2026_ctrls_latent_state_transition","https://raw.githubusercontent.com/mlresearch/v300/main/assets/wu26a/wu26a.pdf","2026_CTRLS.pdf"),
]

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--manifest',type=Path,required=True); a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True); a.manifest.parent.mkdir(parents=True,exist_ok=True)
    s=requests.Session(); s.headers['User-Agent']='CFE-Reasoning-Archaeology/2.0 research-cache'
    rows=[]
    for sid,url,fn in SOURCES:
        p=a.out/fn; rec={'id':sid,'url':url,'path':str(p)}
        try:
            if p.exists() and p.stat().st_size>1000:
                rec.update(status='EXISTING_VERIFIED',bytes=p.stat().st_size,sha256=sha256(p))
            else:
                r=s.get(url,timeout=(20,180),allow_redirects=True,stream=True); r.raise_for_status()
                ctype=(r.headers.get('content-type') or '').lower(); tmp=p.with_suffix(p.suffix+'.part')
                with tmp.open('wb') as f:
                    for chunk in r.iter_content(1024*1024):
                        if chunk: f.write(chunk)
                if tmp.stat().st_size < 1000: raise RuntimeError('download too small')
                head=tmp.read_bytes()[:5]
                if head != b'%PDF-': raise RuntimeError(f'not PDF magic: {head!r}; content-type={ctype}')
                tmp.replace(p)
                rec.update(status='DOWNLOADED_VERIFIED',bytes=p.stat().st_size,sha256=sha256(p),content_type=ctype,final_url=r.url)
        except Exception as e:
            rec.update(status='ERROR',error=repr(e)); part=p.with_suffix(p.suffix+'.part');
            if part.exists(): part.unlink()
        rows.append(rec); print(json.dumps(rec,sort_keys=True),flush=True)
    m={'schema':'cfe.reasoning-archaeology.deep-hunt-cache.v2','created_unix':time.time(),'policy':'LOCAL_RESEARCH_CACHE_NOT_FOR_GIT_PUBLICATION','count':len(rows),'success':sum(x['status']!='ERROR' for x in rows),'errors':sum(x['status']=='ERROR' for x in rows),'items':rows}
    a.manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'manifest':str(a.manifest),'success':m['success'],'errors':m['errors']},indent=2))
if __name__=='__main__': main()
