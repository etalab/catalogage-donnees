"""
Entity-relation diagram (ERD) GraphViz dot-file generator.

Usage:
    python -m erd db.json -o db.dot

Then pass the result to the GraphViz `dot` tool:
    dot db.dot -T png -o db.png

Inspired by: https://github.com/ehne/ERDot
"""
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

import pydantic


class Spec(pydantic.BaseModel):
    tables: Dict[str, Dict[str, str]] = {}
    enums: Dict[str, List[str]] = {}
    relations: List[str] = []


# NOTE: this would be simpler with a declarative templating tool (e.g. Jinja2),
# but we don't have one in the project at the moment of writing this tool.
# So, imperative we go...

FONT = "Arial"
COLUMN_TYPE_COLOR = "gray40"  # See: https://graphviz.org/doc/info/colors.html

GRAPHVIZ_TEMPLATE = """
digraph G {{
    graph [
        nodesep=0.5;
        rankdir="LR";
        cencentrate=true;
        splines="spline";
        fontname="{font}";
        pad="0.2,0.2"
    ];

    node [shape=plain, fontname="Arial"];
    edge [
        dir=both,
        fontsize=12,
        arrowsize=0.9,
        penwidth=1.0,
        labelangle=32,
        labeldistance=1.8,
        fontname="Arial"
    ];

    {tables}

    {enums}

    {relations}
}}
"""


def render_table(name: str, columns: Dict[str, str]) -> str:
    label_lines = [
        '<table border="0" cellborder="1" cellspacing="0">',
        f"<tr><td><i>{name}</i></td></tr>",
    ]
    for key, type_ in columns.items():
        port = key.replace("+", "").replace("*", "")
        display_name = key.replace("*", "PK ").replace("+", "FK ")
        label_lines += [
            f'<tr><td port="{port}" align="left" cellpadding="5">{display_name}'
            " "
            f'<font color="{COLUMN_TYPE_COLOR}">{type_}</font></td></tr>'
        ]
    label_lines += ["</table>"]
    label = "\n".join(label_lines)

    return f'"{name}" [label=<{label}>];'


def render_enum(name: str, items: List[str]) -> str:
    label_lines = [
        '<table border="0" cellborder="1" cellspacing="0">',
        f"<tr><td><i>{name}</i></td></tr>",
    ]
    label_lines += [
        f'<tr><td align="left" cellpadding="5">{item}</td></tr>' for item in items
    ]
    label_lines += ["</table>"]
    label = "\n".join(label_lines)

    return f'"{name}" [label=<{label}>];'


def render_relation(relation: str) -> str:
    # Example: src:dest_id *--1 dest:id
    m = re.match(
        r"^(?P<source_name>\w+):(?P<source_fk>\w+) (?P<left_cardinality>[\d\+\*])--(?P<right_cardinality>[\d\+\*]) (?P<dest_name>\w+):(?P<dest_pk>\w+)$",  # noqa: E501
        relation,
    )
    assert m is not None, f"Invalid relation format: {relation!r}"

    (
        source_name,
        source_fk,
        left_cardinality,
        right_cardinality,
        dest_name,
        dest_pk,
    ) = m.groups()

    left_props = {
        "*": "arrowtail=ocrow",
        "+": "arrowtail=ocrowtee",
    }.get(left_cardinality, "arrowtail=noneotee")

    right_props = {
        "*": "arrowtail=ocrow",
        "+": "arrowtail=ocrowtee",
    }.get(right_cardinality, "arrowtail=noneotee")

    return "\n".join(
        (
            f'"{source_name}":"{source_fk}"->"{dest_name}":"{dest_pk}" [',
            f"{right_props},",
            f"{left_props},",
            "];",
        )
    )


def render(content: str) -> str:
    spec = Spec(**json.loads(content))

    tables = "\n".join(
        render_table(name, columns) for name, columns in spec.tables.items()
    )
    enums = "\n".join(render_enum(name, items) for name, items in spec.enums.items())
    relations = "\n".join(render_relation(relation) for relation in spec.relations)

    return GRAPHVIZ_TEMPLATE.format(
        font=FONT, tables=tables, enums=enums, relations=relations
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("-o", "--output-file", type=Path)
    args = parser.parse_args()

    content = args.input_file.read_text()
    result = render(content)
    args.output_file.write_text(result)


if __name__ == "__main__":
    main()
