#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, random, time
from pathlib import Path
from typing import Any

SEED = 20260902
LICENSE = ["CC0-1.0"]


def stable_json(x: Any) -> str:
    return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def htext(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def msg(role: str, content: str) -> dict[str, str]:
    return {"role": role, "content": content}


def pretty(name: str) -> str:
    return name.replace("_", " ")


def article(name: str) -> str:
    return "an" if name[:1].lower() in "aeiou" else "a"


def upper_first(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def atom(source_key: str, idx: int, family: str, subtype: str, messages: list[dict[str, str]], final: str,
         dims: list[str], hidden: dict[str, Any], packaging: str, lanes: list[str]) -> dict[str, Any]:
    first_user = next(m["content"] for m in messages if m["role"] == "user")
    conv = "\n".join(f"{m['role']}:{m['content']}" for m in messages)
    raw_basis = stable_json({"source_key": source_key, "idx": idx, "messages": messages, "final": final, "hidden": hidden})
    atom_id = htext(f"cfe-project-generated\n{source_key}\nv1\n{idx}\n{htext(raw_basis)}")
    return {
        "atom_id": atom_id,
        "source": {
            "repo": "CFE/project-generated-standard-uplift",
            "revision": "v1-2026-09-02",
            "config": source_key,
            "split": "quarantine",
            "row_id": idx,
            "source_url": None,
            "upstream_lineage": ["PROJECT_GENERATED_FROM_INVARIANT_CONTRACT"],
            "raw_record_sha256": htext(raw_basis),
        },
        "license": {
            "state": "RESOLVED_PROJECT_GENERATED",
            "labels": LICENSE,
            "row_specific": False,
            "notes": "Deterministic project-generated text; no upstream benchmark text copied. CC0 dedication intent for this generated surface only.",
        },
        "content": {
            "messages": messages,
            "reasoning": None,
            "final_answer": final,
            "tools": [],
            "observations": [],
            "target_visibility": "ANSWER_WITH_BOUNDED_JUSTIFICATION",
        },
        "capability": {
            "lanes": lanes,
            "domains": [family],
            "interaction_shape": packaging,
            "difficulty": hidden.get("difficulty", "medium"),
            "composition_required": True,
        },
        "quality": {
            "state": "CANDIDATE",
            "success_evidence": {"generator_contract": "PASS", "subtype": subtype},
            "verifier": "tools/verify_standard_uplift_lhit_gap_fillers_v1.py",
            "teacher_identity": "DETERMINISTIC_TEMPLATE_GENERATOR",
            "objective_check": {"state": "PASS_BY_CONSTRUCTION_PENDING_INDEPENDENT_READBACK"},
            "rejection_reasons": [],
        },
        "invariants": {
            "cfe": [],
            "lhit": [],
            "lhit_cross_domain": {
                "state": "CURATOR_STRUCTURE_BY_CONSTRUCTION",
                "domain_families": [family],
                "candidate_dimensions": sorted(set(dims)),
                "evidence": [f"deterministic generator subtype={subtype}"],
            },
            "tags_state": "CURATOR_GENERATED",
        },
        "contamination": {
            "state": "UNSCREENED_PROJECT_GENERATED",
            "exact_fingerprints": [htext(first_user.strip())],
            "normalized_fingerprints": [htext(" ".join(first_user.lower().split()))],
            "matched_eval_families": [],
        },
        "dedup": {
            "canonical_prompt_hash": htext(" ".join(first_user.lower().split())),
            "conversation_hash": htext(" ".join(conv.lower().split())),
            "duplicate_of": None,
            "near_duplicate_cluster": None,
        },
        "tokenization": {"per_target": {}, "destructive_truncation_required": False},
        "admission": {
            "state": "QUARANTINE",
            "reason": "project-generated gap filler; requires contamination/dedup/quality/invariant review before training",
            "review_history": [],
        },
        "pilot": {
            "project_generated": True,
            "generator": "generate_standard_uplift_lhit_gap_fillers_v1.py",
            "family": family,
            "subtype": subtype,
            "packaging": packaging,
            "hidden_curator_contract": hidden,
            "char_count": sum(len(m["content"]) for m in messages),
            "turn_count": len(messages),
        },
    }


def memory_atoms(rng: random.Random, n: int) -> list[dict[str, Any]]:
    if n % 4:
        raise ValueError("memory n must be divisible by 4")
    direct = [
        ("build server", "used Python 3.11", "was upgraded to Python 3.13", "the old 3.11-only compatibility assumption is stale"),
        ("data export", "ran at 17:00 UTC", "was moved to 19:30 UTC", "the 17:00 schedule is stale"),
        ("release branch", "was release/2.4", "is now release/2.5", "the old branch is no longer current"),
        ("lab freezer", "was assigned shelf B2", "was reassigned to shelf D1", "the B2 location is stale"),
        ("project owner", "was Mina", "was transferred to Theo", "Mina is no longer the current owner"),
        ("service endpoint", "used /v1/search", "now uses /v2/search", "the v1 endpoint is stale"),
        ("nightly report", "included region East", "now excludes region East", "the previous report scope is stale"),
        ("test fixture", "used dataset snapshot 41", "now uses snapshot 44", "snapshot 41 is no longer the current fixture"),
    ]
    propagated = [
        ("parser", "legacy mode is enabled", "legacy mode was removed in the new parser version", "the import job that depends on legacy mode must be re-evaluated"),
        ("field sensor", "calibration is valid through October", "the sensor head was replaced", "the old calibration certificate no longer supports measurements from the replacement head"),
        ("warehouse route", "aisle 4 is open", "aisle 4 is now restricted to maintenance", "the earlier pick route through aisle 4 is no longer feasible"),
        ("analysis notebook", "the table schema has columns A/B/C", "column B was split into B1/B2", "queries assuming one B column need review even though the query text was not directly revoked"),
        ("simulation", "gravity parameter g=9.81 is inherited from profile P", "profile P was changed to lunar gravity", "runs that inherit P must not use the old terrestrial interpretation"),
        ("deployment", "port 8080 is reserved for service K", "service K moved to a managed socket with no fixed port", "the old port reservation should not constrain the new deployment"),
        ("experiment", "batch 12 uses reagent lot L7", "lot L7 failed purity recheck", "results depending on L7 need qualification even if their numeric values have not changed"),
        ("dashboard", "alerts assume metric latency_ms", "the metric was redefined from end-to-end to server-only latency", "old alert thresholds are not directly comparable to the new metric"),
    ]
    preserve = [
        ("project state", "the API key rotation is Friday", "the database migration remains scheduled for Wednesday", "the API key rotation is now Monday", "Revise the key-rotation timing to Monday; the Wednesday migration remains current."),
        ("lab plan", "sample A is in freezer 2", "sample B remains in freezer 1", "sample A was moved to freezer 4", "Update sample A to freezer 4; preserve sample B in freezer 1."),
        ("travel plan", "the outbound train is 08:10", "the return train is still 18:40", "the outbound train moved to 09:05", "Revise the outbound time to 09:05; the 18:40 return remains current."),
        ("release plan", "the documentation freeze is Tuesday", "the code freeze is still Thursday", "the documentation freeze moved to Thursday next week", "Update only the documentation-freeze date; the existing code-freeze date remains supported."),
        ("device setup", "camera firmware is 5.1", "microphone firmware remains 3.7", "camera firmware changed to 5.2", "Update the camera firmware to 5.2; keep the microphone at 3.7."),
        ("inventory", "part Q has 9 units", "part R still has 14 units", "part Q is now out of stock", "Part Q is now out of stock; part R's 14-unit count remains current."),
        ("team roles", "review ownership belongs to Mara", "deployment ownership remains with Jules", "review ownership moved to Priya", "Revise review ownership to Priya; deployment ownership remains with Jules."),
        ("test environment", "browser version is 133", "database version remains 16.2", "browser version changed to 134", "Update the browser to 134; keep the database at 16.2."),
    ]
    ambiguous = [
        ("configuration", "a cached note from Tuesday says feature X is enabled", "an undated note says feature X is disabled", "Ask for a current authoritative configuration readback before acting; the evidence does not establish which note is current."),
        ("sample status", "a signed log at 10:00 says sample 7 is sealed", "a later informal message says it may have been reopened", "Treat the state as unresolved and check the current custody/log record rather than choosing the more convenient statement."),
        ("service ownership", "the runbook names team Blue", "a newer ticket suggests a transfer to team Green but is not approved", "Do not silently promote the proposed transfer; verify the current ownership authority."),
        ("experiment schedule", "calendar A shows Thursday", "calendar B shows Friday", "The schedule is conflicting; identify which calendar is authoritative/current before committing resources."),
        ("dataset revision", "a local file says revision r12", "the manifest pointer says r13 but has no hash", "Verify the authoritative manifest/hash before assuming either revision is current."),
        ("deployment state", "monitoring reports version 6.1", "a release note says 6.2 was intended", "Observed runtime state and intended release differ; check the live deployment rather than inferring 6.2."),
        ("instrument mode", "the operator note says high-gain", "the telemetry field is missing", "The current mode is not established; obtain a direct instrument readback before using high-gain assumptions."),
        ("task priority", "yesterday's plan lists task P first", "today's request says priorities changed without specifying order", "The old order may be stale, but the new order is unknown; ask for the updated priorities."),
    ]
    out=[]; per=n//4; idx=0
    subtypes=[("DIRECT_STALE_UPDATE",direct), ("INDIRECT_PROPAGATED_INVALIDATION",propagated), ("SELECTIVE_PRESERVATION",preserve), ("AMBIGUOUS_CURRENTNESS_DISCRIMINATOR",ambiguous)]
    for subtype, pool in subtypes:
        for j in range(per):
            rec=pool[j % len(pool)]
            packaging = "MULTI_TURN" if (j // len(pool)) % 2 else "SINGLE_TURN"
            if subtype == "SELECTIVE_PRESERVATION":
                subject,old_changed,unaffected,new_changed,answer=rec
                if packaging == "MULTI_TURN":
                    messages=[msg("user",f"Earlier state for {subject}: {old_changed}. Also: {unaffected}."),msg("assistant","Recorded as the current working state."),msg("user",f"New update: {new_changed}. What should remain current and what should be revised?")]
                else:
                    messages=[msg("user",f"For {subject}, an earlier record says: {old_changed}; {unaffected}. A later update says: {new_changed}. State what should be revised and what should remain current.")]
                final=answer
            elif subtype == "AMBIGUOUS_CURRENTNESS_DISCRIMINATOR":
                subject,a,b,answer=rec
                if packaging == "MULTI_TURN":
                    messages=[msg("user",f"For {subject}, {a}."),msg("assistant","That is one available state record."),msg("user",f"But {b}. What should we treat as current?")]
                else:
                    messages=[msg("user",f"For {subject}, {a}; however, {b}. What should we treat as current before acting?")]
                final=answer
            else:
                subject,a,b,answer=rec
                if packaging == "MULTI_TURN":
                    messages=[msg("user",f"Earlier, {subject} {a}."),msg("assistant","Understood."),msg("user",f"Later update for {subject}: {b}. What follows now?")]
                else:
                    messages=[msg("user",f"Earlier, {subject} {a}. Later, {subject} {b}. What follows now? Do not rely on the earlier state if its support changed.")]
                final=upper_first(answer)+". Preserve any unrelated state unless new evidence affects it."
            dims=["CONSEQUENTIAL_HISTORY_CANDIDATE","CURRENTNESS_PROPAGATION_CANDIDATE"]
            if subtype in {"INDIRECT_PROPAGATED_INVALIDATION","SELECTIVE_PRESERVATION"}: dims.append("DEPENDENCY_LOCAL_REPAIR_CANDIDATE")
            if subtype=="AMBIGUOUS_CURRENTNESS_DISCRIMINATOR": dims += ["UNRESOLVED_SEAM_PRESERVATION_CANDIDATE","LIVE_ALTERNATIVES_OR_DISCRIMINATOR_CANDIDATE","ACTIVE_DISCRIMINATOR_CANDIDATE"]
            if packaging=="MULTI_TURN": dims += ["LONG_HORIZON_STATE_CARRY_CANDIDATE","REVISIT_AFTER_STATE_CHANGE_CANDIDATE"]
            hidden={"family":"MEMORY_CURRENTNESS","subtype":subtype,"subject":subject,"expected":final,"difficulty":"medium","must_preserve_unrelated_state":True}
            out.append(atom("memory_currentness_v1",idx,"MEMORY_CURRENTNESS",subtype,messages,final,dims,hidden,packaging,["memory","currentness","state_revision","long_horizon"])); idx+=1
    return out


def discriminator_scores(candidates: list[str], predictions: dict[str, dict[str, str]], tests: list[str]) -> dict[str, dict[str, Any]]:
    out = {}
    for t in tests:
        counts: dict[str, int] = {}
        for h in candidates:
            v = predictions[h][t]
            counts[v] = counts.get(v, 0) + 1
        largest = max(counts.values())
        out[t] = {"partition_gain": len(candidates) - largest, "outcome_count": len(counts), "counts": counts}
    return out


def best_discriminator(candidates: list[str], predictions: dict[str, dict[str, str]], tests: list[str]) -> tuple[str, dict[str, Any], list[str]]:
    scores = discriminator_scores(candidates, predictions, tests)
    rank = {t: (z["partition_gain"], z["outcome_count"]) for t, z in scores.items()}
    best_rank = max(rank.values())
    ties = sorted(t for t, r in rank.items() if r == best_rank)
    return ties[0], scores, ties


def science_atoms(rng: random.Random, n: int) -> list[dict[str, Any]]:
    if n % 4:
        raise ValueError("science n must be divisible by 4")
    scenarios=[
        {"name":"optical bench","obs":"detector output is low","hyps":["source power dropped","aperture is partially blocked","detector gain drifted","alignment shifted"],"tests":["power_meter","aperture_image","reference_detector"],"pred":{
            "source power dropped":{"power_meter":"low","aperture_image":"clear","reference_detector":"low"},
            "aperture is partially blocked":{"power_meter":"normal","aperture_image":"blocked","reference_detector":"low"},
            "detector gain drifted":{"power_meter":"normal","aperture_image":"clear","reference_detector":"normal"},
            "alignment shifted":{"power_meter":"normal","aperture_image":"clear","reference_detector":"low"}}},
        {"name":"thermal chamber","obs":"measured temperature settles 8 C below setpoint","hyps":["heater output is weak","door seal leaks","temperature sensor is biased","controller integral term is disabled"],"tests":["heater_current","independent_thermometer","seal_pressure"],"pred":{
            "heater output is weak":{"heater_current":"low","independent_thermometer":"low","seal_pressure":"normal"},
            "door seal leaks":{"heater_current":"high","independent_thermometer":"low","seal_pressure":"low"},
            "temperature sensor is biased":{"heater_current":"normal","independent_thermometer":"normal","seal_pressure":"normal"},
            "controller integral term is disabled":{"heater_current":"normal","independent_thermometer":"low","seal_pressure":"normal"}}},
        {"name":"flow loop","obs":"downstream flow oscillates","hyps":["pump cavitation","control gain is too high","flow sensor is noisy","valve is sticking"],"tests":["pump_inlet_pressure","manual_valve_sweep","reference_flow_meter"],"pred":{
            "pump cavitation":{"pump_inlet_pressure":"low","manual_valve_sweep":"smooth","reference_flow_meter":"oscillating"},
            "control gain is too high":{"pump_inlet_pressure":"normal","manual_valve_sweep":"smooth","reference_flow_meter":"oscillating"},
            "flow sensor is noisy":{"pump_inlet_pressure":"normal","manual_valve_sweep":"smooth","reference_flow_meter":"stable"},
            "valve is sticking":{"pump_inlet_pressure":"normal","manual_valve_sweep":"jerky","reference_flow_meter":"oscillating"}}},
        {"name":"greenhouse trial","obs":"growth rate fell in one bay","hyps":["light intensity dropped","irrigation is low","soil nitrogen is depleted","growth sensor calibration shifted"],"tests":["light_meter","soil_moisture","manual_height_measurement"],"pred":{
            "light intensity dropped":{"light_meter":"low","soil_moisture":"normal","manual_height_measurement":"low_growth"},
            "irrigation is low":{"light_meter":"normal","soil_moisture":"low","manual_height_measurement":"low_growth"},
            "soil nitrogen is depleted":{"light_meter":"normal","soil_moisture":"normal","manual_height_measurement":"low_growth"},
            "growth sensor calibration shifted":{"light_meter":"normal","soil_moisture":"normal","manual_height_measurement":"normal_growth"}}},
        {"name":"spectrometer","obs":"one spectral peak shifted","hyps":["wavelength calibration drift","sample composition changed","sample temperature changed","peak fitting is biased"],"tests":["reference_lamp","independent_temperature","raw_spectrum_inspection"],"pred":{
            "wavelength calibration drift":{"reference_lamp":"shifted","independent_temperature":"normal","raw_spectrum_inspection":"peak_shifted"},
            "sample composition changed":{"reference_lamp":"normal","independent_temperature":"normal","raw_spectrum_inspection":"peak_shifted"},
            "sample temperature changed":{"reference_lamp":"normal","independent_temperature":"changed","raw_spectrum_inspection":"peak_shifted"},
            "peak fitting is biased":{"reference_lamp":"normal","independent_temperature":"normal","raw_spectrum_inspection":"raw_peak_normal"}}},
        {"name":"battery test rig","obs":"reported capacity fell suddenly","hyps":["cell degraded","current sensor scale changed","test cutoff voltage changed","ambient temperature fell"],"tests":["reference_current_meter","cutoff_config","ambient_probe"],"pred":{
            "cell degraded":{"reference_current_meter":"normal","cutoff_config":"unchanged","ambient_probe":"normal"},
            "current sensor scale changed":{"reference_current_meter":"mismatch","cutoff_config":"unchanged","ambient_probe":"normal"},
            "test cutoff voltage changed":{"reference_current_meter":"normal","cutoff_config":"changed","ambient_probe":"normal"},
            "ambient temperature fell":{"reference_current_meter":"normal","cutoff_config":"unchanged","ambient_probe":"low"}}},
        {"name":"radio telescope chain","obs":"noise floor increased","hyps":["front-end amplifier noise rose","external interference increased","digitizer gain changed","reference calibration is stale"],"tests":["shielded_dummy_load","spectrum_shape","calibration_tone"],"pred":{
            "front-end amplifier noise rose":{"shielded_dummy_load":"high_noise","spectrum_shape":"broadband","calibration_tone":"normal"},
            "external interference increased":{"shielded_dummy_load":"normal_noise","spectrum_shape":"narrowband","calibration_tone":"normal"},
            "digitizer gain changed":{"shielded_dummy_load":"high_noise","spectrum_shape":"broadband","calibration_tone":"scaled"},
            "reference calibration is stale":{"shielded_dummy_load":"normal_noise","spectrum_shape":"broadband","calibration_tone":"normal"}}},
        {"name":"reaction vessel","obs":"product yield is lower than expected","hyps":["reactant concentration is low","temperature profile is wrong","catalyst activity fell","assay calibration shifted"],"tests":["feed_assay","temperature_log","independent_product_assay"],"pred":{
            "reactant concentration is low":{"feed_assay":"low","temperature_log":"normal","independent_product_assay":"low"},
            "temperature profile is wrong":{"feed_assay":"normal","temperature_log":"off_profile","independent_product_assay":"low"},
            "catalyst activity fell":{"feed_assay":"normal","temperature_log":"normal","independent_product_assay":"low"},
            "assay calibration shifted":{"feed_assay":"normal","temperature_log":"normal","independent_product_assay":"normal"}}},
        {"name":"vibration test stand","obs":"a resonance peak moved upward","hyps":["test mass decreased","mount stiffness increased","accelerometer scale changed","analysis window is wrong"],"tests":["weigh_test_mass","static_stiffness_check","reference_accelerometer"],"pred":{
            "test mass decreased":{"weigh_test_mass":"low","static_stiffness_check":"normal","reference_accelerometer":"peak_shifted"},
            "mount stiffness increased":{"weigh_test_mass":"normal","static_stiffness_check":"high","reference_accelerometer":"peak_shifted"},
            "accelerometer scale changed":{"weigh_test_mass":"normal","static_stiffness_check":"normal","reference_accelerometer":"peak_normal"},
            "analysis window is wrong":{"weigh_test_mass":"normal","static_stiffness_check":"normal","reference_accelerometer":"peak_shifted"}}},
        {"name":"water treatment loop","obs":"reported dissolved oxygen fell","hyps":["aeration weakened","probe membrane fouled","water temperature rose","flow bypass opened"],"tests":["air_flow_meter","reference_oxygen_probe","bypass_position"],"pred":{
            "aeration weakened":{"air_flow_meter":"low","reference_oxygen_probe":"low","bypass_position":"closed"},
            "probe membrane fouled":{"air_flow_meter":"normal","reference_oxygen_probe":"normal","bypass_position":"closed"},
            "water temperature rose":{"air_flow_meter":"normal","reference_oxygen_probe":"low","bypass_position":"closed"},
            "flow bypass opened":{"air_flow_meter":"normal","reference_oxygen_probe":"low","bypass_position":"open"}}},
        {"name":"photovoltaic array","obs":"string power dropped at noon","hyps":["one module is shaded","inverter tracking is wrong","irradiance sensor is biased","connector resistance increased"],"tests":["module_thermal_image","dc_iv_sweep","reference_irradiance_meter"],"pred":{
            "one module is shaded":{"module_thermal_image":"cold_patch","dc_iv_sweep":"step","reference_irradiance_meter":"normal"},
            "inverter tracking is wrong":{"module_thermal_image":"uniform","dc_iv_sweep":"normal_curve","reference_irradiance_meter":"normal"},
            "irradiance sensor is biased":{"module_thermal_image":"uniform","dc_iv_sweep":"normal_curve","reference_irradiance_meter":"mismatch"},
            "connector resistance increased":{"module_thermal_image":"hot_connector","dc_iv_sweep":"loss","reference_irradiance_meter":"normal"}}},
        {"name":"fermentation vessel","obs":"carbon dioxide production slowed","hyps":["substrate is depleted","culture activity fell","gas-flow sensor drifted","temperature control is low"],"tests":["substrate_assay","independent_gas_meter","temperature_probe"],"pred":{
            "substrate is depleted":{"substrate_assay":"low","independent_gas_meter":"low","temperature_probe":"normal"},
            "culture activity fell":{"substrate_assay":"normal","independent_gas_meter":"low","temperature_probe":"normal"},
            "gas-flow sensor drifted":{"substrate_assay":"normal","independent_gas_meter":"normal","temperature_probe":"normal"},
            "temperature control is low":{"substrate_assay":"normal","independent_gas_meter":"low","temperature_probe":"low"}}},
        {"name":"seismometer station","obs":"low-frequency noise increased","hyps":["ground tilt increased","sensor leveling shifted","digitizer reference drifted","nearby machinery started"],"tests":["tilt_meter","level_bubble_check","independent_sensor"],"pred":{
            "ground tilt increased":{"tilt_meter":"high","level_bubble_check":"normal","independent_sensor":"high_noise"},
            "sensor leveling shifted":{"tilt_meter":"normal","level_bubble_check":"off_level","independent_sensor":"normal_noise"},
            "digitizer reference drifted":{"tilt_meter":"normal","level_bubble_check":"normal","independent_sensor":"normal_noise"},
            "nearby machinery started":{"tilt_meter":"normal","level_bubble_check":"normal","independent_sensor":"high_noise"}}},
        {"name":"wind tunnel","obs":"measured drag rose across all test points","hyps":["air density estimate is wrong","force balance zero shifted","model surface roughened","tunnel speed calibration changed"],"tests":["reference_barometer","balance_zero_check","independent_speed_probe"],"pred":{
            "air density estimate is wrong":{"reference_barometer":"mismatch","balance_zero_check":"normal","independent_speed_probe":"normal"},
            "force balance zero shifted":{"reference_barometer":"normal","balance_zero_check":"offset","independent_speed_probe":"normal"},
            "model surface roughened":{"reference_barometer":"normal","balance_zero_check":"normal","independent_speed_probe":"normal"},
            "tunnel speed calibration changed":{"reference_barometer":"normal","balance_zero_check":"normal","independent_speed_probe":"mismatch"}}},
        {"name":"chromatograph","obs":"retention times shifted together","hyps":["carrier flow changed","column temperature changed","clock calibration drifted","sample chemistry changed"],"tests":["flow_reference","column_temperature_probe","external_time_reference"],"pred":{
            "carrier flow changed":{"flow_reference":"mismatch","column_temperature_probe":"normal","external_time_reference":"normal"},
            "column temperature changed":{"flow_reference":"normal","column_temperature_probe":"changed","external_time_reference":"normal"},
            "clock calibration drifted":{"flow_reference":"normal","column_temperature_probe":"normal","external_time_reference":"mismatch"},
            "sample chemistry changed":{"flow_reference":"normal","column_temperature_probe":"normal","external_time_reference":"normal"}}},
        {"name":"acoustic chamber","obs":"measured reverberation time increased","hyps":["absorber panels were removed","microphone calibration drifted","room temperature changed","analysis decay window changed"],"tests":["panel_inventory","reference_microphone","analysis_config_check"],"pred":{
            "absorber panels were removed":{"panel_inventory":"missing","reference_microphone":"long_decay","analysis_config_check":"unchanged"},
            "microphone calibration drifted":{"panel_inventory":"complete","reference_microphone":"normal_decay","analysis_config_check":"unchanged"},
            "room temperature changed":{"panel_inventory":"complete","reference_microphone":"long_decay","analysis_config_check":"unchanged"},
            "analysis decay window changed":{"panel_inventory":"complete","reference_microphone":"normal_decay","analysis_config_check":"changed"}}},
    ]
    out=[]; per=n//4; idx=0
    subtypes=["CHOOSE_DISCRIMINATOR","UPDATE_CANDIDATES","SUPPORT_VS_DISCRIMINATION","REPRESENTATION_REFINEMENT"]
    for subtype in subtypes:
        for j in range(per):
            sc=scenarios[j % len(scenarios)]
            hyps=sc["hyps"][:]
            tests=sc["tests"][:]
            best,test_scores,best_ties=best_discriminator(hyps,sc["pred"],tests)
            if subtype=="CHOOSE_DISCRIMINATOR":
                messages=[msg("user",f"In {article(sc['name'])} {sc['name']}, {sc['obs']}. Live explanations are: {', '.join(hyps)}. Available checks are {', '.join(pretty(t) for t in tests)}. Which check should come first if the goal is to distinguish the explanations rather than just gather more supporting data?")]
                if len(best_ties) == 1:
                    final=f"Start with {pretty(best)}. Under the stated model it gives the strongest partition of the live explanations. Keep the explanations live until the measurement arrives; the observation should update the candidate set rather than merely confirm a favorite."
                else:
                    final=f"{upper_first(pretty(best))} is one of the most discriminating checks under the stated model; the tied best options are {', '.join(pretty(t) for t in best_ties)}. Use cost, reliability, or availability to choose among the tie, then update the live candidate set from the observation."
                dims=["LIVE_ALTERNATIVES_OR_DISCRIMINATOR_CANDIDATE","ACTIVE_DISCRIMINATOR_CANDIDATE","EXTERNAL_OR_ORTHOGONAL_CHECK_CANDIDATE"]
                hidden={"family":"SCIENCE_DIAGNOSIS","subtype":subtype,"scenario":sc["name"],"candidates":hyps,"best_test":best,"best_ties":best_ties,"test_scores":test_scores,"difficulty":"medium"}
            elif subtype=="UPDATE_CANDIDATES":
                t=tests[j % len(tests)]; observed=sc["pred"][hyps[j % len(hyps)]][t]
                survivors=[h for h in hyps if sc["pred"][h][t]==observed]
                messages=[msg("user",f"In {article(sc['name'])} {sc['name']}, {sc['obs']}. Candidate explanations are {', '.join(hyps)}. We measured {pretty(t)} and observed '{observed}'. Which candidates remain supported by this measurement?")]
                final=f"After the {pretty(t)} result, retain: {', '.join(survivors)}. The other candidates conflict with this observation under the stated model. Do not discard distinctions among the survivors until another measurement separates them."
                dims=["LIVE_ALTERNATIVES_OR_DISCRIMINATOR_CANDIDATE","CURRENTNESS_PROPAGATION_CANDIDATE","EXTERNAL_OR_ORTHOGONAL_CHECK_CANDIDATE","DEPENDENCY_LOCAL_REPAIR_CANDIDATE"]
                hidden={"family":"SCIENCE_DIAGNOSIS","subtype":subtype,"scenario":sc["name"],"test":t,"observed":observed,"survivors":survivors,"difficulty":"medium"}
            elif subtype=="SUPPORT_VS_DISCRIMINATION":
                ranks={t:(z["partition_gain"],z["outcome_count"]) for t,z in test_scores.items()}
                lower=[t for t in tests if ranks[t] < ranks[best]]
                if lower:
                    worst_rank=min(ranks[t] for t in lower)
                    comparison=sorted(t for t in lower if ranks[t]==worst_rank)[0]
                    relation="STRICT"
                else:
                    comparison=sorted(t for t in tests if t != best)[0]
                    relation="TIED"
                messages=[msg("user",f"For {article(sc['name'])} {sc['name']}, where {sc['obs']}, the current explanations are {', '.join(hyps)}. Check A is {pretty(comparison)}; check B is {pretty(best)}. Which is more useful if the purpose is to identify which explanation is right, and why?")]
                if relation=="STRICT":
                    final=f"Prefer {pretty(best)} for identification. {pretty(comparison)} may still be relevant, but under the stated model its outcomes separate fewer of the live explanations. A useful diagnostic check is one whose possible results divide the candidate set."
                else:
                    final="The two checks are equally discriminating under the stated model. Do not invent a ranking; choose between them using cost, reliability, or availability, then update the candidate set from the result."
                dims=["LIVE_ALTERNATIVES_OR_DISCRIMINATOR_CANDIDATE","ACTIVE_DISCRIMINATOR_CANDIDATE","EXTERNAL_OR_ORTHOGONAL_CHECK_CANDIDATE"]
                hidden={"family":"SCIENCE_DIAGNOSIS","subtype":subtype,"scenario":sc["name"],"preferred":best,"comparison":comparison,"test_scores":test_scores,"rank_relation":relation,"difficulty":"medium"}
            else:
                # Construct an out-of-model residual: every listed candidate predicts one outcome, but observation is outside all listed predictions.
                t=tests[0]; predicted=sorted(set(sc["pred"][h][t] for h in hyps)); impossible="outside_listed_predictions"
                messages=[msg("user",f"In {article(sc['name'])} {sc['name']}, the working model has these explanations: {', '.join(hyps)}. For the {pretty(t)} check, those explanations predict only {', '.join(predicted)}. The actual measurement is outside all of those predicted outcomes, and the measurement passes its self-check. What is the right next reasoning move?")]
                final="Do not force the observation into one of the existing explanations. The current hypothesis/model class is inadequate for this result. Preserve the residual, audit the measurement lineage, and expand or refine the representation/model before ranking the old candidates again."
                dims=["REPRESENTATION_REFINEMENT_CANDIDATE","UNRESOLVED_SEAM_PRESERVATION_CANDIDATE","EXTERNAL_OR_ORTHOGONAL_CHECK_CANDIDATE","CURRENTNESS_PROPAGATION_CANDIDATE"]
                hidden={"family":"SCIENCE_DIAGNOSIS","subtype":subtype,"scenario":sc["name"],"test":t,"model_predictions":predicted,"observed":impossible,"requires_model_refinement":True,"difficulty":"hard"}
            out.append(atom("science_diagnosis_v1",idx,"SCIENCE_DIAGNOSIS",subtype,messages,final,dims,hidden,"SINGLE_TURN",["science","diagnosis","hypothesis_testing","measurement"])); idx+=1
    return out


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="\n") as f:
        for r in rows: f.write(stable_json(r)+"\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",type=Path,required=True); ap.add_argument("--memory-n",type=int,default=64); ap.add_argument("--science-n",type=int,default=64); a=ap.parse_args()
    if a.out.exists(): raise SystemExit(f"REFUSE_OVERWRITE {a.out}")
    a.out.mkdir(parents=True)
    rng=random.Random(SEED)
    mem=memory_atoms(rng,a.memory_n); sci=science_atoms(rng,a.science_n); rows=mem+sci
    sha=write_jsonl(a.out/"PROJECT_GENERATED_SFT_QUARANTINE.jsonl",rows)
    counts={}
    for r in rows:
        k=f"{r['pilot']['family']}::{r['pilot']['subtype']}::{r['pilot']['packaging']}";counts[k]=counts.get(k,0)+1
    manifest={"schema":"cfe.standard-uplift.project-generated-gap-fillers.v1","status":"GENERATED_QUARANTINE__NOT_TRAINABLE","seed":SEED,"created_unix":time.time(),"rows":len(rows),"memory_rows":len(mem),"science_rows":len(sci),"jsonl_sha256":sha,"counts":counts,"license":LICENSE,"laws":["PROJECT GENERATED != TRAINING ADMITTED","LHIT != CONVERSATION FORMAT","TEACH CONSEQUENCE STRUCTURE NOT DONOR LABELS","CONTAMINATION SCREEN STILL REQUIRED","OBJECTIVE GENERATOR CHECK != HOSTILE QUALITY REVIEW"]}
    (a.out/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(manifest,indent=2))

if __name__=="__main__": main()
