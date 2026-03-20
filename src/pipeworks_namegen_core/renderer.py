"""Deterministic name rendering helpers.

This module intentionally provides only lightweight style transforms for
already-generated names. It is designed to be runtime-safe and side-effect free.
"""

from __future__ import annotations

from typing import Sequence

# Explicit style keys make API validation predictable and deterministic.
RENDER_STYLES: set[str] = {"raw", "lower", "upper", "title", "sentence"}


def normalize_render_style(raw_style: str | None) -> str:
    """Normalize and validate a render style value.

    Args:
        raw_style: User-supplied style value. ``None`` and blank strings map to
            ``"raw"``.

    Returns:
        Canonical lower-cased style key.

    Raises:
        ValueError: If style is unknown.
    """
    if raw_style is None:
        return "raw"

    normalized = str(raw_style).strip().lower()
    if not normalized:
        return "raw"

    if normalized not in RENDER_STYLES:
        allowed = ", ".join(sorted(RENDER_STYLES))
        raise ValueError(f"Unknown render style: {raw_style!r}. Allowed: {allowed}.")

    return normalized


def render_name(name: str, style: str | None = None) -> str:
    """Render one name using the provided style.

    Args:
        name: Input name.
        style: Optional style key.

    Returns:
        Rendered name.
    """
    normalized = normalize_render_style(style)

    if normalized == "raw":
        return name
    if normalized == "lower":
        return name.lower()
    if normalized == "upper":
        return name.upper()
    if normalized == "sentence":
        if not name:
            return name
        return name[:1].upper() + name[1:].lower()

    # ``title`` transform intentionally delegates to Python's standard behavior
    # to keep rendering deterministic across all call-sites.
    return name.title()


def render_names(names: Sequence[str], style: str | None = None) -> list[str]:
    """Render a sequence of names with a common style.

    Args:
        names: Input names.
        style: Optional style key.

    Returns:
        New list containing rendered values.
    """
    normalized = normalize_render_style(style)
    if normalized == "raw":
        # Always return a copy so callers can mutate safely without touching the
        # original sequence object they passed in.
        return list(names)

    return [render_name(name, normalized) for name in names]
