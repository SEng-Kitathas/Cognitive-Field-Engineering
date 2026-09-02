# Qwen3.5-35B-A3B Claude-Distilled Speculative Runtime Disposition

Date: 2026-09-02
Status: **VERIFIED LOCAL RUNTIME DISPOSITION / LIMITED BENCHMARK SCOPE**

## Target
`D:/Project_Linked_Tensors/monster-standard-inference-revival-2026-04-06/incoming/Qwen3.5-35B-A3B-Claude-4.6-Opus-Reasoning-Distilled.i1-Q4_K_M.gguf`

SHA-256:
`d1ed134b54a8509a6dc773d30d7eadb70b59bc2e5d010ee2fd40c4cb02b24992`

Runtime:
`tooling/llama_cpp_b10759_cuda13/runtime_verified/llama-server.exe`
Build `b10759`, commit `b81c99b47`.

Hardware under test:
- Ryzen 9 7940HX
- ~32 GB system RAM
- RTX 4050 Laptop GPU, 6 GB VRAM

## Resource precondition
Before all heavy phases, `tools/cfe_resource_authority_guard.py` SHALL return PASS. Benchmark phases are sequential and CFE-owned servers are shut down before the next phase.

## Stale-load correction before benchmark
A 14B llama server on PID 34152 / port 8114 was initially treated as foreign authority. It was later proven stale by parent absence, idle slot, no established clients, zero CPU delta over 6 seconds, and retained ~7.113 GiB private RAM. It was reclaimed by exact PID/command-line fingerprint only.

## Tested speculative candidates

### Generic Qwen3.5 0.8B draft
Technically compatible under current checkpoint-backed speculative decoding, but slower than target-only.
- tuned `n_max=3`, high confidence: ~22.61 tok/s vs ~26.17 tok/s earlier single-prompt target baseline.
- high token acceptance did not amortize draft/checkpoint overhead.

### Generic Qwen3.5 2B draft
Technically compatible but slower still.
- ~19.99 tok/s on the same earlier single-prompt test.

### Native MTP Q8_0 sidecar
Artifact:
`E:/models/speculative/qwen35_a3b_mtp/Qwen3.5-35B-A3B-MTP-ONLY-Q8_0.gguf`

SHA-256:
`54f372d7ce6625a9cf66e296f9da7b2786efdb12a2ec3c957cdfec3ff6d36ed7`

At `n_max=3` over the 4-prompt technical benchmark:
- paired target-only mean: `34.0361 tok/s`
- MTP Q8 mean: `33.2668 tok/s`
- ratio: `0.9774x`

Disposition: **REJECT AS DEFAULT ON THIS 6 GB GPU**.

Mechanism-level reason: the Q8 MTP sidecar forced the target from 41/41 GPU-offloaded layers down to 36/41, with target CUDA model buffer ~1617.94 MiB plus draft ~1372.68 MiB. The added draft quality did not compensate for lost hot-target residency.

### Native MTP Q4_K_M sidecar, n_max=3
Artifact:
`E:/models/speculative/qwen35_a3b_mtp/Qwen3.5-35B-A3B-MTP-ONLY-Q4_K_M.gguf`

Bytes: `1,621,551,104`
SHA-256:
`14639932a007d1fa49bbb837bce6ad4525e65c8ccc932104c6e6ca2b6b2aa274`

4-prompt benchmark:
- paired target-only mean: `34.9689 tok/s`
- Q4 MTP mean: `36.0452 tok/s`
- ratio: `1.0308x`

Target retained 41/41 GPU-offloaded layers while the Q4 MTP model also fully offloaded.

Disposition: **SUPPORTED, BUT NOT BEST TESTED SETTING**.

### Native MTP Q4_K_M sidecar, n_max=2
4-prompt benchmark:
- paired target-only mean: `35.4938 tok/s`
- Q4 MTP n=2 mean: `38.0903 tok/s`
- ratio: `1.07315x`
- MTP wins: `4/4 prompts`

Per-prompt generation rates, target -> MTP:
1. `32.4637 -> 33.3083 tok/s`
2. `35.9110 -> 38.3501 tok/s`
3. `36.8245 -> 37.8752 tok/s`
4. `36.7760 -> 42.8278 tok/s`

Draft acceptance by prompt:
1. `71/109 = 65.14%`, position rates `(0.745, 0.545)`
2. `69/114 = 60.53%`, position rates `(0.702, 0.509)`
3. `68/117 = 58.12%`, position rates `(0.695, 0.458)`
4. `75/101 = 74.26%`, position rates `(0.784, 0.686)`

Resource state while loaded:
- target reports 41/41 layers offloaded;
- target CUDA model buffer ~1943.76 MiB under the combined fit;
- MTP CUDA model buffer ~1020.68 MiB;
- post-launch free RAM ~17.74 GB;
- post-launch free VRAM ~1717 MiB;
- no foreign model runtime detected.

## Current recommended local runtime profile
For this exact target and this exact machine, the best tested profile is:

- target: existing mradermacher i1 `Q4_K_M` Claude-distilled 35B-A3B GGUF;
- llama.cpp: current isolated b10759 CUDA 13.3 runtime;
- context for verified benchmark: `4096`;
- flash attention: on;
- GPU fit: auto;
- speculative type: `draft-mtp`;
- MTP sidecar: `Qwen3.5-35B-A3B-MTP-ONLY-Q4_K_M.gguf`;
- MTP GPU layers: auto;
- `spec-draft-n-max = 2`;
- parallel slots: 1.

## Claim ceiling
This is a **local engineering benchmark**, not a universal performance claim.

Verified scope:
- this exact hardware;
- this exact target quant;
- llama.cpp b10759;
- 4K context;
- single-slot inference;
- four 128-token technical prompts.

Not yet verified:
- long-context behavior at 8K/16K/32K+;
- multi-user/parallel serving;
- quality equivalence beyond qualitative inspection;
- end-to-end latency under tool-calling workloads;
- whether Qwen3.6-35B-A3B or Gemma 4 26B-A4B is a stronger overall machine-fit model.

## Laws earned
`HIGH DRAFT PRECISION != BEST SPECULATIVE CONFIGURATION`
`DRAFT QUALITY MUST BE EVALUATED WITH TARGET GPU RESIDENCY`
`ACCEPTANCE RATE != THROUGHPUT`
`SMALLER MATCHED MTP CAN BEAT LARGER MTP ON VRAM-CONSTRAINED HARDWARE`
`RESOURCE AUTHORITY MUST BE REVALIDATED AT LAUNCH TIME`
