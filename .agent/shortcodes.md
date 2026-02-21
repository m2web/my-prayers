# Hugo Shortcodes Reference

All shortcodes live in `layouts/shortcodes/`. They are called from Markdown content files in `content/` using `{{< shortcode-name >}}`.

## Content Shortcodes

| Shortcode File | Purpose | Data Source |
| --- | --- | --- |
| `prayer-requests.html` | Displays daily categorized prayer requests | `data/prayerrequests.json` |
| `special-prayer-requests.html` | Displays special/targeted prayer requests | `data/specialprayer.json` |
| `requests.html` | Displays prayer requests by day of week from `data/requests/` directory | `data/requests/` |
| `todays-staff.html` | Shows one staff member per day with mailto link | `data/staff.json` |
| `todays-verse.html` | Shows today's ESV Bible verse | `data/esvVerses.json` |
| `todays-wsc.html` | Shows today's Westminster Shorter Catechism Q/A | `data/wsc.json` |
| `todays-country.html` | Shows today's mission country with PrayerCast link | `data/countries.json` |
| `todays-psalm.html` | Displays a random psalm for today via the ESV API | ESV API (external) |
| `todays-vov.html` | Links to today's Valley of Vision prayer | External link |
| `memory-verse.html` | Shows the current month's memory verse; shows full year review in last 4 days of month | `data/memoryverses.json` |
| `mission-link.html` | Displays the weekly mission link | `data/missionlink.json` |

## Utility Shortcodes

| Shortcode File | Purpose |
| --- | --- |
| `the-date.html` | Displays the current date |
| `category-menu.html` | Dropdown menu to filter prayer by category |
| `prayer-timer.html` | A prayer timer widget |
| `todosmaillink.html` | Generates a mailto link to email TODOs |

## Day-Cycling Logic

Several shortcodes (staff, verse, WSC, country, psalm) cycle through their data arrays based on the **day of the year** or **day of the month**, so a different item appears each day without any backend or database. The cycling is done in the Go template using modular arithmetic on `.Now`.

## Adding a New Shortcode

1. Create `layouts/shortcodes/my-shortcode.html`
2. Use Hugo's `.Site.Data.<filename>` to access data files
3. Embed in a content Markdown file with `{{< my-shortcode >}}`
4. Run `hugo server` locally to verify output
