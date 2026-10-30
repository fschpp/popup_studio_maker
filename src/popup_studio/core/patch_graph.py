"""Grafo de parches (ADR-03): parches planos, bisagras y pegados."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np
from numpy.typing import NDArray

Vec = NDArray[np.float64]


@dataclass(frozen=True)
class Hinge:
    patch_a: str
    patch_b: str
    kind: Literal["rigid", "elastic"] = "rigid"
    fold: Literal["mountain", "valley"] = "valley"


@dataclass(frozen=True)
class Glue:
    """Pestaña de `flap_patch` pegada sobre `target_patch`."""

    flap_patch: str
    target_patch: str


@dataclass
class PatchGraph:
    patches: dict[str, Vec] = field(default_factory=dict)  # id -> polígono 2D (N,2) en mm
    hinges: list[Hinge] = field(default_factory=list)
    glues: list[Glue] = field(default_factory=list)

    def add_patch(self, pid: str, polygon: list[tuple[float, float]]) -> None:
        if pid in self.patches:
            raise ValueError(f"parche duplicado: {pid}")
        self.patches[pid] = np.asarray(polygon, dtype=float)

    def add_hinge(self, h: Hinge) -> None:
        for pid in (h.patch_a, h.patch_b):
            if pid not in self.patches:
                raise KeyError(pid)
        self.hinges.append(h)
