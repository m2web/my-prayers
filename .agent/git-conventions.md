# Git Conventions

## Commit Message Format

Based on `.gitmessage.txt` at the repo root.

```
{emoji} Commit Title

Short summary of the change (imperative mood)

Details (if needed):
- What/why/how
- Any references or issues
```

### Emoji Guide

| Emoji | Code | Use for |
|---|---|---|
| ⚡ | `:zap:` | Performance improvement |
| 🔥 | `:fire:` | Removing code or files |
| ✏️ | `:pencil2:` | Content/text update (prayers, data files) |
| 🐛 | `:bug:` | Bug fix |
| ✨ | `:sparkles:` | New feature or shortcode |
| 🎨 | `:art:` | Formatting, style, CSS |

### Example Commit Messages

```
✏️ Update prayerrequests.json with AI-refreshed prayers

Ran reword-prayers.py to paraphrase all prose prayer entries.
Name-list entries left unchanged.
```

```
✨ Add todays-psalm shortcode

New shortcode cycles through psalms by day of month.
Embedded in content/prayer.md.
```

```
🐛 Fix staff cycling bug in todays-staff.html

Off-by-one error caused wrong staff to display on day 1.
```

## Branch Strategy

- **`main`** — the only branch; all work goes here directly.
- Cloudflare Pages deploys automatically on push to `main`.

## Files NOT to Commit

(Handled by `.gitignore`)

- `.env` — API keys
- `__pycache__/`, `*.pyc` — Python bytecode
- `public/`, `resources/` — Hugo build output
- `node_modules/`, `package.json`, `package-lock.json`
- `assets/*.eml` — Email files
- `.markdownlint.json`

## Commit Signing / Settings

Git commit template is configured via `.gitmessage.txt`. To activate it locally:

```powershell
git config commit.template .gitmessage.txt
```

Always include the emoji in the beginning of the commit message.

## AI-Assisted Changes

The commit message MUST begin with an appropriate GitHub emoji.

Do not push changes to the remote repository until I see the changes and approve the push.
