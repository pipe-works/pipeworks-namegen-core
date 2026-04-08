"""Tests for deterministic sampling helpers."""

from __future__ import annotations

import pytest

from pipeworks_namegen_core import dedupe_preserve_order, sample_values


def test_dedupe_preserve_order_keeps_first_seen_values() -> None:
    """Deduplication helper should preserve first-seen order."""
    assert dedupe_preserve_order(["alfa", "beta", "alfa", "gamma"]) == [
        "alfa",
        "beta",
        "gamma",
    ]


def test_sample_values_unique_mode_is_deterministic() -> None:
    """Unique deterministic sampling should be stable for a fixed seed."""
    first = sample_values(["alfa", "beta", "beta"], count=2, seed=7, unique_only=True)
    second = sample_values(["alfa", "beta", "beta"], count=2, seed=7, unique_only=True)
    assert first == second
    assert sorted(first) == ["alfa", "beta"]


def test_sample_values_non_unique_mode_allows_repetition() -> None:
    """Non-unique mode should sample with replacement."""
    sampled = sample_values(["alfa"], count=3, seed=1, unique_only=False)
    assert sampled == ["alfa", "alfa", "alfa"]


def test_sample_values_rejects_negative_count() -> None:
    """Negative count should fail fast."""
    with pytest.raises(ValueError, match="count must be >= 0"):
        sample_values(["alfa"], count=-1, seed=1, unique_only=False)
