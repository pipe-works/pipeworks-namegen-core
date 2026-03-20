"""Public API for ``pipeworks-namegen-core``.

This package is the deterministic generation/runtime styling layer shared by
service/UI consumers.
"""

from .generator import NameGenerator
from .renderer import RENDER_STYLES, normalize_render_style, render_name, render_names
from .version import __version__

__all__ = [
    "NameGenerator",
    "RENDER_STYLES",
    "normalize_render_style",
    "render_name",
    "render_names",
    "__version__",
    "healthcheck",
]


def healthcheck() -> str:
    """Return a small stable value for smoke/integration checks."""
    return "ok"
