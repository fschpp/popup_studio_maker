"""Patrón plano del V-fold y mapa de pegado sobre la hoja (plano de pegado, plan §8.4).

Pieza: vértice en (0, 0), crease a lo largo de +x hasta (L, 0); ala G hacia +y (ángulo b_g
respecto del crease) y ala B hacia -y (ángulo b_b). Cada línea de pegado lleva una pestaña de
`flap` mm hacia afuera de su ala. [Propuesta] crease = montaña, líneas de pegado = valle.

Mapa de pegado: pliegue central vertical; G = mitad izquierda, B = mitad derecha; el crease
apunta hacia arriba de la hoja (+x del mecanismo). El vértice se ubica a `apex_y` mm del borde
superior.
"""
from __future__ import annotations

import math

from shapely.geometry import Polygon
from shapely.ops import unary_union

from popup_studio.layout.step_fold_layout import Fold, Label, Pattern, Pt
from popup_studio.mechanisms.v_fold import VFold


def _tab(p0: Pt, p1: Pt, tip: Pt, flap: float, corner: float) -> list[Pt]:
    """Pestaña sobre el segmento p0-p1 hacia el lado opuesto a `tip`, con esquinas recortadas."""
    d = math.dist(p0, p1)
    u = ((p1[0] - p0[0]) / d, (p1[1] - p0[1]) / d)
    n = (-u[1], u[0])
    if n[0] * (tip[0] - p0[0]) + n[1] * (tip[1] - p0[1]) > 0:
        n = (-n[0], -n[1])
    c = corner
    q0 = (p0[0] + n[0] * flap, p0[1] + n[1] * flap)
    q1 = (p1[0] + n[0] * flap, p1[1] + n[1] * flap)
    return [
        p0,
        p1,
        (q1[0] - n[0] * c, q1[1] - n[1] * c),
        (q1[0] - u[0] * c, q1[1] - u[1] * c),
        (q0[0] + u[0] * c, q0[1] + u[1] * c),
        (q0[0] - n[0] * c, q0[1] - n[1] * c),
    ]


def v_fold_pattern(
    v: VFold,
    length: float,
    glue_g: float,
    glue_b: float,
    flap: float = 10.0,
    corner: float = 2.0,
    name: str = "V",
) -> Pattern:
    """Pieza con sus dos pestañas en un solo contorno de corte."""
    if min(length, glue_g, glue_b) <= 0:
        raise ValueError("length, glue_g y glue_b deben ser > 0")
    if flap < 10.0:
        raise ValueError("las pestañas deben medir al menos 10 mm")
    if not 0 <= corner < flap / 2:
        raise ValueError("corner fuera de rango")
    o: Pt = (0.0, 0.0)
    tip: Pt = (length, 0.0)
    bg, bb = math.radians(v.b_g), math.radians(v.b_b)
    pg: Pt = (glue_g * math.cos(bg), glue_g * math.sin(bg))
    pb: Pt = (glue_b * math.cos(bb), -glue_b * math.sin(bb))
    wing_g, wing_b = Polygon([o, pg, tip]), Polygon([o, tip, pb])
    tab_g, tab_b = _tab(o, pg, tip, flap, corner), _tab(o, pb, tip, flap, corner)
    polys = [wing_g, wing_b, Polygon(tab_g), Polygon(tab_b)]
    union = unary_union(polys)
    if union.geom_type != "Polygon" or union.area < sum(p.area for p in polys) - 1e-6:
        raise ValueError("la pieza se solapa en el desarrollo plano (ángulos demasiado abiertos)")
    cut = [(float(x), float(y)) for x, y in union.exterior.coords][:-1]
    folds = [
        Fold(o, tip, "mountain"),
        Fold(o, pg, "valley"),
        Fold(o, pb, "valley"),
    ]
    centroid = lambda pts: (
        sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    )
    labels = [Label(f"{name}-G", centroid(tab_g)), Label(f"{name}-B", centroid(tab_b))]
    return Pattern(name=name, cut=cut, folds=folds, labels=labels)


def v_fold_page_map(
    v: VFold,
    glue_g: float,
    glue_b: float,
    apex_y: float,
    sheet_mm: tuple[float, float] = (420.0, 297.0),
    name: str = "V",
) -> Pattern:
    """Hoja con el pliegue central y las dos líneas de pegado desde el vértice."""
    w, h = sheet_mm
    fx = w / 2
    ag, ab = math.radians(v.a_g), math.radians(v.a_b)
    apex: Pt = (fx, apex_y)
    end_g: Pt = (fx - glue_g * math.sin(ag), apex_y - glue_g * math.cos(ag))
    end_b: Pt = (fx + glue_b * math.sin(ab), apex_y - glue_b * math.cos(ab))
    for e in (end_g, end_b, apex):
        if not (0 <= e[0] <= w and 0 <= e[1] <= h):
            raise ValueError("las líneas de pegado salen de la hoja: acortá el pegado o mové el vértice")
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    return Pattern(
        name=f"{name}-mapa",
        cut=[(0, 0), (w, 0), (w, h), (0, h)],
        folds=[
            Fold((fx, 0), (fx, h), "valley"),
            Fold(apex, end_g, "glue"),
            Fold(apex, end_b, "glue"),
        ],
        labels=[Label(f"{name}-G", mid(apex, end_g)), Label(f"{name}-B", mid(apex, end_b))],
    )
