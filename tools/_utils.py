from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

_templates = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)


def get_template(name: str) -> Template:
    return _templates.get_template(name)
