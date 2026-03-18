from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any
import random


def parse_set_size(condition_label: Any, default_size: int = 3) -> int:
    """Parse set size from labels like `set3`, `load_5`, `size7`."""
    text = str(condition_label).strip().lower()
    match = re.search(r"(\d+)", text)
    if not match:
        return int(default_size)
    return max(1, int(match.group(1)))


@dataclass
class TrialSpec:
    set_size: int
    memory_items: list[str]
    probe_item: str
    probe_type: str  # old | new


def _normalize_letter_pool(values: Any) -> list[str]:
    if not isinstance(values, (list, tuple)):
        raise TypeError("letter_pool must be a sequence of stimulus items")

    letters = [str(value).strip().upper() for value in values if str(value).strip()]
    if not letters:
        raise ValueError("letter_pool must be non-empty")
    return letters


def sample_trial_spec(
    *,
    rng: random.Random,
    set_size: int,
    letter_pool: Any,
    probe_old_prob: Any,
) -> TrialSpec:
    pool = _normalize_letter_pool(letter_pool)
    size = int(set_size)
    if size > len(pool):
        raise ValueError("set_size cannot exceed letter_pool length")

    old_prob = max(0.0, min(1.0, float(probe_old_prob)))
    memory_items = rng.sample(pool, k=size)
    probe_old = bool(rng.random() < old_prob)

    if probe_old:
        probe_item = str(rng.choice(memory_items))
        probe_type = "old"
    else:
        non_members = [item for item in pool if item not in memory_items]
        if not non_members:
            raise ValueError("letter_pool must include at least one non-member item for new probes")
        probe_item = str(rng.choice(non_members))
        probe_type = "new"

    return TrialSpec(
        set_size=size,
        memory_items=[str(item) for item in memory_items],
        probe_item=probe_item,
        probe_type=probe_type,
    )
