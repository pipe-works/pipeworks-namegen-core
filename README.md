[![CI](https://github.com/pipe-works/pipeworks-namegen-core/actions/workflows/ci.yml/badge.svg)](https://github.com/pipe-works/pipeworks-namegen-core/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/pipe-works/pipeworks-namegen-core/branch/main/graph/badge.svg)](https://codecov.io/gh/pipe-works/pipeworks-namegen-core) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# pipeworks-namegen-core

`pipeworks-namegen-core` is the pure deterministic name-generation library in
the PipeWorks namegen split. It owns the small, reusable primitives that higher
layers build on: deterministic sampling, deterministic rendering, and the
`NameGenerator` abstraction.

## PipeWorks Workspace

These repositories are designed to live inside a shared PipeWorks workspace
rooted at `/srv/work/pipeworks`.

- `repos/` contains source checkouts only.
- `venvs/` contains per-project virtual environments such as `pw-mud-server`.
- `runtime/` contains mutable runtime state such as databases, exports, session
  files, and caches.
- `logs/` contains service-owned log output when a project writes logs outside
  the process manager.
- `config/` contains workspace-level configuration files that should not be
  treated as source.
- `bin/` contains optional workspace helper scripts.
- `home/` is reserved for workspace-local user data when a project needs it.

Across the PipeWorks ecosphere, the rule is simple: keep source in `repos/`,
keep mutable state outside the repo checkout, and use explicit paths between
repos when one project depends on another.

## What This Repo Owns

This repository is the source of truth for:

- deterministic name generation via `NameGenerator`
- deterministic value sampling via `sample_values`
- deterministic rendering helpers such as `render_name` and `render_names`
- a small public API intended to be embedded by runtime and UI consumers

This repository does not own:

- HTTP endpoints or browser applications
- SQLite storage, package import, or runtime user state
- corpus extraction, syllable-walk tooling, or package authoring

## Public API

Current top-level exports are:

- `NameGenerator`
- `sample_values`
- `dedupe_preserve_order`
- `render_name`
- `render_names`
- `normalize_render_style`
- `RENDER_STYLES`
- `healthcheck`

The design goal is stable behavior for identical inputs. This package should be
side-effect free and boring to depend on.

## Repository Layout

- `src/pipeworks_namegen_core/generator.py` deterministic generation primitives
- `src/pipeworks_namegen_core/sampler.py` deterministic value selection helpers
- `src/pipeworks_namegen_core/renderer.py` render-style transforms
- `tests/` pytest coverage for generator, sampler, renderer, and smoke checks
- `docs/` project documentation

## Quick Start

Create a dedicated workspace venv and install the package in editable mode:

```bash
python3 -m venv /srv/work/pipeworks/venvs/pw-namegen-core
/srv/work/pipeworks/venvs/pw-namegen-core/bin/pip install -e ".[dev]"
```

Minimal usage:

```python
from pipeworks_namegen_core import NameGenerator, render_name, sample_values

generator = NameGenerator(source_values=["ka", "la", "dor", "mir"])
name = generator.generate(seed=42)
styled = render_name(name, style="title")

pool = sample_values(["ash", "elm", "rowan", "thorn"], count=2, seed=7, unique_only=True)
```

## Relationship To The Other Namegen Repos

- `pipeworks-namegen-core`
  pure deterministic library boundary
- `pipeworks-namegen-api`
  canonical runtime HTTP contract and service-owned persistence
- `pipeworks-namegen-lexicon`
  creator tooling, corpus pipeline, package authoring, and consumer web apps

The split is intentional. If a feature needs HTTP, persistence, package import,
or browser workflow concerns, it probably does not belong here.

## Development

Run the local checks from the repo root:

```bash
/srv/work/pipeworks/venvs/pw-namegen-core/bin/pytest
/srv/work/pipeworks/venvs/pw-namegen-core/bin/ruff check src tests
/srv/work/pipeworks/venvs/pw-namegen-core/bin/black --check src tests
/srv/work/pipeworks/venvs/pw-namegen-core/bin/mypy src
```

If you need the docs toolchain:

```bash
/srv/work/pipeworks/venvs/pw-namegen-core/bin/pip install -e ".[docs]"
make -C docs html
```

## Documentation

Additional documentation lives in `docs/`.

## License

[GPL-3.0-or-later](LICENSE)
