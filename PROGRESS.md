# PROGRESS

_Última actualización: 2026-10-30_

## Current Focus
Arranque del repo (Fase 0/1 del plan v2.6): esqueleto, núcleo sin GTK y primera pieza con oráculo
(step-fold, apéndice B), antes de los spikes S0.1–S0.6.

## Todo List

### [ ] Todo
- [ ] S0.1 visor GTK 4 + ModernGL (ADR-01) — requiere sesión gráfica en el equipo del cliente
- [ ] S0.2 simulación: resortes vs. proyección de restricciones (ADR-02)
- [ ] S0.3 contorno desde PNG con alfa
- [ ] S0.4 PDF a escala 1:1 con pycairo (ADR-06); imprimir y medir 100 mm
- [ ] S0.5 STL y voxelización 64³/128³
- [ ] S0.6 prototipos en papel (step-fold y box-fold)
- [ ] Rebanada vertical F1: capa plana + step-fold → PDF armado (US-301, US-302, US-601)
- [ ] Tent-fold, v-fold (CR-1), box-fold, cilindro, mecanismo por datos (apéndice D)
- [ ] Datos del cliente: 3 PNG, STL simple, espesores, medidas de la casita (preguntas 3, 13, 14)

### [/] In Progress
- [/] Núcleo: grafo de parches (solo estructura), proyecto/página/ajustes

### [x] Done
- [x] Estructura del repo según plan §24, `pyproject.toml`, README, `docs/plan.md`, ADR-01…08 (stubs)
- [x] `core/project.py` (US-101 parcial: valores ≤ 0 rechazados) y `io/popup_file.py` (ida y vuelta)
- [x] `mechanisms/step_fold.py` con fórmula cerrada; coincide con el apéndice B (≤ 0,05 mm)
- [x] `validate/rules.py`: V-01 y V-03 para step-fold
- [x] CLI `python -m popup_studio step-fold`
- [x] Ventana GTK 4 mínima (`python -m popup_studio gui`): sección del step-fold con deslizador de φ. Sin probar (sin GTK en el entorno de desarrollo)
- [x] Tests: 14 pasan (unitarios + propiedades); ruff y mypy estricto limpios

## Latest Blockers/Discoveries
- Los spikes S0.1 (visor) y S0.4 (impresión real) necesitan el equipo y la impresora del cliente.
- Dependencias de desarrollo: pytest, hypothesis, ruff, mypy, shapely, pycairo (instaladas con pip).
