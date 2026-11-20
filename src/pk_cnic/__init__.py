"""Validate, normalise and read Pakistani CNIC numbers (12345-1234567-1).

Format checks only: a CNIC has no check digit, so a well-formed number can still be
wrong or belong to someone else. Verify identity against NADRA's records.
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import NamedTuple, Sequence

__all__ = ["Cnic", "parse", "is_valid", "normalize", "REGIONS", "main"]
__version__ = "0.1.0"

# First digit by region, as commonly documented. A hint for consistency checks, not a source of truth.
REGIONS = {
    "1": "Khyber Pakhtunkhwa",
    "2": "FATA (now part of Khyber Pakhtunkhwa)",
    "3": "Punjab",
    "4": "Sindh",
    "5": "Balochistan",
    "6": "Islamabad",
    "7": "Gilgit-Baltistan",
}

# Extended Arabic-Indic (Urdu) and Arabic-Indic digits, as produced by OCR or Urdu keyboards.
_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
_SHAPE = re.compile(r"[0-9]{5}-?[0-9]{7}-?[0-9]")


class Cnic(NamedTuple):
    number: str  # canonical form: 12345-1234567-1
    locality_code: str
    region: str
    gender: str  # from the last digit: odd male, even female

    @property
    def digits(self) -> str:
        return self.number.replace("-", "")


def normalize(raw: str) -> str:
    """Return the canonical hyphenated form. Raises ValueError if the input isn't a CNIC number."""
    text = raw.strip().translate(_DIGITS)
    if not _SHAPE.fullmatch(text) or text.count("-") not in (0, 2):
        raise ValueError(f"not a CNIC number: {raw!r}")
    d = text.replace("-", "")
    return f"{d[:5]}-{d[5:12]}-{d[12]}"


def parse(raw: str) -> Cnic:
    """Validate the format of a CNIC number and read what its digits encode."""
    number = normalize(raw)
    d = number.replace("-", "")
    return Cnic(
        number=number,
        locality_code=d[:5],
        region=REGIONS.get(d[0], "unknown"),
        gender="male" if int(d[12]) % 2 else "female",
    )


def is_valid(raw: str) -> bool:
    """True if the input is a well-formed CNIC number (13 digits, hyphens all or none)."""
    try:
        normalize(raw)
    except ValueError:
        return False
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pk-cnic", description="Validate and read Pakistani CNIC numbers.")
    parser.add_argument("numbers", nargs="*", help="CNIC numbers; read from stdin if omitted")
    args = parser.parse_args(argv)
    numbers = args.numbers or [line for line in sys.stdin.read().splitlines() if line.strip()]
    status = 0
    for raw in numbers:
        try:
            c = parse(raw)
        except ValueError as exc:
            print(f"invalid  {exc}")
            status = 1
            continue
        print(f"ok       {c.number}  region={c.region}  gender={c.gender}")
    return status


if __name__ == "__main__":
    sys.exit(main())
