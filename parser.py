import re
from pathlib import Path

DICTIONARY_FILE = Path(__file__).parent / "devils_dictionary.txt"


def parse_devils_dictionary(filepath=DICTIONARY_FILE):
    if not Path(filepath).exists():
        return [], {}

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        file_lines = f.readlines()

    # Find start line (ABASEMENT)
    start_idx = None
    for idx, l in enumerate(file_lines):
        if l.startswith("ABASEMENT,"):
            start_idx = idx
            break

    if start_idx is None:
        return [], {}

    entries = []  # list of dicts: {"letter": str, "lemma": str, "definition": str}
    curr_entry_lines = []
    curr_letter = "A"
    entries_letter = "A"

    i = start_idx
    while i < len(file_lines):
        line = file_lines[i]
        stripped = line.strip()

        if stripped.startswith("*** END OF THE PROJECT GUTENBERG"):
            break

        # Check for standalone single-letter section header on column 0 (e.g. "B", "C")
        if len(line) - len(line.lstrip()) == 0 and len(stripped) == 1 and stripped.isupper() and stripped.isalpha():
            curr_letter = stripped
            i += 1
            continue

        # Column 0 non-empty
        if len(line) - len(line.lstrip()) == 0 and stripped:
            # Check if this line is a new lemma header:
            # Must start with curr_letter (letter tracking rule)
            if stripped[0].upper() == curr_letter and not stripped.startswith("TO MY PET TORTOISE"):
                first_token = re.split(r"[\,\.\s]", stripped)[0]
                if first_token.isupper() and (first_token.isalpha() or "-" in first_token or "." in first_token):
                    if curr_entry_lines:
                        text_str = "".join(curr_entry_lines).rstrip()
                        first_line = curr_entry_lines[0].strip()
                        lemma = first_line.split(",")[0].split(".")[0].strip()
                        entries.append({"letter": entries_letter, "lemma": lemma, "definition": text_str})
                        curr_entry_lines = []

                    entries_letter = curr_letter

        curr_entry_lines.append(line)

        # Check if ZOOLOGY entry is finished
        if entries and entries[-1]["lemma"] == "ZIGZAG" and "sheds its horns every two years." in "".join(curr_entry_lines):
            if i + 1 < len(file_lines) and file_lines[i + 1].strip() == "":
                text_str = "".join(curr_entry_lines).rstrip()
                first_line = curr_entry_lines[0].strip()
                lemma = first_line.split(",")[0].split(".")[0].strip()
                entries.append({"letter": entries_letter, "lemma": lemma, "definition": text_str})
                curr_entry_lines = []
                break

        i += 1

    if curr_entry_lines:
        text_str = "".join(curr_entry_lines).rstrip()
        first_line = curr_entry_lines[0].strip()
        lemma = first_line.split(",")[0].split(".")[0].strip()
        entries.append({"letter": entries_letter, "lemma": lemma, "definition": text_str})

    # Compute letter sequence limits (1-indexed)
    letter_limits = {}
    for idx, entry in enumerate(entries, start=1):
        let = entry["letter"].lower()
        if let not in letter_limits:
            letter_limits[let] = {"letter": let, "min_id": idx, "max_id": idx}
        else:
            letter_limits[let]["max_id"] = idx

    return entries, letter_limits


if __name__ == "__main__":
    entries, limits = parse_devils_dictionary()
    print(f"Parsed {len(entries)} entries across {len(limits)} letters.")
    if entries:
        print("First entry:", entries[0]["lemma"], "->", repr(entries[0]["definition"][:60]))
        print("Last entry:", entries[-1]["lemma"], "->", repr(entries[-1]["definition"][:60]))
    print("Letter 'a' limits:", limits.get("a"))
    print("Letter 'z' limits:", limits.get("z"))
