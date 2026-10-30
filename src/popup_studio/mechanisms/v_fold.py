"""V-fold (pliegues convergentes), fórmula cerrada. Plan §11.1b, tutorial de Birmingham.

Convención: el pliegue central es el eje x; el vértice (apex) está en el origen. La mitad G
(ground) es el semiplano y >= 0 con z = 0; la mitad B (backdrop) gira alrededor de x con el
ángulo de apertura phi (0 = cerrada, 180 = plana). Direcciones desde el vértice:

    G = (cos aG, sin aG, 0)            línea de pegado sobre G
    B = cos aB * x + sin aB * u(phi)   línea de pegado sobre B, u = (0, cos phi, sin phi)

La arista central de la pieza (crease) c es el vector unitario con c·G = cos bG y
c·B = cos bB; de las dos soluciones simétricas se toma la que sube (z >= 0).
Balance (V-03): aG + bG = aB + bB; es la condición para que cierre plano.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

Vec3 = tuple[float, float, float]

_BALANCE_TOL = 1e-6


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


@dataclass(frozen=True)
class VFold:
    """Ángulos en grados. a = base (pegado vs. pliegue central), b = pieza (pegado vs. crease)."""

    a_g: float
    b_g: float
    a_b: float
    b_b: float

    def __post_init__(self) -> None:
        for name, v in (("a_g", self.a_g), ("a_b", self.a_b)):
            if not 0 < v < 90:
                raise ValueError(f"{name} debe estar entre 0 y 90 grados (recibido: {v})")
        for name, v in (("b_g", self.b_g), ("b_b", self.b_b)):
            if not 0 < v < 180:
                raise ValueError(f"{name} debe estar entre 0 y 180 grados (recibido: {v})")
        if abs((self.a_g + self.b_g) - (self.a_b + self.b_b)) > _BALANCE_TOL:
            raise ValueError(
                f"V-fold desbalanceado: a_g + b_g = {self.a_g + self.b_g:g} "
                f"distinto de a_b + b_b = {self.a_b + self.b_b:g}"
            )
        if self.a_g + self.b_g >= 180:
            raise ValueError("a + b debe ser menor que 180 grados")

    # --- variantes (son valores de parámetros con balance, no mecanismos distintos) ---
    @classmethod
    def right_angle(cls, alpha: float = 45.0) -> VFold:
        """Ángulo recto: ambos ángulos de la pieza valen 90° (la casita: alpha = 45)."""
        return cls(alpha, 90.0, alpha, 90.0)

    @classmethod
    def symmetric(cls, alpha: float, beta: float) -> VFold:
        """Agudo (beta < 90), puntiagudo (beta pequeño) u obtuso (beta > 90), iguales a ambos lados."""
        return cls(alpha, beta, alpha, beta)

    @classmethod
    def asymmetric(cls, a_g: float, b_g: float, a_b: float) -> VFold:
        """Asimétrico: b_b se deriva del balance."""
        return cls(a_g, b_g, a_b, a_g + b_g - a_b)

    @property
    def closed_angle(self) -> float:
        """Dirección del crease con la tarjeta cerrada, medida desde el pliegue central."""
        return self.a_g + self.b_g

    # --- geometría ---
    def glue_dirs(self, phi_deg: float) -> tuple[Vec3, Vec3]:
        if not 0.0 <= phi_deg <= 180.0:
            raise ValueError("phi debe estar entre 0 y 180 grados")
        phi, ag, ab = map(math.radians, (phi_deg, self.a_g, self.a_b))
        g = (math.cos(ag), math.sin(ag), 0.0)
        b = (math.cos(ab), math.sin(ab) * math.cos(phi), math.sin(ab) * math.sin(phi))
        return g, b

    def crease_dir(self, phi_deg: float) -> Vec3:
        """Vector unitario del crease para la apertura phi."""
        g, b = self.glue_dirs(phi_deg)
        cg, cb = math.cos(math.radians(self.b_g)), math.cos(math.radians(self.b_b))
        gb = _dot(g, b)
        det = 1.0 - gb * gb
        if det < 1e-12:  # tarjeta cerrada: el crease queda en el plano de la hoja
            t = math.radians(self.closed_angle)
            return (math.cos(t), math.sin(t), 0.0)
        lam = (cg - gb * cb) / det
        mu = (cb - gb * cg) / det
        nu2 = (1.0 - (lam * cg + mu * cb)) / det
        nu = math.sqrt(max(nu2, 0.0))
        n = _cross(g, b)
        best: Vec3 | None = None
        for s in (1.0, -1.0):
            c = tuple(lam * g[i] + mu * b[i] + s * nu * n[i] for i in range(3))
            if best is None or c[2] > best[2]:
                best = (c[0], c[1], c[2])
        assert best is not None
        return best

    def tip(self, phi_deg: float, length: float) -> Vec3:
        """Punta del crease a `length` mm del vértice."""
        c = self.crease_dir(phi_deg)
        return (c[0] * length, c[1] * length, c[2] * length)


def closed_footprint(
    v: VFold, length: float, glue_g: float, glue_b: float
) -> list[tuple[float, float]]:
    """Vértices de la pieza con la tarjeta cerrada (plana sobre G), en (x, y) del mecanismo:
    vértice, extremo de pegado G, punta del crease y extremo de pegado B (plegado sobre G)."""
    t = math.radians(v.closed_angle)
    ag, ab = math.radians(v.a_g), math.radians(v.a_b)
    return [
        (0.0, 0.0),
        (glue_g * math.cos(ag), glue_g * math.sin(ag)),
        (length * math.cos(t), length * math.sin(t)),
        (glue_b * math.cos(ab), glue_b * math.sin(ab)),
    ]
