
import sys
import os
import re
import json
from email import policy
from email.parser import BytesParser

# Usage: python email-list-to-specialprayer.py path/to/email.eml


def extract_prayer_prompts(text):
    # Find the 'Prayer Prompts:' section
    match = re.search(r'Prayer Prompts:([\s\S]+)', text, re.IGNORECASE)
    if not match:
        return []
    prompts_section = match.group(1)
    lines = prompts_section.splitlines()
    prayers = []
    in_bullets = False
    for line in lines:
        line = line.strip()
        if not line:
            if in_bullets:
                break  # Stop at first blank line after bullets start
            continue
        if re.match(r'^[-*•]\s+', line):
            in_bullets = True
            line = re.sub(r'^[-*•]\s+', '', line)
            prayers.append({"prayer": line})
        elif in_bullets:
            # Handle wrapped lines (continuation of previous bullet)
            if prayers:
                prayers[-1]["prayer"] += ' ' + line
        elif in_bullets:
            break  # Stop if non-bullet after bullets started
    return prayers

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python email-list-to-specialprayer.py path/to/email.eml")
        sys.exit(1)
    eml_path = sys.argv[1]
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    # Get the email body (prefer plain text)
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_content()
                break
        else:
            body = msg.get_body(preferencelist=('plain', 'html')).get_content()
    else:
        body = msg.get_content()
    prayers = extract_prayer_prompts(body)
    with open('specialprayer.json', 'w', encoding='utf-8') as f:
        json.dump(prayers, f, ensure_ascii=False, indent=2)
    print(f"Extracted {len(prayers)} prayers from {os.path.basename(eml_path)} to specialprayer.json")
