# Project Overview: Mark's Private Prayer Site

## Purpose

A **personal daily prayer site** used by Mark for private devotions. It is not a public-facing product — it is a private spiritual tool. All content in data files, shortcodes, and prayers is real and personal.

## Technology Stack

| Layer | Technology |
| --- | --- |
| Static Site Generator | [Hugo](https://gohugo.io/) v0.121.1 (extended) |
| Theme | [hugo-theme-jane](https://github.com/xianmin/hugo-theme-jane) (installed as a git submodule in `themes/`) |
| Hosting | [Cloudflare Pages](https://pages.cloudflare.com/) |
| CI/CD | GitHub Actions (`.github/workflows/`) |
| Custom CSS | `static/m2css.css` (referenced in `config.toml` → `Params.customCSS`) |
| AI Integration | Google Gemini (`gemini-2.5-flash`) via Python |
| Python Dependencies | See `requirements.txt`; key packages: `google-generativeai`, `python-dotenv` |

## Site Configuration

- **`config.toml`** — Main Hugo config. Base URL: `https://todaysprivateprayer.github.io`. Theme: `hugo-theme-jane`.
- **`staticwebapp.config.json`** — Azure Static Web App routing rules (legacy, currently hosted on Cloudflare Pages).

## Directory Structure

```text
my-prayers/
├── .agent/               ← AI assistant context files (this folder)
├── .github/workflows/    ← GitHub Actions CI/CD
├── archetypes/           ← Hugo content templates
├── assets/               ← Hugo asset pipeline files
├── content/              ← Hugo markdown content pages
├── data/                 ← JSON data files consumed by shortcodes
├── layouts/
│   ├── shortcodes/       ← Custom Hugo shortcodes (HTML templates)
│   ├── partials/         ← Hugo partial templates
│   └── _default/         ← Default layout overrides
├── static/               ← Static assets (CSS, images)
├── themes/hugo-theme-jane/ ← Hugo theme (git submodule)
├── reword-prayers.py     ← AI prayer paraphrase script
├── staff-csv-to-json.py  ← Converts staff CSV → data/staff.json
├── staff-json-to-csv.py  ← Converts data/staff.json → CSV
├── email-list-to-specialprayer.py ← Converts email list → data/specialprayer.json
├── new-staff.csv         ← Staff source data (CSV)
├── requirements.txt      ← Python dependencies
└── .env                  ← Local secrets (NOT committed; contains API keys)
```

## Key Concepts

- **Data-driven site**: The site is powered by JSON files in `data/`. Hugo shortcodes read these files and render them on the page. No CMS is used.
- **Shortcodes drive content**: All dynamic prayer content on the page is injected via Hugo shortcodes embedded in Markdown content files under `content/`.
- **Python scripts are maintenance tools**: They are run locally (not in CI) to update data files. After running them, the updated JSON files are committed and pushed, which triggers a Cloudflare Pages deploy.
- **Private content**: Personal names, prayer requests, and staff data are real. Treat them with discretion.

## Environment Variables

The `.env` file at repo root holds local secrets. It is gitignored. See `.agent/python-scripts.md` for details.
