"""Proyecto, página y ajustes (US-101). Sin dependencias de GTK."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

FORMAT_VERSION = 1


class ValidationError(ValueError):
    """Valor inválido en el modelo del proyecto."""


def _positive(name: str, value: float) -> float:
    if not value > 0:
        raise ValidationError(f"{name} debe ser > 0 (recibido: {value})")
    return float(value)


@dataclass
class Thickness:
    """Espesores en mm; None = pendiente de medir con calibre."""

    cardstock: float | None = None
    sticker: float | None = None
    glue: float | None = None


@dataclass
class Settings:
    design_angle: Literal[90, 180] = 180
    tolerance_mm: float = 0.2
    thickness_mm: Thickness = field(default_factory=Thickness)

    def __post_init__(self) -> None:
        if self.design_angle not in (90, 180):
            raise ValidationError("design_angle debe ser 90 o 180")
        _positive("tolerance_mm", self.tolerance_mm)


@dataclass
class Page:
    """Pliego completo abierto, con el pliegue central en la mitad (pregunta 11)."""

    sheet_mm: tuple[float, float] = (420.0, 297.0)
    fold_orientation: Literal["short_side", "long_side"] = "short_side"
    fold_position_mm: float | None = None  # None = centro

    def __post_init__(self) -> None:
        w, h = self.sheet_mm
        _positive("sheet_mm[0]", w)
        _positive("sheet_mm[1]", h)
        if self.fold_position_mm is None:
            self.fold_position_mm = w / 2 if self.fold_orientation == "short_side" else h / 2
        _positive("fold_position_mm", self.fold_position_mm)

    @property
    def half_depth_mm(self) -> float:
        """Distancia del pliegue al borde, medida perpendicular al pliegue (para V-01)."""
        w, h = self.sheet_mm
        assert self.fold_position_mm is not None
        total = w if self.fold_orientation == "short_side" else h
        return min(self.fold_position_mm, total - self.fold_position_mm)


@dataclass
class Project:
    settings: Settings = field(default_factory=Settings)
    page: Page = field(default_factory=Page)
    elements: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        t = self.settings.thickness_mm
        return {
            "format_version": FORMAT_VERSION,
            "units": "mm",
            "settings": {
                "design_angle": self.settings.design_angle,
                "tolerance_mm": self.settings.tolerance_mm,
                "thickness_mm": {"cardstock": t.cardstock, "sticker": t.sticker, "glue": t.glue},
            },
            "page": {
                "sheet_mm": list(self.page.sheet_mm),
                "central_fold": {
                    "orientation": self.page.fold_orientation,
                    "position_mm": self.page.fold_position_mm,
                },
            },
            "elements": self.elements,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Project:
        if data.get("format_version") != FORMAT_VERSION:
            raise ValidationError(f"format_version no soportada: {data.get('format_version')}")
        s = data["settings"]
        th = s.get("thickness_mm", {})
        settings = Settings(
            design_angle=s["design_angle"],
            tolerance_mm=s["tolerance_mm"],
            thickness_mm=Thickness(th.get("cardstock"), th.get("sticker"), th.get("glue")),
        )
        p = data["page"]
        page = Page(
            sheet_mm=(p["sheet_mm"][0], p["sheet_mm"][1]),
            fold_orientation=p["central_fold"]["orientation"],
            fold_position_mm=p["central_fold"]["position_mm"],
        )
        return cls(settings=settings, page=page, elements=list(data.get("elements", [])))
