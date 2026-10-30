"""Patrón plano del step-fold: tira con pestaña en A, parche AM, parche MG y pestaña en G.

Coordenadas en mm, origen en la esquina superior izquierda de la tira; x a lo largo de la
tira (de la pestaña de A a la de G) e y a lo largo del pliegue central (ancho `width`).
[Propuesta] Asignación de plegados: A y G valle, M montaña; se valida en el prototipo S0.6.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from popup_studio.mechanisms.step_fold import StepFold

Pt = tuple[float, float]
FoldKind = Literal["mountain", "valley", "glue"]


@dataclass(frozen=True)
class Fold:
    p1: Pt
    p2: Pt
    kind: FoldKind


@dataclass(frozen=True)
class Label:
    text: str
    at: Pt


@dataclass
class Pattern:
    name: str
    cut: list[Pt]  # contorno cerrado de corte
    folds: list[Fold] = field(default_factory=list)
    labels: list[Label] = field(default_factory=list)

    def bounds(self) -> tuple[float, float, float, float]:
        xs = [p[0] for p in self.cut]
        ys = [p[1] for p in self.cut]
        return min(xs), min(ys), max(xs), max(ys)


def step_fold_pattern(
    step: StepFold, width: float, flap: float = 10.0, corner: float = 2.0, name: str = "step"
) -> Pattern:
    """Pestañas >= 10 mm (regla de oficio); esquinas recortadas para que no se enganchen."""
    if width <= 0:
        raise ValueError("width debe ser > 0")
    if flap < 10.0:
        raise ValueError("las pestañas deben medir al menos 10 mm")
    if not 0 <= corner < min(flap, width) / 2:
        raise ValueError("corner fuera de rango")
    xa = flap  # pliegue en A
    xm = xa + step.g  # pliegue en M (parche AM mide g)
    xg = xm + step.h  # pliegue en G (parche MG mide h)
    xe = xg + flap
    w, c = width, corner
    cut: list[Pt] = [
        (0, c), (c, 0), (xa, 0), (xg, 0), (xe - c, 0), (xe, c),
        (xe, w - c), (xe - c, w), (xg, w), (xa, w), (c, w), (0, w - c),
    ]
    folds = [
        Fold((xa, 0), (xa, w), "valley"),
        Fold((xm, 0), (xm, w), "mountain"),
        Fold((xg, 0), (xg, w), "valley"),
    ]
    labels = [
        Label(f"{name}-A", (flap / 2, w / 2)),
        Label(f"{name}-G", (xg + flap / 2, w / 2)),
    ]
    return Pattern(name=name, cut=cut, folds=folds, labels=labels)
