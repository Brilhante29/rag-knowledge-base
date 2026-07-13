# Reuse Improvement Review

Project: `3 - rag-knowledge-base`

## Review Points

- [x] after scaffold
- [x] after architecture decision
- [x] after first working slice
- [x] after benchmark result
- [x] before publication
- [ ] after CI failure, if applicable

## Findings

| Finding | Classification | Kit Area | Action | Status |
|---|---|---|---|---|
| Projects need an explicit loop that asks whether the reuse kit should improve while work progresses. | `patch_now` | `decision-brain`, `skills`, `sdd`, `templates`, `validation` | Added reuse-improvement loop to `portfolio-reuse-kit` before implementing this project. | done |
| RAG projects benefit from a local deterministic embedding baseline before model-backed providers. | `backlog` | `templates`, `harness` | Consider adding a reusable retrieval benchmark template after one more retrieval repo validates the shape. | pending |
| Python CI templates should support pyproject-based repos and explicit unittest discovery, not only requirements plus pytest. | `backlog` | `templates`, `validation` | Revisit after the next Python repo to avoid overfitting the shared template to this project. | pending |
| Project-specific fixture documents should move into the kit. | `reject` | `templates` | Fixtures are domain-specific evidence and should stay in this repo. | done |

## Patch Now Decisions

- Added `decision-brain/reuse-improvement-loop.yaml` to `portfolio-reuse-kit`.
- Added `reuse-improvement-review` skills for Codex and Claude.
- Added `sdd/templates/reuse-improvement-review.md` and scaffold/validation support.

## Backlog Decisions

- Add a reusable retrieval benchmark harness only after `embeddings-benchmark` confirms common inputs/result shape.
- Add a more flexible Python CI template after another Python repo confirms the right default.

## Rejected Improvements

- Do not move this repo's corpus/questions into the kit.

## Final Gate

- [x] Reusable improvements were patched or recorded.
- [x] Project-specific implementation was not moved into the kit.
- [x] Validation reflects the new repeated review requirement.
