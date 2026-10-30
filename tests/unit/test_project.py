import pytest

from popup_studio.core.project import Page, Project, Settings, ValidationError
from popup_studio.io import popup_file
from popup_studio.mechanisms.step_fold import StepFold
from popup_studio.validate.rules import v01_closes_inside, v03_balance


def test_crear_proyecto_por_defecto():
    p = Project()
    assert p.page.sheet_mm == (420, 297)
    assert p.page.fold_position_mm == 210
    assert p.settings.design_angle == 180


@pytest.mark.parametrize("kw", [{"sheet_mm": (0, 297)}, {"sheet_mm": (420, -1)}])
def test_rechaza_valores_no_positivos(kw):
    with pytest.raises(ValidationError):
        Page(**kw)
    with pytest.raises(ValidationError):
        Settings(tolerance_mm=0)


def test_ida_y_vuelta(tmp_path):
    p = Project(settings=Settings(design_angle=90), page=Page(sheet_mm=(500, 300)))
    f = tmp_path / "a.popup"
    popup_file.save(p, f)
    assert popup_file.load(f).to_dict() == p.to_dict()


def test_v03_y_v01():
    assert v03_balance(10, 20, 15, 15) == []
    assert v03_balance(10, 20, 15, 16)[0].code == "V-03"
    page = Page()  # mitad = 210 mm
    assert v01_closes_inside(StepFold(40, 40), page) == []
    assert v01_closes_inside(StepFold(120, 100), page)[0].code == "V-01"
