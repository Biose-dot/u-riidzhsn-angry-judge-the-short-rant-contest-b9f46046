#!/usr/bin/env python3
"""Writes the competition entry text to entry.txt.

Entry: a short rant for the angry-judge short-rant contest, aimed at
the office printer. The rant builds its anger in three escalating
beats. First, the diagnosis: the printer has exactly one personality
trait, spite. Second, the evidence: it prints fine all week, then
jams the one page you actually need, flashes an error in a language
you do not speak, and demands a cartridge that costs more than the
printer itself. Third, the humiliation: you have apologized to a
machine, you have begged a machine, and the machine has never once
apologized back. The structure is what makes it a good rant rather
than a complaint -- each sentence raises the stakes, the repetition
of "I have ... a machine" drums the absurdity in, and the final line
lands the reversal: the human is the one grovelling.

The runner takes MAKEFUN_OUTPUT_DIR (default /output), creates it if
needed, and writes the entry there as entry.txt (UTF-8, no trailing
newline). The entry text is stored in the ENTRY constant below and is
written byte-for-byte, exactly as written; nothing in this script
rewords, wraps, strips or otherwise transforms it.

Validation rules enforced before writing:
- ENTRY must not be blank.
- ENTRY must stay within the competition length budget (this rant is
  321 characters, inside the short-rant limit).
- ENTRY must keep its paragraph structure: the text is one paragraph
  with no line breaks, so embedded newlines are rejected.
"""
import os

ENTRY = "Our office printer has exactly one personality trait: spite. It prints fine all week, then jams the one page I need, flashes an error in a language I don't speak, and demands a cartridge that costs more than the printer. I have apologized to a machine. I have begged a machine. The machine has never once apologized back."

OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"

# Competition length budget for a short rant entry (characters).
MAX_ENTRY_LENGTH = 500


def normalize_text(text):
    """Return text with surrounding whitespace removed.

    The entry itself is already exact; this helper only guards against
    accidental leading or trailing whitespace creeping in during edits.
    It never touches the interior of the text.
    """
    return text.strip()


def validate_entry(text):
    """Check the entry against the competition rules; raise on failure.

    Rules: the entry must not be blank, must contain no embedded
    newlines (it is a single paragraph), and must fit within
    MAX_ENTRY_LENGTH characters.
    """
    if not text or not text.strip():
        raise ValueError("ENTRY must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("ENTRY must be a single paragraph")
    if len(text) > MAX_ENTRY_LENGTH:
        raise ValueError(
            "ENTRY is %d characters, over the %d-character limit"
            % (len(text), MAX_ENTRY_LENGTH)
        )
    return text


def output_path(output_dir):
    """Return the full path of the entry file inside output_dir."""
    return os.path.join(output_dir, OUTPUT_FILENAME)


def resolve_output_dir(output_dir=None):
    """Pick the output directory: explicit arg, env var, or default."""
    return output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)


def verify_written(path, expected_text):
    """Re-read the written file and confirm it matches the entry exactly.

    A write that silently truncates or re-encodes the text would make
    the submission wrong, so the runner checks the bytes on disk
    against the entry it intended to write.
    """
    with open(path, "r", encoding="utf-8") as f:
        actual = f.read()
    if actual != expected_text:
        raise ValueError(
            "entry.txt does not match ENTRY (%d bytes on disk, %d expected)"
            % (len(actual), len(expected_text))
        )
    return True


def write_entry(output_dir=None):
    """Write ENTRY to entry.txt in output_dir; return the file path."""
    text = validate_entry(normalize_text(ENTRY))
    output_dir = resolve_output_dir(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    path = output_path(output_dir)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Confirm the file on disk is byte-for-byte the intended entry.
    verify_written(path, text)
    return path


def main():
    write_entry()


if __name__ == "__main__":
    main()
