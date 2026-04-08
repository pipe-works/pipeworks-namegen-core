"""Deterministic sampling helpers for PipeWorks namegen core.

This module provides pure value-sampling primitives with no knowledge of HTTP,
SQLite, package metadata, or deployment concerns. It exists so runtime
consumers can share deterministic selection behavior without re-implementing
local RNG handling.
"""

from __future__ import annotations

import random
from typing import Sequence


def dedupe_preserve_order(values: Sequence[str]) -> list[str]:
    """Return unique values while preserving first-seen order."""
    return list(dict.fromkeys(str(value) for value in values))


def sample_values(
    values: Sequence[str],
    *,
    count: int,
    seed: int | None,
    unique_only: bool,
) -> list[str]:
    """Sample values deterministically from a candidate pool.

    Args:
        values: Candidate values to sample from.
        count: Number of values to return.
        seed: Optional deterministic seed. ``None`` uses a fresh local RNG.
        unique_only: When ``True``, values are de-duplicated before sampling.

    Returns:
        Sampled values.

    Raises:
        ValueError: If ``count`` is negative.
    """
    if count < 0:
        raise ValueError("count must be >= 0")

    # Non-cryptographic sampling is intentional for deterministic content
    # generation, not for security-sensitive randomness.
    rng = random.Random(seed) if seed is not None else random.Random()  # nosec B311

    if unique_only:
        unique_values = dedupe_preserve_order(values)
        if not unique_values or count == 0:
            return []
        if count >= len(unique_values):
            shuffled = list(unique_values)
            rng.shuffle(shuffled)
            return shuffled
        return rng.sample(unique_values, k=count)

    normalized_values = [str(value) for value in values]
    if not normalized_values or count == 0:
        return []
    return [str(rng.choice(normalized_values)) for _ in range(count)]  # nosec B311


__all__ = ["dedupe_preserve_order", "sample_values"]
