"""Step-fold / pliegue paralelo: fórmula cerrada (apéndice B del plan).

Sección transversal en el plano y–z (perpendicular al pliegue central).
Ground a lo largo de +y; backdrop a lo largo de u(phi) = (cos phi, sin phi).
A = h·u(phi) (sobre el backdrop), G = (g, 0) (sobre el ground), M = A + G.
Longitudes: SA = h, AM = g, MG = h, GS = g  =>  a + b = c + d (V-03).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

Point = tuple[float, float]


@dataclass(frozen=True)
class StepFold:
    h: float  # distancia del pegado al pliegue sobre el backdrop
    g: float  # distancia del pegado al pliegue sobre el ground

    def __post_init__(self) -> None:
        if not (self.h > 0 and self.g > 0):
            raise ValueError("h y g deben ser > 0")

    def cross_section(self, phi_deg: float) -> dict[str, Point]:
        """Puntos S, A, M, G (y, z) para el ángulo de apertura phi (0..180°)."""
        if not 0.0 <= phi_deg <= 180.0:
            raise ValueError("phi debe estar entre 0 y 180 grados")
        phi = math.radians(phi_deg)
        a = (self.h * math.cos(phi), self.h * math.sin(phi))
        g = (self.g, 0.0)
        m = (a[0] + g[0], a[1] + g[1])
        return {"S": (0.0, 0.0), "A": a, "M": m, "G": g}

    def closed_reach(self) -> float:
        """Alcance desde el pliegue con la tarjeta cerrada (phi = 0): h + g (V-01)."""
        return self.h + self.g
