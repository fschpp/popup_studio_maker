import math

import pytest

from popup_studio.mechanisms.step_fold import StepFold

# Oráculo: apéndice B del plan, h = g = 40 mm (tolerancia 0,05 mm)
ORACLE = {
    0: ((40.00, 0.0), (80.00, 0.0)),
    45: ((28.28, 28.28), (68.28, 28.28)),
    90: ((0.0, 40.00), (40.00, 40.00)),
    135: ((-28.28, 28.28), (11.72, 28.28)),
    180: ((-40.00, 0.0), (0.0, 0.0)),
}


@pytest.mark.parametrize("phi", ORACLE)
def test_apendice_b(phi):
    s = StepFold(40, 40).cross_section(phi)
    a, m = ORACLE[phi]
    assert s["A"] == pytest.approx(a, abs=0.05)
    assert s["M"] == pytest.approx(m, abs=0.05)


def test_rigidez_longitudes():
    s = StepFold(30, 55)
    for phi in range(0, 181, 15):
        p = s.cross_section(phi)
        assert math.dist(p["S"], p["A"]) == pytest.approx(30)
        assert math.dist(p["A"], p["M"]) == pytest.approx(55)
        assert math.dist(p["M"], p["G"]) == pytest.approx(30)
        assert math.dist(p["G"], p["S"]) == pytest.approx(55)


def test_parametros_invalidos():
    with pytest.raises(ValueError):
        StepFold(0, 10)
    with pytest.raises(ValueError):
        StepFold(10, 10).cross_section(181)
