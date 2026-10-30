import math

import pytest

from popup_studio.mechanisms.v_fold import VFold, _dot
from popup_studio.validate.rules import v03_v_fold_balance


def test_casita_a_180_es_vertical():
    c = VFold.right_angle(45).crease_dir(180)
    assert c == pytest.approx((0, 0, 1), abs=1e-9)


def test_simetrico_a_180_formula_cerrada():
    # c_x = cos(beta)/cos(alpha); c_z = sqrt(1 - c_x^2)
    v = VFold.symmetric(45, 60)
    cx = math.cos(math.radians(60)) / math.cos(math.radians(45))
    c = v.crease_dir(180)
    assert c[0] == pytest.approx(cx)
    assert c[1] == pytest.approx(0, abs=1e-9)
    assert c[2] == pytest.approx(math.sqrt(1 - cx**2))


def test_cerrada_queda_plana_en_alfa_mas_beta():
    v = VFold.right_angle(45)
    c = v.crease_dir(0)
    assert c[2] == 0
    assert math.degrees(math.atan2(c[1], c[0])) == pytest.approx(135)
    # y continuidad con una apertura casi nula
    c2 = v.crease_dir(0.5)
    assert c2 == pytest.approx(c, abs=0.02)


def test_desbalanceado_se_rechaza():
    with pytest.raises(ValueError, match="desbalanceado"):
        VFold(45, 90, 45, 80)
    assert v03_v_fold_balance(45, 90, 45, 80)[0].code == "V-03"
    assert v03_v_fold_balance(45, 90, 60, 75) == []


@pytest.mark.parametrize("args", [(0, 90, 0, 90), (95, 40, 95, 40), (45, 180, 45, 180)])
def test_rangos_invalidos(args):
    with pytest.raises(ValueError):
        VFold(*args)


def test_asimetrico_deriva_beta():
    v = VFold.asymmetric(30, 80, 50)
    assert v.b_b == pytest.approx(60)
    assert v.closed_angle == pytest.approx(110)


@pytest.mark.parametrize("phi", range(0, 181, 15))
@pytest.mark.parametrize(
    "v", [VFold.right_angle(45), VFold.symmetric(40, 60), VFold.symmetric(30, 120),
          VFold.asymmetric(30, 80, 50)]
)
def test_rigidez_de_angulos(v, phi):
    g, b = v.glue_dirs(phi)
    c = v.crease_dir(phi)
    assert math.sqrt(_dot(c, c)) == pytest.approx(1)
    assert math.degrees(math.acos(_dot(c, g))) == pytest.approx(v.b_g, abs=1e-6)
    assert math.degrees(math.acos(_dot(c, b))) == pytest.approx(v.b_b, abs=1e-6)
    assert c[2] >= -1e-12


def test_la_punta_sube_al_abrir():
    v = VFold.right_angle(45)
    zs = [v.tip(p, 50)[2] for p in (10, 45, 90, 135, 180)]
    assert zs == sorted(zs)
    assert zs[-1] == pytest.approx(50)
