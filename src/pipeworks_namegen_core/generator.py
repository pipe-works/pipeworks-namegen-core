"""Deterministic name generation primitives for PipeWorks namegen core.

The core library intentionally stays small and pure:

1. deterministic generation from explicit value pools
2. optional built-in preset inventories for convenience
3. no HTTP, SQLite, package-import, or deployment concerns
"""

from __future__ import annotations

from typing import Sequence

from pipeworks_namegen_core.sampler import dedupe_preserve_order


class NameGenerator:
    """Generate deterministic names from an internal syllable/value pool.

    The primary invariant is stable output for identical inputs.

    Args:
        pattern: Optional built-in preset name. Currently only ``"simple"`` is
            provided.
        source_values: Optional explicit value pool. When provided, it replaces
            any preset pattern inventory.

    Raises:
        ValueError: If no usable value pool can be resolved.
    """

    _PRESET_VALUE_POOLS: dict[str, tuple[str, ...]] = {
        "simple": (
            "ka",
            "la",
            "thin",
            "mar",
            "in",
            "del",
            "so",
            "ra",
            "vyn",
            "tha",
            "len",
            "is",
            "el",
            "an",
            "dor",
            "mir",
            "eth",
            "al",
            "grim",
            "thor",
            "ak",
            "bor",
            "din",
            "wyn",
            "krag",
            "durn",
            "mok",
            "gor",
            "thrak",
            "zar",
        ),
    }

    def __init__(
        self,
        pattern: str = "simple",
        *,
        source_values: Sequence[str] | None = None,
    ) -> None:
        """Create a generator bound to one resolved value pool.

        Args:
            pattern: Built-in preset name used when ``source_values`` is not
                provided.
            source_values: Optional explicit value pool.

        Raises:
            ValueError: If the resolved pool is empty or invalid.
        """
        self.pattern = pattern
        self._source_values = self._resolve_source_values(
            pattern=pattern, source_values=source_values
        )

    @classmethod
    def available_patterns(cls) -> tuple[str, ...]:
        """Return known built-in preset names."""
        return tuple(sorted(cls._PRESET_VALUE_POOLS))

    @classmethod
    def _resolve_source_values(
        cls,
        *,
        pattern: str,
        source_values: Sequence[str] | None,
    ) -> tuple[str, ...]:
        """Resolve the internal value pool from explicit values or a preset."""
        if source_values is not None:
            normalized = [str(value).strip() for value in source_values if str(value).strip()]
            if not normalized:
                raise ValueError("source_values must contain at least one non-empty value.")
            return tuple(normalized)

        preset = cls._PRESET_VALUE_POOLS.get(pattern)
        if preset is None:
            allowed = ", ".join(cls.available_patterns())
            raise ValueError(f"Unknown pattern: {pattern!r}. Allowed patterns: {allowed}.")
        return tuple(preset)

    def generate(self, seed: int, syllables: int | None = None) -> str:
        """Generate one deterministic name.

        Args:
            seed: Deterministic seed value.
            syllables: Number of syllables to include. If ``None``, a deterministic
                random value in ``[2, 3]`` is used.

        Returns:
            Generated name with first character capitalized.

        Raises:
            ValueError: If requested syllable count is out of range.
        """
        from pipeworks_namegen_core.sampler import sample_values

        if syllables is None:
            syllables = 2 if seed % 2 == 0 else 3

        if syllables < 1:
            raise ValueError("Syllable count must be at least 1")
        if syllables > len(self._source_values):
            raise ValueError(
                f"Cannot generate {syllables} syllables with only "
                f"{len(self._source_values)} available values"
            )

        chosen = sample_values(
            self._source_values,
            count=syllables,
            seed=seed,
            unique_only=True,
        )
        return "".join(chosen).capitalize()

    def generate_batch(self, count: int, base_seed: int, unique: bool = True) -> list[str]:
        """Generate multiple names using incremental deterministic seeds.

        The batch behavior is deterministic because each candidate is generated
        from ``base_seed + offset``.

        Args:
            count: Number of names to return.
            base_seed: Seed used for the first generated name.
            unique: When ``True``, enforce uniqueness within the batch.

        Returns:
            List of generated names.

        Raises:
            ValueError: If a unique batch cannot be satisfied within bounded
                attempts.
        """
        if count < 0:
            raise ValueError("count must be >= 0")

        names: list[str] = []
        seed = base_seed
        attempts = 0
        max_attempts = count * 100

        while len(names) < count and attempts < max_attempts:
            name = self.generate(seed=seed)

            if unique and name in names:
                seed += 1
                attempts += 1
                continue

            names.append(name)
            seed += 1
            attempts += 1

        if len(names) < count:
            raise ValueError(
                f"Could not generate {count} unique names. "
                f"Only generated {len(names)}. Try a larger syllable pool."
            )

        return names

    def __repr__(self) -> str:
        """Return debug representation including selected pattern."""
        return (
            f"NameGenerator(pattern='{self.pattern}', "
            f"source_values={len(self._source_values)} items)"
        )

    @property
    def source_values(self) -> tuple[str, ...]:
        """Return the resolved internal value pool."""
        return self._source_values

    def available_values(self, *, unique_only: bool = False) -> list[str]:
        """Return the internal value pool as a list.

        Args:
            unique_only: When ``True``, remove duplicates while preserving
                first-seen order.
        """
        if unique_only:
            return dedupe_preserve_order(self._source_values)
        return list(self._source_values)
