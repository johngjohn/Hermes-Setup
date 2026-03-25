from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Mapping


class TemplateRenderError(ValueError):
    pass


def render_template(template_path: Path, values: Mapping[str, object]) -> str:
    template = Template(template_path.read_text(encoding="utf-8"))
    rendered_values = {key: str(value) for key, value in values.items()}
    try:
        return template.substitute(rendered_values)
    except KeyError as exc:
        missing_key = str(exc).strip("'\"")
        raise TemplateRenderError(f"Missing template value '{missing_key}' for {template_path}") from exc
