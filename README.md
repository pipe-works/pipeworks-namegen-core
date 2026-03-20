# pipeworks-namegen-core

`pipeworks-namegen-core` is the deterministic runtime library for name generation.

## Scope

- deterministic generation primitives (`NameGenerator`)
- deterministic rendering helpers (`render_name`, `render_names`)
- no HTTP server, UI assets, or SQLite/runtime service concerns

## Determinism Guardrail

This package uses isolated RNG instances (`random.Random(seed)`) and does not rely
on module-global random state.

## Quickstart

```python
from pipeworks_namegen_core import NameGenerator, render_name

gen = NameGenerator(pattern="simple")
name = gen.generate(seed=42)
print(name)                 # deterministic output for seed 42
print(render_name(name, "upper"))
```
