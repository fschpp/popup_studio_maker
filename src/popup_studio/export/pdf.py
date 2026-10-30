"""Exportación a PDF 1:1 en milímetros con pycairo (ADR-06, a confirmar en S0.4).

Estilos de línea (plan §7): corte continuo negro; valle discontinuo azul;
montaña guión-punto rojo.
"""
from __future__ import annotations

from pathlib import Path

import cairo

from popup_studio.layout.step_fold_layout import Pattern

MM = 72.0 / 25.4  # puntos por mm
LINE_W = 0.25 * MM

_STYLE = {
    "cut": ((0.0, 0.0, 0.0), []),
    "valley": ((0.0, 0.2, 0.9), [3.0 * MM, 1.5 * MM]),
    "mountain": ((0.85, 0.1, 0.1), [4.0 * MM, 1.2 * MM, 0.6 * MM, 1.2 * MM]),
    "glue": ((0.0, 0.55, 0.2), [1.0 * MM, 1.0 * MM]),
}


def _stroke(cr: cairo.Context, kind: str) -> None:
    rgb, dash = _STYLE[kind]
    cr.set_source_rgb(*rgb)
    cr.set_dash(dash)
    cr.set_line_width(LINE_W)
    cr.stroke()


def draw_pattern(cr: cairo.Context, pat: Pattern, dx: float, dy: float) -> None:
    """Dibuja un patrón con su esquina superior izquierda en (dx, dy) mm."""
    cr.save()
    cr.translate(dx * MM, dy * MM)
    cr.move_to(pat.cut[0][0] * MM, pat.cut[0][1] * MM)
    for x, y in pat.cut[1:]:
        cr.line_to(x * MM, y * MM)
    cr.close_path()
    _stroke(cr, "cut")
    for f in pat.folds:
        cr.move_to(f.p1[0] * MM, f.p1[1] * MM)
        cr.line_to(f.p2[0] * MM, f.p2[1] * MM)
        _stroke(cr, f.kind)
    cr.set_source_rgb(0, 0, 0)
    cr.select_font_face("sans-serif")
    cr.set_font_size(2.5 * MM)
    for lb in pat.labels:
        ext = cr.text_extents(lb.text)
        cr.move_to(lb.at[0] * MM - ext.width / 2, lb.at[1] * MM + ext.height / 2)
        cr.show_text(lb.text)
    cr.restore()


def export_patterns(
    patterns: list[Pattern],
    path: str | Path,
    sheet_mm: tuple[float, float] = (420.0, 297.0),
    margin_mm: float = 10.0,
    gap_mm: float = 5.0,
) -> None:
    """Coloca los patrones en fila (nesting mínimo) y falla si no entran en la hoja."""
    w, h = sheet_mm
    x, y, row_h = margin_mm, margin_mm, 0.0
    placed: list[tuple[Pattern, float, float]] = []
    for pat in patterns:
        x0, y0, x1, y1 = pat.bounds()
        pw, ph = x1 - x0, y1 - y0
        if x + pw > w - margin_mm:  # nueva fila
            x, y, row_h = margin_mm, y + row_h + gap_mm, 0.0
        if x + pw > w - margin_mm or y + ph > h - margin_mm:
            raise ValueError(f"el patrón '{pat.name}' no entra en la hoja {w:g}x{h:g} mm")
        placed.append((pat, x - x0, y - y0))
        x += pw + gap_mm
        row_h = max(row_h, ph)
    surface = cairo.PDFSurface(str(path), w * MM, h * MM)
    cr = cairo.Context(surface)
    for pat, dx, dy in placed:
        draw_pattern(cr, pat, dx, dy)
    surface.finish()


def export_calibration(path: str | Path, sheet_mm: tuple[float, float] = (420.0, 297.0)) -> None:
    """Página de calibración (S0.4): cuadrado de 100 mm para medir tras imprimir al 100 %."""
    w, h = sheet_mm
    surface = cairo.PDFSurface(str(path), w * MM, h * MM)
    cr = cairo.Context(surface)
    cr.rectangle(10 * MM, 10 * MM, 100 * MM, 100 * MM)
    _stroke(cr, "cut")
    cr.set_source_rgb(0, 0, 0)
    cr.set_font_size(3 * MM)
    cr.move_to(12 * MM, 116 * MM)
    cr.show_text("Imprimir al 100 % (sin ajustar a página). El cuadrado debe medir 100 mm.")
    surface.finish()


def export_page_map(
    pattern: Pattern, path: str | Path, sheet_mm: tuple[float, float] = (420.0, 297.0)
) -> None:
    """Exporta un patrón en coordenadas absolutas de la hoja (sin acomodar): mapa de pegado."""
    w, h = sheet_mm
    surface = cairo.PDFSurface(str(path), w * MM, h * MM)
    cr = cairo.Context(surface)
    draw_pattern(cr, pattern, 0.0, 0.0)
    surface.finish()
