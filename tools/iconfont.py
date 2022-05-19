"""
Generate custom icon font from RemixIcon icons using the Fontello API

See: https://remixicon.com/
See: https://github.com/fontello/fontello (MIT)
"""

import argparse
import base64
import io
import json
import secrets
import string
import textwrap
import zipfile
from pathlib import Path
from xml.dom import minidom

import httpx
import svg_path_transform


def _extract_svg_path(source: str) -> str:
    # Extract $PATH in <svg><path d="$PATH"></svg>
    doc = minidom.parseString(source)
    (path,) = [el.getAttribute("d") for el in doc.getElementsByTagName("path")]
    doc.unlink()
    return path


def _scale_svg_path(path: str, s: float) -> str:
    # See: https://pypi.org/project/svg-path-transform/
    parsed_path = svg_path_transform.parse_path(path)
    parsed_path = svg_path_transform.translate_and_scale(parsed_path, s=(s, s))
    return svg_path_transform.path_to_string(parsed_path)


def _make_fontello_config(name: str, prefix: str, icons_dir: Path) -> dict:
    # See config format here:
    # https://github.com/fontello/fontello/blob/master/server/fontello/font/_lib/config_schema.js

    glyphs = []

    for k, path in enumerate(icons_dir.glob("**/*.svg")):
        icon_name = path.stem
        icon_code = (
            f"e{800 + k}"  # Character codepoint, e.g. "content: '\e800';" in CSS
        )

        svg_path = _extract_svg_path(path.read_text())

        # XXX: Adjust scale, as Fontello expects SVG paths in 1000x1000,
        # but RemixIcon exports SVGs containing paths in 24x24.
        svg_path = _scale_svg_path(svg_path, 1000 / 24)

        glyph = {
            "uid": secrets.token_hex(16),
            "css": icon_name,
            "code": int(icon_code, 16),
            "src": "custom_icons",
            "selected": True,
            "svg": {
                "path": svg_path,
                "width": 1000,
            },
        }
        glyphs.append(glyph)

    return {
        "name": name,
        "css_prefix_text": prefix,
        "css_use_suffix": False,
        "hinting": True,
        "units_per_em": 1000,
        "ascent": 850,
        "glyphs": glyphs,
    }


def main(name: str, prefix: str, icons_dir: Path, output: Path) -> None:
    fontello_config = _make_fontello_config(name, prefix, icons_dir)

    with httpx.Client() as client:
        # Generate font from config via Fontello API.
        # See: https://github.com/fontello/fontello#developers-api

        files = {"config": json.dumps(fontello_config).encode("utf-8")}
        response = client.post("https://fontello.com/", files=files)
        session_id = response.text
        response = client.get(f"https://fontello.com/{session_id}/get")

        # Font package is a ZIP file containing various items.
        # We want the main CSS and font files.

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:

            def findname(value: str) -> str:
                return next(name for name in zf.namelist() if value in name)

            css = zf.read(findname(f"{name}.css")).decode("utf-8")
            woff2 = zf.read(findname(f"{name}.woff2"))

        # The default CSS does not fit our use case exactly.
        # Instead, generate it explicitly, with the generated font embedded.

        css_template = textwrap.dedent(
            """\
            /* GENERATED -- Do not modify */

            @font-face {
              font-family: "$name";
              src: url("data:application/octet-stream;base64,$font_data")
                format("woff");
              font-weight: normal;
              font-style: normal;
            }

            [class^="$prefix"]::before,
            [class*=" $prefix"]::before {
              font-family: $name !important;
            }

            $icon_classes
            """
        )

        variables = {
            "name": name,
            "prefix": prefix,
            "font_data": base64.b64encode(woff2).decode("utf-8"),
            "icon_classes": "\n".join(
                f"/* prettier-ignore */\n{line}"
                for line in sorted(css.splitlines())
                if line.startswith(f".{prefix}")
            ),
        }

        css = string.Template(css_template).substitute(variables)

        output.write_text(css)

        print("done:", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name")
    parser.add_argument("--prefix")
    parser.add_argument("--icons-dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    main(
        name=args.name,
        prefix=args.prefix,
        icons_dir=args.icons_dir,
        output=args.output,
    )
