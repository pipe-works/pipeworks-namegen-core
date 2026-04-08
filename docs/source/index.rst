Pipeworks Namegen Core
======================

Overview
========

``pipeworks-namegen-core`` provides deterministic runtime primitives used by the
Namegen API service and other potential consumers.

The core package is intentionally pure-library only:

- no HTTP server
- no SQLite
- no package import flow
- no deployment/runtime config concerns

Repository Boundary
===================

In the current split:

1. ``pipeworks-namegen-core`` owns deterministic library behavior.
2. ``pipeworks-namegen-api`` owns HTTP/runtime behavior and package-backed
   service semantics.
3. ``pipeworks-namegen-lexicon`` owns corpus, lexicon, and creator-facing
   tooling.

If a function depends on HTTP payloads, SQLite package tables, imported package
metadata, or deployment state, it should not live in ``core``.

Library Surface
===============

- ``pipeworks_namegen_core.NameGenerator``
- ``pipeworks_namegen_core.sample_values``
- ``pipeworks_namegen_core.dedupe_preserve_order``
- ``pipeworks_namegen_core.normalize_render_style``
- ``pipeworks_namegen_core.render_name``
- ``pipeworks_namegen_core.render_names``

Generator Model
===============

``NameGenerator`` supports two modes:

1. a small built-in convenience preset via ``pattern="simple"``
2. explicit caller-supplied value pools via ``source_values=[...]``

The preferred long-term model is explicit values. The built-in preset exists as
convenience, not as an implicit runtime dependency for other repos.

Examples
========

Deterministic generation from a preset:

.. code-block:: python

   from pipeworks_namegen_core import NameGenerator

   gen = NameGenerator(pattern="simple")
   print(gen.generate(seed=42))

Deterministic generation from explicit values:

.. code-block:: python

   from pipeworks_namegen_core import NameGenerator

   gen = NameGenerator(source_values=["al", "fa", "grim", "dor"])
   print(gen.generate(seed=10, syllables=2))

Deterministic sampling without the generator wrapper:

.. code-block:: python

   from pipeworks_namegen_core import sample_values

   values = ["alfa", "beta", "beta", "gamma"]
   print(sample_values(values, count=2, seed=7, unique_only=True))

Rendering helpers:

.. code-block:: python

   from pipeworks_namegen_core import render_names

   print(render_names(["alfador", "grimthin"], "title"))

Determinism Notes
=================

Generation behavior is intentionally deterministic for fixed inputs. The core
library uses isolated RNG instances per call and avoids global RNG mutation.

Built-in preset patterns are convenience surfaces only. The preferred mental
model for the library is deterministic behavior from explicit input values.

Non-Goals
=========

This package should not absorb:

- API request validation
- SQLite-backed generation scopes
- filename-to-class mapping logic
- package option caching
- deployment or host-service rules
