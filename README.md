# Squeaky Systems website

The site is served as static HTML by GitHub Pages. Open `index.html` directly or
run `python3 -m http.server 8000` to preview it locally.

## Reusable app pages

Pernolay and Gonglitea use the same templates for their overview, support, and
privacy pages. The shared design comes from Pernolay: the header and navigation,
icon and introduction layout, content column, and footer.

- `_templates/` contains the shared page shell, overview, App Store badge,
  support, and privacy templates.
- `_content/apps.json` contains app names, icons, taglines, release status or
  App Store URLs, page descriptions, and optional page stylesheets and scripts.
- `_content/<app>/overview.html`, `support.html`, and `privacy.html` contain the
  app-specific content. Use `app-features`, `app-feature-card`,
  `app-feature-image`, `app-feature-copy`, and `app-principles` for feature cards.
  Use `policy-section` for groups of privacy content.
- `apps.css`, `privacy.css`, and `site.js` provide shared styles and behavior.
  Additional content such as Gonglitea’s watch gallery and steep explorer stays
  in that app’s content and assets.

After editing the templates or content, regenerate all six pages:

```sh
python3 scripts/build-app-pages.py
python3 scripts/build-app-pages.py --check
```

Commit the generated `<app>/index.html`, `support.html`, and `privacy-policy.html`
alongside their sources. They remain complete HTML pages and work without a
client-side template loader. Python 3 is needed only to regenerate them; there
are no extra dependencies. CI checks that the committed pages match the sources.

To add another app, add an entry to `_content/apps.json`, create its three content
fragments under `_content/<slug>/`, put its assets in `<slug>/`, and run the build
command. Set `app_store_url` for a released app, or `release_status` for an
unreleased one. Add its link to the homepage as needed.

When changing shared CSS or JavaScript, update the corresponding cache version
in `_templates/app-page.html` (or `scripts/build-app-pages.py` for privacy CSS)
before rebuilding. Page-specific asset versions live in `_content/apps.json`.
