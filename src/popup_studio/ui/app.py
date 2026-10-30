"""Ventana mínima GTK 4: sección transversal del step-fold con deslizador de ángulo."""
from __future__ import annotations

import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from popup_studio.mechanisms.step_fold import StepFold


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(application=app, title="Popup Studio")
        self.set_default_size(800, 600)
        self.step = StepFold(40, 40)
        self.phi = 90.0

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.area = Gtk.DrawingArea(hexpand=True, vexpand=True)
        self.area.set_draw_func(self._draw)
        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 180, 1)
        scale.set_value(self.phi)
        scale.set_draw_value(True)
        scale.connect("value-changed", self._on_phi)
        box.append(self.area)
        box.append(Gtk.Label(label="Ángulo de apertura φ (grados)"))
        box.append(scale)
        self.set_child(box)

    def _on_phi(self, scale: Gtk.Scale) -> None:
        self.phi = scale.get_value()
        self.area.queue_draw()

    def _draw(self, _area: Gtk.DrawingArea, cr, w: int, h: int) -> None:  # type: ignore[no-untyped-def]
        sec = self.step.cross_section(self.phi)
        k = min(w, h) / 220.0  # px por mm
        ox, oy = w / 2, h * 0.8

        def p(pt: tuple[float, float]) -> tuple[float, float]:
            return ox + pt[0] * k, oy - pt[1] * k

        cr.set_source_rgb(1, 1, 1)
        cr.paint()
        cr.set_source_rgb(0.1, 0.1, 0.1)
        cr.set_line_width(3)
        cr.move_to(*p(sec["S"]))
        for name in ("A", "M", "G", "S"):
            cr.line_to(*p(sec[name]))
        cr.stroke()


class App(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id="io.github.fschpp.PopupStudio")

    def do_activate(self) -> None:
        MainWindow(self).present()


def run() -> int:
    return App().run(sys.argv[:1])
