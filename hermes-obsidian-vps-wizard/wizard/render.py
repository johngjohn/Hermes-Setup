from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Mapping


def render_template(template_path: Path, values: Mapping[str, object]) -> str:
    template = Template(template_path.read_text(encoding="utf-8"))
    return template.safe_substitute({key: str(value) for key, value in values.items()})
