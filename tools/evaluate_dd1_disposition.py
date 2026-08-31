#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def L(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--aggregate',type=Path,required=True);ap.add_argument('--prereg',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();agg=L(a.aggregate);pr=L(a.prereg)
 if agg.get('status')!='COMPLETE_6_OF_6':raise SystemExit('AGGREGATE_NOT_COMPLETE_6_OF_6')
 rows=agg['per_seed'];
 if len(rows)!=6:raise SystemExit('SIX_SEEDS_REQUIRED')
 mean_delta=sum(r['delta_ba'] for r in rows)/6
 wins=sum(r['delta_ba']>0 for r in rows); losses=sum(r['delta_ba']<0 for r in rows);ties=6-wins-losses
 mi=sum(r['identifying_ba'] for r in rows)/6; md=sum(r['dispersed_ba'] for r in rows)/6
 fi=sum(r['identifying_false'] for r in rows)/6; fd=sum(r['dispersed_false'] for r in rows)/6
 ti=sum(r['identifying_true'] for r in rows)/6; td=sum(r['dispersed_true'] for r in rows)/6
 twos=sum(r['identifying_false']>=.65 and r['identifying_true']>=.65 for r in rows)
 supported=(mean_delta>0 and wins>=4 and fi>=fd-.05 and ti>=td-.05)
 strong=(supported and mi>=.75 and twos>=4)
 not_supported=(mean_delta<=0 or wins<=2)
 if strong:disp='FIELD_RESOLUTION_STRONGLY_SUPPORTED'
 elif supported:disp='FIELD_RESOLUTION_SUPPORTED'
 elif not_supported:disp='FIELD_RESOLUTION_NOT_SUPPORTED'
 else:disp='MIXED_OR_RELATION_FAMILY_DEPENDENT'
 out={'schema':'cfe.dd1.disposition.v1','status':'MECHANICALLY_EVALUATED','identity':agg.get('identity'),'disposition':disp,'criteria':{'mean_delta_gt_0':mean_delta>0,'identifying_wins_ge_4':wins>=4,'false_noninferiority_within_005':fi>=fd-.05,'true_noninferiority_within_005':ti>=td-.05,'identifying_mean_ba_ge_075':mi>=.75,'identifying_two_sided_ge_065_ge_4':twos>=4,'not_supported_trigger':not_supported},'metrics':{'mean_identifying_ba':mi,'mean_dispersed_ba':md,'mean_delta_ba':mean_delta,'identifying_wins':wins,'dispersed_wins':losses,'ties':ties,'mean_identifying_false':fi,'mean_dispersed_false':fd,'mean_identifying_true':ti,'mean_dispersed_true':td,'identifying_two_sided_ge_065':twos},'prereg_rules':pr['decision_rules'],'interpretation_guards':pr['interpretation_guards']}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
