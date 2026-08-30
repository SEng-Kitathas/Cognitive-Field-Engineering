# Publication and Asset Boundary

## Goal
Keep the repository sufficient for **continuation and reproducibility reasoning** without making a normal clone/install download the entire R&D warehouse.

## In normal Git
Track:
- source code and tooling;
- continuity state;
- scientific contracts, manifests, hashes, analyses, qualification receipts;
- small candidate/evaluation data required to understand or reproduce compilers;
- project history, decisions, doctrine and policies;
- campaign ledgers and compact logs required for lineage.

## Never in normal Git
- model weights / HF caches;
- LoRA adapter payloads / checkpoints;
- executed full run directories when they can be regenerated or archived separately;
- multi-hundred-MB reincarnation ZIPs;
- historical raw R&D dumps;
- transient `.pcmmad_sync_runs` logs;
- credentials/secrets.

## Heavy package publication
Heavy packages SHALL be published as opt-in GitHub Release assets (or an explicitly separate archive repository if size requires it). Every asset must have:
- exact filename;
- bytes;
- SHA-256;
- provenance/source date;
- relationship to current doctrine;
- whether it is required for runtime, scientific reproduction, or forensic recovery.

A normal `git clone` or OS install MUST NOT download those assets. Fetch scripts must require an explicit archive/research flag.
