#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
def L(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--aggregate',type=Path,required=True);ap.add_argument('--prereg',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();g=L(a.aggregate);p=L(a.prereg)
 if g.get('status')!='COMPLETE_6_OF_6' or len(g.get('per_seed',[]))!=6:raise SystemExit('AGGREGATE_NOT_COMPLETE_6_OF_6')
 r=g['per_seed'];mean=lambda k:sum(x[k] for x in r)/6;delta=mean('delta_ba');sw=sum(x['delta_ba']>0 for x in r);mw=sum(x['delta_ba']<0 for x in r)
 sf, mf, st, mt=mean('spaced_false'),mean('massed_false'),mean('spaced_true'),mean('massed_true')
 s_sup=delta>0 and sw>=4 and sf>=mf-.05 and st>=mt-.05
 m_sup=delta<0 and mw>=4 and mf>=sf-.05 and mt>=st-.05
 null=abs(delta)<=.01 and sw<4 and mw<4
 if s_sup:d='STRUCTURED_REVISIT_SUPPORTED'
 elif m_sup:d='MASSED_REVISIT_SUPPORTED'
 elif null:d='REVISIT_TOPOLOGY_NOT_SUPPORTED'
 else:d='MIXED_OR_PATH_DEPENDENT'
 o={'schema':'cfe.dd2.revisit-disposition.v1','status':'MECHANICALLY_EVALUATED','disposition':d,'criteria':{'mean_delta':delta,'spaced_wins':sw,'massed_wins':mw,'spaced_false_noninferiority':sf>=mf-.05,'spaced_true_noninferiority':st>=mt-.05,'massed_false_noninferiority':mf>=sf-.05,'massed_true_noninferiority':mt>=st-.05,'null_trigger':null},'metrics':g['summary'],'prereg_rules':p['decision_rules'],'interpretation_guards':p['interpretation_guards']};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(o,indent=2,sort_keys=True))
if __name__=='__main__':main()
