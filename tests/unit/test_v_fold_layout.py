import math

import pytest
from pypdf import PdfReader
from shapely.geometry import Polygon

from popup_studio.export.pdf import MM, export_page_map, export_patterns
from popup_studio.layout.v_fold_layout import v_fold_page_map, v_fold_pattern
from popup_studio.mechanisms.v_fold import VFold
from popup_studio.validate.rules import v01_v_fold_closes_inside


def test_longitudes_y_angulos_de_la_pieza():
    v = VFold.symmetric(40, 60)
    pat = v_fold_pattern(v, length=50, glue_g=45, glue_b=45)
    crease, gg, gb = pat.folds
    assert math.dist(crease.p1, crease.p2) == pytest.approx(50)
    assert math.dist(gg.p1, gg.p2) == pytest.approx(45)

    def ang(a, b):
        va = (a.p2[0] - a.p1[0], a.p2[1] - a.p1[1])
        vb = (b.p2[0] - b.p1[0], b.p2[1] - b.p1[1])
        return math.degrees(math.acos(
            (va[0] * vb[0] + va[1] * vb[1]) / (math.hypot(*va) * math.hypot(*vb))))

    assert ang(crease, gg) == pytest.approx(60)
    assert ang(crease, gb) == pytest.approx(60)
    assert {f.kind for f in pat.folds} == {"mountain", "valley"}


def test_contorno_es_un_poligono_simple():
    pat = v_fold_pattern(VFold.right_angle(45), 60, 50, 50)
    assert Polygon(pat.cut).is_valid


def test_muy_abierto_se_rechaza_por_solape():
    with pytest.raises(ValueError, match="solapa"):
        v_fold_pattern(VFold.symmetric(10, 165), 60, 50, 50)


@pytest.mark.parametrize("kw", [{"flap": 9}, {"length": 0}, {"corner": 6}])
def test_parametros_invalidos(kw):
    args = {"v": VFold.right_angle(45), "length": 60, "glue_g": 50, "glue_b": 50} | kw
    with pytest.raises(ValueError):
        v_fold_pattern(**args)


def test_mapa_de_pegado_geometria():
    v = VFold.right_angle(45)
    m = v_fold_page_map(v, 120, 120, apex_y=230)
    _, g, b = m.folds
    # a 45° del pliegue central, ambas puntas suben y se alejan lo mismo
    assert g.p2[0] == pytest.approx(210 - 120 * math.sin(math.radians(45)))
    assert b.p2[0] == pytest.approx(210 + 120 * math.sin(math.radians(45)))
    assert g.p2[1] == pytest.approx(230 - 120 * math.cos(math.radians(45)))
    assert {f.kind for f in m.folds} == {"valley", "glue"}


def test_mapa_fuera_de_hoja():
    with pytest.raises(ValueError):
        v_fold_page_map(VFold.right_angle(45), 400, 400, apex_y=230)


def test_v01_cerrada_dentro_y_fuera():
    v, sheet = VFold.right_angle(45), (420.0, 297.0)
    assert v01_v_fold_closes_inside(v, 60, 50, 50, 230, sheet) == []
    # el crease cerrado va hacia abajo-izquierda: con el vértice casi al borde inferior sobresale
    assert v01_v_fold_closes_inside(v, 120, 50, 50, 280, sheet)[0].code == "V-01"


def test_pdfs(tmp_path):
    v = VFold.right_angle(45)
    f1, f2 = tmp_path / "pieza.pdf", tmp_path / "mapa.pdf"
    export_patterns([v_fold_pattern(v, 60, 50, 50)], f1)
    export_page_map(v_fold_page_map(v, 120, 120, 230), f2)
    box = PdfReader(f2).pages[0].mediabox
    assert float(box.width) == pytest.approx(420 * MM, abs=0.1)
    assert f1.stat().st_size > 0
