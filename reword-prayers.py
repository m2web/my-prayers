# reword-prayers.py
#
# Reads data/prayerrequests.json, lightly paraphrases each prose prayer entry
# using Google Gemini (gemini-2.5-flash), updates the dateUpdated timestamp,
# and overwrites the file in place.
#
# Usage:
#   python reword-prayers.py
#
# Requirements:
#   pip install -r requirements.txt
#
# Setup:
#   Create a .env file at the repo root with:
#     GOOGLE_API_KEY=your_api_key_here

import json
import os
import re
import shutil
from datetime import datetime, timezone

import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_FILE = os.path.join("data", "prayerrequests.json")
BACKUP_FILE = DATA_FILE + ".bak"
MODEL_NAME = "gemini-2.5-flash"

PARAPHRASE_PROMPT = (
    "You are helping someone refresh their personal prayer journal. "
    "Lightly paraphrase the following prayer so it feels freshly worded while "
    "keeping exactly the same meaning, tone, and approximate length. "
    "Preserve any Scripture references (e.g. 'Colossians 3:23–24', 'Matthew 6:33') "
    "word-for-word and in the same location. "
    "Do not add new ideas, remove existing ones, or change the theological content. "
    "Return only the reworded prayer text — no preamble, no explanation.\n\n"
    "Prayer:\n{prayer}"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def is_name_list(text: str) -> bool:
    """Return True if the request looks like a list of names rather than a prayer.

    Heuristic: if the text contains no sentence-ending punctuation (.!?) it is
    treated as a list of names and left unchanged.
    """
    return not re.search(r"[.!?]", text)


def reword_prayer(model, prayer_text: str) -> str:
    """Send a prayer to Gemini and return the paraphrased version."""
    prompt = PARAPHRASE_PROMPT.format(prayer=prayer_text)
    response = model.generate_content(prompt)
    return response.text.strip()


def today_iso() -> str:
    """Return the current UTC datetime as an ISO 8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    # Load API key from .env
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found. Create a .env file with your key.")
        raise SystemExit(1)

    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)

    # Load the JSON data
    if not os.path.exists(DATA_FILE):
        print(f"ERROR: {DATA_FILE} not found.")
        raise SystemExit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        entries = json.load(f)

    # Create a backup before making any changes
    shutil.copy2(DATA_FILE, BACKUP_FILE)
    print(f"Backup created: {BACKUP_FILE}")

    updated_entries = []

    try:
        for entry in entries:
            category = entry.get("category", "Unknown")
            prayer_text = entry.get("request", "")

            if is_name_list(prayer_text):
                print(f"  [{category}] Skipped (name list — left unchanged)")
                updated_entries.append(entry)
                continue

            print(f"  [{category}] Paraphrasing...", end=" ", flush=True)
            new_text = reword_prayer(model, prayer_text)
            entry["request"] = new_text
            entry["dateUpdated"] = today_iso()
            print("done.")
            updated_entries.append(entry)

    except Exception as exc:
        print(f"\nERROR during processing: {exc}")
        print(f"The original file is safe at: {BACKUP_FILE}")
        raise SystemExit(1)

    # Write the updated JSON back to the data file
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_entries, f, ensure_ascii=False, indent=2)

    # Remove the backup on success
    os.remove(BACKUP_FILE)
    print(f"\nSuccess! {DATA_FILE} has been updated.")
    print("Backup removed.")


if __name__ == "__main__":
    main()
