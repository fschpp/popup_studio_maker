"""Formato .popup (ADR-05): zip con project.json versionado y assets/."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

from popup_studio.core.project import Project


def save(project: Project, path: str | Path) -> None:
    tmp = Path(str(path) + "~")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("project.json", json.dumps(project.to_dict(), indent=2, ensure_ascii=False))
    tmp.replace(path)  # escritura atómica


def load(path: str | Path) -> Project:
    with zipfile.ZipFile(path) as z:
        return Project.from_dict(json.loads(z.read("project.json")))
