"""Validaciones analíticas (subconjunto inicial de V-01 y V-03)."""
from __future__ import annotations

from dataclasses import dataclass

from popup_studio.core.project import Page
from popup_studio.mechanisms.step_fold import StepFold


@dataclass(frozen=True)
class Issue:
    code: str
    message: str


def v03_balance(a: float, b: float, c: float, d: float, tol: float = 1e-9) -> list[Issue]:
    """Plegabilidad por balance: a + b = c + d."""
    if abs((a + b) - (c + d)) > tol:
        return [Issue("V-03", f"a + b = {a + b:g} distinto de c + d = {c + d:g}")]
    return []


def v01_closes_inside(
    step: StepFold, page: Page, thickness_mm: float = 0.0, margin_mm: float = 2.0
) -> list[Issue]:
    """Cierra plano dentro de la hoja: h + g + espesor + margen < mitad de página."""
    need = step.closed_reach() + thickness_mm + margin_mm
    if need >= page.half_depth_mm:
        return [
            Issue("V-01", f"alcance cerrado {need:g} mm >= mitad de página {page.half_depth_mm:g} mm")
        ]
    return []
