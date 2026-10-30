import pytest
from pypdf import PdfReader

from popup_studio.export.pdf import MM, export_calibration, export_patterns
from popup_studio.layout.step_fold_layout import step_fold_pattern
from popup_studio.mechanisms.step_fold import StepFold


def test_dimensiones_del_patron():
    pat = step_fold_pattern(StepFold(40, 30), width=60, flap=10)
    x0, y0, x1, y1 = pat.bounds()
    assert (x1 - x0, y1 - y0) == (10 + 30 + 40 + 10, 60)
    xs = sorted(f.p1[0] for f in pat.folds)
    assert xs == [10, 40, 80]  # A, M (tras g=30), G (tras h=40)
    assert {f.kind for f in pat.folds} == {"valley", "mountain"}


@pytest.mark.parametrize("kw", [{"width": 0}, {"width": 50, "flap": 9}, {"width": 50, "corner": 6}])
def test_patron_invalido(kw):
    with pytest.raises(ValueError):
        step_fold_pattern(StepFold(40, 40), **kw)


def _mediabox(path):
    box = PdfReader(path).pages[0].mediabox
    return float(box.width), float(box.height)


def test_pdf_a3_a_escala(tmp_path):
    f = tmp_path / "p.pdf"
    export_patterns([step_fold_pattern(StepFold(40, 40), 60)], f)
    assert f.read_bytes().startswith(b"%PDF")
    w, h = _mediabox(f)
    assert w == pytest.approx(420 * MM, abs=0.1)
    assert h == pytest.approx(297 * MM, abs=0.1)


def test_pdf_pieza_que_no_entra(tmp_path):
    with pytest.raises(ValueError):
        export_patterns([step_fold_pattern(StepFold(40, 40), 60)], tmp_path / "x.pdf",
                        sheet_mm=(50, 50))


def test_calibracion(tmp_path):
    f = tmp_path / "c.pdf"
    export_calibration(f)
    assert f.stat().st_size > 0
