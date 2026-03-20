# AGENTS.md

## Foundation

This repository follows Pipe-Works org standards and reusable workflow conventions.

## Scope

- Deterministic generation engine library only.
- No web/server/runtime deployment responsibilities.
- No corpus/lexicon pipeline tooling.

## Non-Negotiables

- Determinism first: use isolated RNG (`random.Random(seed)`), avoid global RNG state.
- Keep runtime dependencies minimal.
- Keep public package API stable once published.
