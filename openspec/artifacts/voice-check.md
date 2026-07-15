# Voice Check: rag-knowledge-base

## Verdict

aligned (7/7)

## Reference Files

- README.md
- sdd\spec.md
- sdd\technical-decision.md

## Style Stats

| Source | Words | Avg sentence words | Headings | Bullets | Numbers | Evidence words | Hype words |
|---|---:|---:|---:|---:|---:|---:|---:|
| existing docs | 819 | 10 | 26 | 50 | 26 | 61 | 0 |
| generated article | 186 | 9.1 | 1 | 0 | 8 | 16 | 0 |

## Checks

- PASS: article starts with project number and name.
- PASS: claim appears verbatim.
- PASS: benchmark evidence appears early.
- PASS: architecture and rejected alternatives are part of the story.
- PASS: hype-word count is low.
- PASS: average sentence length is close to the existing docs.
- PASS: evidence-word density is high enough.

## Interpretation

The desired portfolio voice is direct, evidence-first, benchmark-heavy, specific about tradeoffs, and light on adjectives. A generated article should sound like the README and SDD were written by the same engineer: first the number, then the claim, then the architectural tradeoff.
