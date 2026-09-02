# Local Fleet Priority + Capybara Data Policy

Date: 2026-09-02 09:57 Eastern Daylight Time
Status: **ACTIVE ENGINEERING SELECTION / DATA POLICY**

## 1. Primary high-end local model — VERIFIED
File:
`D:/Project_Linked_Tensors/monster-standard-inference-revival-2026-04-06/incoming/Qwen3.5-35B-A3B-Claude-4.6-Opus-Reasoning-Distilled.i1-Q4_K_M.gguf`

Identity from embedded GGUF metadata:
- Qwen3.5-35B-A3B;
- qwen35moe;
- 34.66B params, ~A3B active regime;
- 40 blocks;
- 256 experts / 8 experts used;
- 262144 native context metadata;
- source Jackrong Claude-4.6-Opus reasoning-distilled model;
- mradermacher i1 importance-matrix Q4_K_M quantization.

Remote identity verified against `mradermacher/Qwen3.5-35B-A3B-Claude-4.6-Opus-Reasoning-Distilled-i1-GGUF` revision `724ed5dc98278195746f5f90ac388de78fa753c1`:
- bytes `21169115200`;
- SHA256 `d1ed134b54a8509a6dc773d30d7eadb70b59bc2e5d010ee2fd40c4cb02b24992`;
- exact match PASS.

Local llama.cpp CPU-only benchmark (CUDA backend not loaded by current build):
- pp256 ~49.8-89.3 tok/s across two runs;
- tg64 ~13.6-14.5 tok/s.

Disposition: **PRIMARY HIGH-END LOCAL TEACHER / RESEARCH / JUDGE / HARD-PROBLEM MODEL**.
Not a practical local training target in GGUF form. Train smaller learners; use this model to generate/challenge/judge selected material.

## 2. Capybara models currently local
### A — CapybaraHermes-2.5-Mistral-7B
- base OpenHermes-2.5-Mistral-7B;
- preference tuned on Argilla dpo-mix-7k;
- local separate checkpoint, NOT identical to ORPO Capybara;
- published MTBench ~7.90, MMLU 63.13.
- current stronger local Capybara model.

### B — kaist-ai/Mistral-ORPO-Capybara-7k
- Mistral-7B-v0.1 base;
- ORPO trained exclusively on Argilla distilabel Capybara DPO 7k;
- published MTBench 7.44; AlpacaEval2 LC 15.9.
- useful lineage/reference model but weaker than local CapybaraHermes.

## 3. Better Capybara objective
Do not merely preserve a 2023/2024 checkpoint. Build a **modern Capybara successor** that preserves the valuable Capybara phenotype:
- long-form multi-turn continuity;
- reasoning/extrapolation across follow-ups;
- obscure-domain depth;
- natural conversational prose;
- low refusal/boilerplate contamination;
while adding 2025-2026 reasoning, code, science, agentic execution and evidence discipline.

Nous-Capybara-7B-V1.9 is a useful canonical reference checkpoint/data lineage, but its own model card lacks published benchmark results. Treat it as a lineage comparator, not automatically the final base.

## 4. "Our Capybara" is a first-class data family
Fleet Uplift Pack v2 SHALL contain a named `OUR_CAPYBARA_CORE` stratum.

### SFT material
1. `LDJnr/Capybara` (Apache-2.0) — decontaminated multi-turn Capybara conversations.
2. High-rated chosen trajectories from `argilla/Capybara-Preferences-Filtered` (Apache-2.0), flattened only when the full multi-turn context is preserved.
3. Select exact local CapybaraHermes / ORPO-Capybara generations **only if** externally checked or verified against objective constraints; local model origin alone is not quality evidence.

### Preference material
Primary Capybara preference source:
`argilla/Capybara-Preferences-Filtered` — 14,811 filtered chosen/rejected pairs, Apache-2.0.

Secondary lineage source:
`argilla/distilabel-capybara-dpo-7k-binarized` — exact family used by local ORPO-Capybara.

### Guard
Do not put rejected responses into SFT targets.
Do not train on local-Capybara generations simply because they are "ours."
Use local generations as candidate variants and retain them only if verification/judging improves the source or fills a missing field.

## 5. Model-role stack
1. **Qwen3.5-35B-A3B Claude-distilled i1 Q4_K_M** — strongest practical high-end teacher/judge/research model.
2. **Qwen3-4B-Thinking-2507** — primary trainable reasoning learner on current 6GB GPU.
3. **Modern Capybara successor** — second trainable target; base selection remains a benchmarked engineering choice, not automatically old Mistral.
4. **CapybaraHermes-7B + ORPO-Capybara-7B** — lineage comparators / phenotype donors / candidate response generators, not final target by default.

## 6. CFE integration
For each trainable target, use matched atom sets:
- STANDARD_BALANCED;
- CFE_STRUCTURED.

`OUR_CAPYBARA_CORE` must occur in both arms with identical atom counts. CFE may change placement/revisit/contrast geometry, not whether Capybara content exists.
