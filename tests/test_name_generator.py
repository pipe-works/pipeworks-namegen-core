"""Deterministic tests for :mod:`pipeworks_namegen_core.generator`."""

from __future__ import annotations

import pytest

from pipeworks_namegen_core import NameGenerator


class TestBasicGeneration:
    """Validate deterministic single-name behavior."""

    def test_generator_creates_deterministic_names(self) -> None:
        """Same seed must always map to the same generated name."""
        gen = NameGenerator(pattern="simple")

        name1 = gen.generate(seed=42)
        name2 = gen.generate(seed=42)

        assert name1 == name2
        assert isinstance(name1, str)
        assert len(name1) > 0

    def test_different_seeds_produce_different_names(self) -> None:
        """Different seeds should produce different names in normal operation."""
        gen = NameGenerator(pattern="simple")

        name1 = gen.generate(seed=1)
        name2 = gen.generate(seed=2)

        assert name1 != name2

    def test_generator_accepts_pattern_name(self) -> None:
        """Known pattern should initialize without error."""
        gen = NameGenerator(pattern="simple")
        assert gen is not None
        assert "simple" in gen.available_patterns()

    def test_generator_rejects_unknown_pattern(self) -> None:
        """Unknown pattern names should be rejected."""
        with pytest.raises(ValueError, match="Unknown pattern"):
            NameGenerator(pattern="nonexistent")

    def test_generator_accepts_explicit_source_values(self) -> None:
        """Explicit source values should be usable without relying on presets."""
        gen = NameGenerator(source_values=["al", "fa", "beta"])
        assert gen.source_values == ("al", "fa", "beta")
        assert gen.generate(seed=2, syllables=2)

    def test_generator_rejects_empty_explicit_source_values(self) -> None:
        """Blank explicit value pools should fail fast."""
        with pytest.raises(ValueError, match="at least one non-empty value"):
            NameGenerator(source_values=["", "   "])

    def test_generated_names_are_capitalized(self) -> None:
        """Generated names should begin with an uppercase character."""
        gen = NameGenerator(pattern="simple")
        name = gen.generate(seed=1)

        assert name[0].isupper()

    def test_optional_syllable_count(self) -> None:
        """Caller should be able to request explicit syllable count."""
        gen = NameGenerator(pattern="simple")

        short_name = gen.generate(seed=1, syllables=2)
        long_name = gen.generate(seed=2, syllables=3)

        assert isinstance(short_name, str)
        assert isinstance(long_name, str)

    def test_invalid_syllable_count_raises(self) -> None:
        """Invalid syllable count requests should fail fast."""
        gen = NameGenerator(pattern="simple")

        with pytest.raises(ValueError, match="at least 1"):
            gen.generate(seed=1, syllables=0)


class TestBatchGeneration:
    """Validate deterministic batch generation behavior."""

    def test_generate_batch_returns_list(self) -> None:
        """Batch generation should return the requested number of strings."""
        gen = NameGenerator(pattern="simple")
        names = gen.generate_batch(count=5, base_seed=100)

        assert isinstance(names, list)
        assert len(names) == 5
        assert all(isinstance(name, str) for name in names)

    def test_generate_batch_unique_names(self) -> None:
        """Unique mode should avoid duplicate names in the same batch."""
        gen = NameGenerator(pattern="simple")
        names = gen.generate_batch(count=10, base_seed=100, unique=True)

        assert len(names) == len(set(names))

    def test_generate_batch_deterministic(self) -> None:
        """Batch generation must be deterministic for fixed inputs."""
        gen = NameGenerator(pattern="simple")

        batch1 = gen.generate_batch(count=5, base_seed=42)
        batch2 = gen.generate_batch(count=5, base_seed=42)

        assert batch1 == batch2

    def test_available_values_can_dedupe(self) -> None:
        """Generator should expose its resolved pool in stable order."""
        gen = NameGenerator(source_values=["al", "al", "fa"])
        assert gen.available_values() == ["al", "al", "fa"]
        assert gen.available_values(unique_only=True) == ["al", "fa"]
