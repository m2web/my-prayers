

# Import required modules
import sys  # For command-line arguments
import os   # For file path operations
import re   # For regular expressions
import json # For working with JSON files
from email import policy  # For parsing email files
from email.parser import BytesParser  # For parsing .eml files

# Usage: python email-list-to-specialprayer.py path/to/email.eml

# This function extracts the bulleted prayer prompts that appear after 'Prayer Prompts:' in the email body.
def extract_prayer_prompts(text):
    # Search for the 'Prayer Prompts:' section in the email text
    match = re.search(r'Prayer Prompts:([\s\S]+)', text, re.IGNORECASE)
    if not match:
        return []  # Return empty list if not found
    prompts_section = match.group(1)
    lines = prompts_section.splitlines()  # Split the section into lines
    prayers = []
    in_bullets = False  # Track if we are inside the bulleted list
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if not line:
            if in_bullets:
                break  # Stop at first blank line after bullets start
            continue  # Skip blank lines before bullets
        # If the line starts with a bullet (*, -, or •), it's a new prayer prompt
        if re.match(r'^[-*•]\s+', line):
            in_bullets = True
            line = re.sub(r'^[-*•]\s+', '', line)  # Remove the bullet
            prayers.append({"prayer": line})
        elif in_bullets:
            # If we're in bullets and the line doesn't start with a bullet, it's a continuation of the previous bullet (wrapped line)
            if prayers:
                prayers[-1]["prayer"] += ' ' + line
        elif in_bullets:
            break  # Stop if non-bullet after bullets started
    return prayers


# Main script logic
if __name__ == "__main__":
    # Check if the user provided a .eml file path as an argument
    if len(sys.argv) < 2:
        print("Usage: python email-list-to-specialprayer.py path/to/email.eml")
        sys.exit(1)
    eml_path = sys.argv[1]

    # Open and parse the .eml file using the email library
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # Get the email body (prefer plain text if available)
    if msg.is_multipart():
        # If the email has multiple parts, look for the plain text part
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_content()
                break
        else:
            # If no plain text part, get the first available part
            body = msg.get_body(preferencelist=('plain', 'html')).get_content()
    else:
        # If the email is not multipart, just get the content
        body = msg.get_content()

    # Extract the prayer prompts from the email body
    prayers = extract_prayer_prompts(body)

    # Write the extracted prayers to specialprayer.json in JSON format
    with open('specialprayer.json', 'w', encoding='utf-8') as f:
        json.dump(prayers, f, ensure_ascii=False, indent=2)

    # Print a summary for the user
    print(f"Extracted {len(prayers)} prayers from {os.path.basename(eml_path)} to specialprayer.json")
