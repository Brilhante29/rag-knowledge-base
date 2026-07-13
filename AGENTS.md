# Agents

This repository is governed by `portfolio-reuse-kit`.

Agents must use the local `.portfolio/` snapshot as the source of truth. The principal agent coordinates architecture, stack, benchmark, local-first runtime, reuse review, and publication.

## Required Flow

1. Read `.portfolio/decision-brain/agent-graph.yaml`.
2. Read `.portfolio/decision-brain/reuse-improvement-loop.yaml`.
3. Keep `project.yaml`, SDD files, README, benchmark result, and references aligned.
4. Patch `portfolio-reuse-kit` when this project reveals a low-risk reusable improvement.

## Current Decisions

- Architecture: clean-architecture with ports/adapters boundaries.
- Stack: Python FastAPI backend with local deterministic hashing embeddings.
- API style: REST/HTTP plus CLI for benchmark automation.
- Messaging: none.
- Cloud: none for default path; Kumo remains the local-first choice if AWS-like behavior is added later.
- Benchmark: Recall@3, latency, cost/query.
