"""Validaciones analíticas (subconjunto inicial de V-01 y V-03)."""
from __future__ import annotations

from dataclasses import dataclass

from popup_studio.core.project import Page
from popup_studio.mechanisms.step_fold import StepFold
from popup_studio.mechanisms.v_fold import VFold, closed_footprint


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


def v03_v_fold_balance(a_g: float, b_g: float, a_b: float, b_b: float, tol: float = 1e-6) -> list[Issue]:
    """Balance de ángulos del V-fold: a_g + b_g = a_b + b_b."""
    if abs((a_g + b_g) - (a_b + b_b)) > tol:
        return [Issue("V-03", f"a_g + b_g = {a_g + b_g:g} distinto de a_b + b_b = {a_b + b_b:g}")]
    return []


def v01_v_fold_closes_inside(
    v: VFold,
    length: float,
    glue_g: float,
    glue_b: float,
    apex_y: float,
    sheet_mm: tuple[float, float],
    margin_mm: float = 2.0,
) -> list[Issue]:
    """La pieza cerrada (plana sobre la mitad G) no debe sobresalir de la hoja.

    Coordenadas de página: x = fold_x - y_mec (hacia la izquierda), y = apex_y - x_mec.
    """
    w, h = sheet_mm
    out: list[Issue] = []
    for x_m, y_m in closed_footprint(v, length, glue_g, glue_b):
        px, py = w / 2 - y_m, apex_y - x_m
        if not (margin_mm <= px and margin_mm <= py <= h - margin_mm):
            out.append(
                Issue("V-01", f"con la tarjeta cerrada un vértice cae en ({px:.1f}, {py:.1f}) mm, fuera de la hoja")
            )
    return out
