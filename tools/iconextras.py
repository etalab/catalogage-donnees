"""
Generate custom DSFR icon classes

See:
https://gouvfr.atlassian.net/wiki/spaces/DB/pages/222331396/Ic+nes+-+Icons#Pour-les-d%C3%A9veloppeurs
"""

import argparse
from pathlib import Path

from ._utils import get_template

CSS_TEMPLATE = get_template("iconextras.css.j2")


def main(prefix: str, output: Path) -> None:
    client_src = output.parent.parent
    icons_dir = client_src / "assets" / "icons"

    icons = [
        {"name": path.stem, "url": f"../{path.relative_to(client_src)}"}
        for path in sorted(icons_dir.glob("**/*.svg"), key=lambda p: p.stem)
    ]

    css = CSS_TEMPLATE.render({"prefix": prefix, "icons": icons})

    output.write_text(css)

    print("done:", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    main(
        prefix=args.prefix,
        output=args.output,
    )
