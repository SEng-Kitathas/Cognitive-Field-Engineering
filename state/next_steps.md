# CFE NEXT STEPS

As of: 2026-09-02 01:05 Eastern Daylight Time

## Overnight active
1. Complete bounded local archaeology scan.
2. Execute three research lanes: MACHINERY, CARTOGRAPHY, EXTERNAL; each lane is 3x20 autonomous passes with OARR, Loop+, Semantic Helix, Attention Reservoir and CSC audit-only hard stop.
3. Research output remains non-authoritative until morning synthesis/hostile adjudication; no auto-promotion.
4. At research completion, dedicated inference service is terminated and `RESEARCH_LANE_COMPLETE.sentinel` is emitted.
5. DD2R1 then verifies/downloads only the train-manifest-bound seed3121/CYCLIC_SPACED adapter and attempts clean-state evaluation.
6. If salvage evaluation fails after bounded retries: stop DD2R1 with no further training.
7. If salvage evaluation passes: continue seed3121 pair and remaining fresh DD2 pairs under unchanged scientific contract; aggregate only 6/6.
8. Morning readback must reconcile research artifacts against first-class cartography before any promotion or new experiment selection.

## Fleet validation — gated future work
- Preserve and freeze representative pre-CFE phenotype probes before any CFE fleet intervention.
- Inventory eligible local learners/trainable checkpoints.
- Do not launch broad fleet training until the authorization threshold in the fleet research plan is met.

## Rosetta/LBE historical branch — parked but preserved
- Do not mix into active CFE science without explicit branch selection.
- If reopened, first experiment should test whether a function-preserving block representation + small router can outperform ordinary retrieval at equal active-memory/compute budget.
- Use Rosetta structural atlas for candidate motif selection, not as the functional substrate itself.

## Fleet Uplift Pack v2
- Build new v2 pack; do not reuse empty v1 output directory as authoritative artifact.
- Freeze Capybara core first: LDJnr/Capybara + filtered Capybara chosen responses; keep preference pairs for separate preference phase.
- Benchmark candidate modern Capybara bases before download/train selection.
- Repair/upgrade llama.cpp CUDA backend separately; CPU-only 35B-A3B is already usable at ~14 tok/s.

## Resource-gated continuation — 2026-09-02
1. Do not launch Qwen3.5-35B-A3B, MTP, QLoRA, or any other heavy CFE model job while a foreign model runtime is live.
2. Before any later heavy run, execute `tools/cfe_resource_authority_guard.py`; require PASS immediately before launch and again after CFE-owned server startup.
3. When a safe window exists, run `tools/run_qwen35_a3b_mtp_benchmark_safe.py` sequentially: target-only baseline -> Q8 MTP, never concurrently.
4. If MTP fails compatibility or loses throughput, preserve the failure and only then consider a target-distilled MTP/EAGLE/DFlash route.
5. Continue low-impact dataset/LHIT/Capybara design and model-quality research while blocked.

## Speculative runtime next steps — 2026-09-02
1. Treat `Q4_K_M MTP + n_max=2` as the current best-tested local speculative profile for the Claude-distilled Qwen3.5-35B-A3B at 4K/single-slot.
2. Do not use the Q8 MTP sidecar as default on this 6GB GPU; it reduces target residency and lost throughput in paired testing.
3. Before wider deployment, test the chosen Q4/n=2 profile at 8K and 16K context under the same resource guard; stop if another project claims resources.
4. Keep Qwen3.6-35B-A3B and Gemma 4 26B-A4B as model-fit challengers, but do not download/load them until a later safe window and explicit comparison packet is ready.
5. Keep the stale-runtime reclamation rule active: healthy socket alone does not prove current ownership; require multi-signal liveness before preserving a warm load indefinitely.
