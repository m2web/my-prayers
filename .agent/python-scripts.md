# Python Scripts

These scripts are **run locally** (not in CI). After running them, commit and push the updated JSON files to trigger a Cloudflare Pages deploy.

## Environment Setup

All scripts require a `.env` file at the repo root. This file is gitignored and must be created manually.

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Install dependencies once:

```powershell
pip install -r requirements.txt
```

---

## `reword-prayers.py`

**Purpose**: Lightly paraphrases each prose prayer in `data/prayerrequests.json` using Google Gemini (`gemini-2.5-flash`) to keep the wording fresh. Updates `dateUpdated` timestamps.

**Run**:

```powershell
python reword-prayers.py
```

**Behavior**:

- Creates a `.bak` backup of `prayerrequests.json` before making changes.
- Skips entries where `request` has no sentence-ending punctuation (`.!?`) — these are name lists.
- Preserves Scripture references verbatim.
- If any error occurs mid-run, the original file is left safe at the backup path.
- On success, removes the backup and overwrites `prayerrequests.json`.

**Key constants** (edit at top of file):

- `MODEL_NAME` — Gemini model to use (default: `gemini-2.5-flash`)
- `PARAPHRASE_PROMPT` — The prompt template sent to Gemini
- `DATA_FILE` — Path to the JSON file (default: `data/prayerrequests.json`)

---

## `staff-csv-to-json.py`

**Purpose**: Converts `new-staff.csv` into `data/staff.json`.

**Run**:

```powershell
python staff-csv-to-json.py
```

Use this whenever the staff list in `new-staff.csv` or `new-staff.xlsx` changes.

---

## `staff-json-to-csv.py`

**Purpose**: Converts `data/staff.json` back to a CSV. Useful for exporting the current staff list for editing in Excel.

**Run**:

```powershell
python staff-json-to-csv.py
```

---

## `email-list-to-specialprayer.py`

**Purpose**: Takes an email-style list of names/info and converts it into `data/specialprayer.json` for use with the `special-prayer-requests.html` shortcode.

**Run**:

```powershell
python email-list-to-specialprayer.py
```

---

## Typical Workflow for Prayer Data Updates

1. Edit `data/prayerrequests.json` directly to add/change prayer text, **or** run `reword-prayers.py` to AI-refresh existing prayers.
2. Commit the updated JSON.
3. Push to `main` → Cloudflare Pages auto-deploys.
