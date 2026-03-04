from __future__ import annotations

from dataclasses import dataclass
import random
import re
from typing import Any


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


class SternbergController:
    """Generate Sternberg trial materials and track score/accuracy."""

    def __init__(
        self,
        *,
        letter_pool: list[str],
        probe_old_prob: float,
        random_seed: int,
        score_correct: int = 1,
        score_incorrect: int = 0,
        score_timeout: int = 0,
    ) -> None:
        if not letter_pool:
            raise ValueError("letter_pool must be non-empty")
        self.letter_pool = [str(x) for x in letter_pool]
        self.probe_old_prob = float(probe_old_prob)
        self.rng = random.Random(int(random_seed))

        self.score_correct = int(score_correct)
        self.score_incorrect = int(score_incorrect)
        self.score_timeout = int(score_timeout)

        self._trial_id = 0
        self.total_score = 0
        self.total_trials = 0
        self.total_answered = 0
        self.total_correct = 0

    def next_trial_id(self) -> int:
        self._trial_id += 1
        return int(self._trial_id)

    def build_trial(self, set_size: int) -> TrialSpec:
        if set_size > len(self.letter_pool):
            raise ValueError("set_size cannot exceed letter_pool length")

        memory_items = self.rng.sample(self.letter_pool, k=int(set_size))
        probe_old = bool(self.rng.random() < self.probe_old_prob)

        if probe_old:
            probe_item = str(self.rng.choice(memory_items))
            probe_type = "old"
        else:
            non_members = [x for x in self.letter_pool if x not in memory_items]
            probe_item = str(self.rng.choice(non_members))
            probe_type = "new"

        return TrialSpec(
            set_size=int(set_size),
            memory_items=[str(x) for x in memory_items],
            probe_item=probe_item,
            probe_type=probe_type,
        )

    def apply_score(self, *, is_correct: bool | None, timed_out: bool) -> dict[str, int]:
        score_before = int(self.total_score)
        if timed_out:
            delta = int(self.score_timeout)
        elif bool(is_correct):
            delta = int(self.score_correct)
        else:
            delta = int(self.score_incorrect)
        self.total_score = score_before + delta
        return {"score_before": score_before, "score_delta": int(delta), "score_after": int(self.total_score)}

    def record_trial(self, *, is_correct: bool | None, timed_out: bool) -> None:
        self.total_trials += 1
        if timed_out:
            return
        self.total_answered += 1
        if bool(is_correct):
            self.total_correct += 1

    def accuracy(self) -> float:
        if self.total_answered <= 0:
            return 0.0
        return float(self.total_correct / self.total_answered)
