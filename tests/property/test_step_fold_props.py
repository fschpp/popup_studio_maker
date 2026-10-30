import math

from hypothesis import given
from hypothesis import strategies as st

from popup_studio.mechanisms.step_fold import StepFold

dim = st.floats(min_value=1, max_value=200)


@given(dim, dim, st.floats(min_value=0, max_value=180))
def test_aristas_conservadas_y_sin_nan(h, g, phi):
    p = StepFold(h, g).cross_section(phi)
    assert all(math.isfinite(c) for pt in p.values() for c in pt)
    assert math.isclose(math.dist(p["S"], p["A"]), h, rel_tol=1e-9)
    assert math.isclose(math.dist(p["A"], p["M"]), g, rel_tol=1e-9)


@given(dim, dim)
def test_cerrada_es_plana(h, g):
    assert all(abs(pt[1]) < 1e-9 for pt in StepFold(h, g).cross_section(0).values())
