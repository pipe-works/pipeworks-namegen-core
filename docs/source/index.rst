Pipeworks Namegen Core
======================

Overview
========

``pipeworks-namegen-core`` provides deterministic runtime primitives used by the
Namegen API service and other potential consumers.

Library Surface
===============

- ``pipeworks_namegen_core.NameGenerator``
- ``pipeworks_namegen_core.normalize_render_style``
- ``pipeworks_namegen_core.render_name``
- ``pipeworks_namegen_core.render_names``

Determinism Notes
=================

Generation behavior is intentionally deterministic for fixed inputs. The core
library uses isolated RNG instances per call and avoids global RNG mutation.
