import json
import os

# List of words to add
WORDS = [
    "Pelle", "Soiste", "Charissa", "Napoles", "Samri", "Wenye", "Jereon", "Hailey", "Kaylyn", "Guage",
    "Sophya", "Carlee", "Rayder", "Kearsten", "Alyse", "Remi", "Bular", "IOUS", "Clermont", "Vanoy",
    "Austina", "Beshear", "Pashtun"
]

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '..', '.vscode', 'settings.json')

# Load existing settings or create new
def load_settings(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}

# Save settings back to file
def save_settings(path, settings):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)

# Add words to cSpell.words
def add_words(settings, words):
    existing = set(settings.get("cSpell.words", []))
    updated = existing.union(words)
    settings["cSpell.words"] = sorted(updated)
    return settings

if __name__ == "__main__":
    settings = load_settings(SETTINGS_PATH)
    settings = add_words(settings, WORDS)
    save_settings(SETTINGS_PATH, settings)
    print(f"Added {len(WORDS)} words to .vscode/settings.json")
