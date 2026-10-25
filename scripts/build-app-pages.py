#!/usr/bin/env python3
"""Render the shared app templates to committed, directly servable HTML."""

import argparse
from html import escape
import json
from pathlib import Path
from string import Template
from textwrap import indent


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    ("overview", "index.html", "Overview"),
    ("support", "support.html", "Support"),
    ("privacy", "privacy-policy.html", "Privacy"),
)


def template(name, **values):
    source = (ROOT / "_templates" / name).read_text(encoding="utf-8")
    return Template(source).substitute(values).rstrip()


def render_page(app, page, label):
    page_settings = app["pages"][page]
    app_name = escape(app["name"], quote=True)
    content = (
        ROOT / "_content" / app["slug"] / (page + ".html")
    ).read_text(encoding="utf-8").strip()
    values = {"app_name": app_name, "content": content}

    if page == "overview":
        if app.get("app_store_url"):
            availability = template(
                "store-link.html",
                app_name=app_name,
                app_store_url=escape(app["app_store_url"], quote=True),
            )
        else:
            availability = '<p class="release-status">{}</p>'.format(
                escape(app["release_status"])
            )
        values.update(
            icon=escape(app["icon"]["src"], quote=True),
            icon_width=app["icon"]["width"],
            icon_height=app["icon"]["height"],
            tagline=escape(app["tagline"]),
            availability=indent(availability, "        "),
        )

    navigation = []
    for key, filename, nav_label in PAGES:
        current = ' aria-current="page"' if key == page else ""
        navigation.append(
            '                <a href="{}"{}>{}</a>'.format(
                filename, current, nav_label
            )
        )

    stylesheets = list(page_settings.get("stylesheets", []))
    if page == "privacy":
        stylesheets.insert(0, "../privacy.css?v=3")

    title = (
        app["name"] + " — Squeaky Systems"
        if page == "overview"
        else app["name"] + " " + label
    )
    return template(
        "app-page.html",
        app_name=app_name,
        title=escape(title),
        description=escape(page_settings["description"], quote=True),
        navigation="\n".join(navigation),
        stylesheets="\n".join(
            '        <link rel="stylesheet" href="{}" />'.format(escape(url, quote=True))
            for url in stylesheets
        ),
        scripts="\n".join(
            '        <script src="{}" defer></script>'.format(escape(url, quote=True))
            for url in page_settings.get("scripts", [])
        ),
        content=indent(template(page + ".html", **values), "            "),
    ) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail if committed HTML needs rebuilding."
    )
    args = parser.parse_args()
    apps = json.loads((ROOT / "_content" / "apps.json").read_text(encoding="utf-8"))
    stale = []
    for app in apps:
        for page, filename, label in PAGES:
            output = ROOT / app["slug"] / filename
            rendered = render_page(app, page, label)
            if output.exists() and output.read_text(encoding="utf-8") == rendered:
                continue
            if args.check:
                stale.append(str(output.relative_to(ROOT)))
            else:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(rendered, encoding="utf-8")
                print("Built " + str(output.relative_to(ROOT)))

    if stale:
        parser.exit(
            1,
            "Pages need rebuilding: " + ", ".join(stale)
            + "\nRun: python3 scripts/build-app-pages.py\n",
        )
    if args.check:
        print("All app pages match their templates and content.")


if __name__ == "__main__":
    main()
