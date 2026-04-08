"""Public API for ``pipeworks-namegen-core``.

This package is the deterministic generation/runtime styling layer shared by
service/UI consumers.
"""

from .generator import NameGenerator
from .renderer import RENDER_STYLES, normalize_render_style, render_name, render_names
from .sampler import dedupe_preserve_order, sample_values
from .version import __version__

__all__ = [
    "NameGenerator",
    "RENDER_STYLES",
    "dedupe_preserve_order",
    "normalize_render_style",
    "render_name",
    "render_names",
    "sample_values",
    "__version__",
    "healthcheck",
]


def healthcheck() -> str:
    """Return a small stable value for smoke/integration checks."""
    return "ok"
