from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for Sternberg old/new probe decisions."""

    old_key: str = "f"
    new_key: str = "j"
    continue_key: str = "space"
    accuracy: float = 0.8
    rt_mean_s: float = 0.28
    rt_sd_s: float = 0.05
    rt_min_s: float = 0.12

    def __post_init__(self) -> None:
        self.accuracy = max(0.0, min(1.0, float(self.accuracy)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))
        self._rng: Any = None

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _rand(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        import random as _py_random

        return float(_py_random.random())

    def _normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        import random as _py_random

        return float(_py_random.gauss(mean, sd))

    def _choose_probe_key(self, obs: Observation, valid_keys: list[str]) -> str:
        expected = ""
        factors = dict(obs.task_factors or {})
        expected = str(factors.get("expected_response_key", "")).strip().lower()

        if expected in valid_keys and self._rand() < self.accuracy:
            return expected

        # Controlled error or fallback branch.
        alternatives = [k for k in valid_keys if k != expected]
        if alternatives:
            return alternatives[0]
        return valid_keys[0]

    def act(self, obs: Observation) -> Action:
        valid_keys = [str(k).strip().lower() for k in list(obs.valid_keys or [])]
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        if self.continue_key in valid_keys:
            return Action(
                key=self.continue_key,
                rt_s=max(self.rt_min_s, self.rt_mean_s - 0.08),
                meta={"source": "task_sampler", "policy": "continue"},
            )

        phase = str(obs.phase or "")
        if phase != "probe_response":
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "phase": phase})

        key = self._choose_probe_key(obs, valid_keys)
        rt_s = max(self.rt_min_s, self._normal(self.rt_mean_s, self.rt_sd_s))
        return Action(
            key=key,
            rt_s=rt_s,
            meta={"source": "task_sampler", "policy": "expected_key_with_accuracy", "accuracy": self.accuracy},
        )
