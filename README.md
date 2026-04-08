# pipeworks-namegen-core

`pipeworks-namegen-core` is the pure deterministic library for PipeWorks name
generation.

It is the lowest-level runtime boundary in the three-repo split:

- `pipeworks-namegen-core` owns pure deterministic generation/rendering logic
- `pipeworks-namegen-api` owns the HTTP/runtime contract and package-backed
  service behavior
- `pipeworks-namegen-lexicon` owns corpus, lexicon, and creator-facing
  tooling

## Scope

- deterministic generation primitives (`NameGenerator`)
- deterministic rendering helpers (`render_name`, `render_names`)
- deterministic value sampling helpers (`sample_values`)
- no HTTP server, UI assets, or SQLite/runtime service concerns
- no package-import, filename-mapping, or deployment ownership

## Library Model

This package should be boring:

- given the same inputs, it should produce the same outputs
- consumers provide value pools or use a small built-in preset
- no web/runtime/persistence assumptions leak into the library boundary

The preferred mental model is:

1. another repo or app gathers/owns candidate values
2. `pipeworks-namegen-core` deterministically samples or renders them
3. higher layers decide how those values are stored, exposed, or served

## Public API

Current stable exports:

- `NameGenerator`
- `sample_values`
- `dedupe_preserve_order`
- `RENDER_STYLES`
- `normalize_render_style`
- `render_name`
- `render_names`

`NameGenerator` supports two input modes:

1. `pattern="simple"` for a tiny built-in preset inventory
2. `source_values=[...]` for explicit caller-supplied value pools

When both concepts matter, `source_values` is the more important one. The
built-in preset is a convenience surface, not the center of the design.

## Determinism Guardrail

This package uses isolated per-call RNG behavior and does not rely on
module-global random state.

This means:

- identical inputs should produce identical outputs
- the library should remain safe to call from APIs, CLIs, tests, and future UIs
- consumers do not need to worry about shared module-global random state being
  mutated elsewhere in the process

## Quickstart

```python
from pipeworks_namegen_core import (
    NameGenerator,
    render_name,
    sample_values,
)

gen = NameGenerator(pattern="simple")
name = gen.generate(seed=42)
print(name)                 # deterministic output for seed 42
print(render_name(name, "upper"))

values = ["alfa", "beta", "gamma"]
print(sample_values(values, count=2, seed=7, unique_only=True))
```

Using explicit caller-supplied values:

```python
from pipeworks_namegen_core import NameGenerator

gen = NameGenerator(source_values=["al", "fa", "beta", "grim"])
print(gen.generate(seed=10, syllables=2))
print(gen.available_values(unique_only=True))
```

Sampling without using `NameGenerator`:

```python
from pipeworks_namegen_core import sample_values

values = ["alfa", "beta", "beta", "gamma"]
print(sample_values(values, count=3, seed=11, unique_only=False))
print(sample_values(values, count=3, seed=11, unique_only=True))
```

Rendering generated names:

```python
from pipeworks_namegen_core import render_names

names = ["alfathin", "grimdor"]
print(render_names(names, "title"))
```

## What Does Not Belong Here

This repo should not grow ownership of:

- HTTP route validation
- SQLite package stores
- imported package metadata or filename-mapping conventions
- deployment templates or host config
- creator workflow orchestration or corpus tooling

If code depends on package ids, database rows, HTTP payloads, or deployment
state, it probably belongs in `pipeworks-namegen-api` or
`pipeworks-namegen-lexicon`, not here.

## Compatibility Note

`pattern="simple"` remains as a convenience preset, but the long-term design
center for this package is explicit deterministic behavior from supplied value
pools rather than hidden runtime state.

The package should therefore evolve toward clearer pure-library contracts, not
toward recreating monolithic runtime behavior inside `core`.
