"""Deterministic name generation primitives for Pipeworks namegen.

This module intentionally keeps the runtime generation behavior small and
predictable:

1. deterministic random number generation via ``random.Random(seed)``
2. a minimal built-in syllable inventory for the ``simple`` pattern
3. no external runtime dependencies

The extraction goal for ``pipeworks-namegen-core`` is to preserve behavior that
already exists in the legacy ``pipeworks_name_generation`` runtime while
moving it into a dedicated library boundary.
"""

from __future__ import annotations

import random


class NameGenerator:
    """Generate phonetically-plausible names deterministically.

    The primary invariant is deterministic output:
    given identical inputs, this generator must always return identical values.

    Args:
        pattern: Pattern set name. Currently only ``"simple"`` is supported.

    Raises:
        ValueError: If ``pattern`` is not recognized.
    """

    # Hardcoded syllable inventory retained from the legacy runtime.
    # Keeping this list in-core avoids runtime dependency on build-time assets
    # while extraction/migration is in progress.
    _SIMPLE_SYLLABLES = [
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
    ]

    def __init__(self, pattern: str) -> None:
        """Create a generator bound to one pattern set.

        Args:
            pattern: Pattern set name. Only ``"simple"`` is currently allowed.

        Raises:
            ValueError: If ``pattern`` is unknown.
        """
        if pattern != "simple":
            raise ValueError(
                f"Unknown pattern: '{pattern}'. "
                f"Only 'simple' is currently supported in core extraction."
            )

        self.pattern = pattern
        # Copy to protect class-level constant from accidental mutation.
        self._syllables = self._SIMPLE_SYLLABLES.copy()

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
        # nosec B311: this is deterministic game content generation,
        # not cryptographic randomness.
        rng = random.Random(seed)  # nosec B311

        if syllables is None:
            syllables = rng.randint(2, 3)

        if syllables < 1:
            raise ValueError("Syllable count must be at least 1")
        if syllables > len(self._syllables):
            raise ValueError(
                f"Cannot generate {syllables} syllables with only "
                f"{len(self._syllables)} available syllables"
            )

        # ``sample`` gives non-repeating selections which avoids generated names
        # containing the exact same source syllable multiple times.
        chosen = rng.sample(self._syllables, k=syllables)
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
        return f"NameGenerator(pattern='{self.pattern}')"
