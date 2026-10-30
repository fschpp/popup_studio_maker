# Popup Studio (nombre provisional)

Aplicación de escritorio para Linux (Python + GTK 4) para diseñar páginas de libros popup:
layout 3D con proxies, simulación de plegado, texturas PNG y exportación de PDFs para papel
sticker sobre cartulina.

- Plan completo: [`docs/plan.md`](docs/plan.md) (v2.6)
- Estado del desarrollo: [`PROGRESS.md`](PROGRESS.md)
- Decisiones de arquitectura: [`docs/adr/`](docs/adr/)

## Desarrollo

```bash
python3 -m venv --system-site-packages .venv   # reutiliza PyGObject del sistema
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check . && mypy
python -m popup_studio step-fold --h 40 --g 40
```

Regla de capas: `core`, `mechanisms`, `sim`, `validate`, `io` **no importan GTK**.
