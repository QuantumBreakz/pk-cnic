# pk-cnic

Validate, normalise and read **Pakistani CNIC numbers** (`12345-1234567-1`). Pure Python, no dependencies, typed.

- Accepts the number with or without hyphens and stores one canonical form.
- Converts Urdu (Extended Arabic-Indic) and Arabic-Indic digits, as produced by OCR or Urdu keyboards.
- Reads the region from the first digit and the gender from the last (odd male, even female).

**A CNIC has no check digit.** Format validation catches badly formed input; it can't tell you the number is real or belongs to the person. Verify identity against NADRA's records.

## Install

```bash
pip install pk-cnic
```

## Usage

```python
from pk_cnic import is_valid, normalize, parse

parse("35202-1234567-1")
# Cnic(number='35202-1234567-1', locality_code='35202', region='Punjab', gender='male')

normalize("3520212345671")      # '35202-1234567-1'
normalize("۳۵۲۰۲-۱۲۳۴۵۶۷-۸")    # '35202-1234567-8'
is_valid("35202-12345671")      # False: hyphens must be all or none
```

`parse` and `normalize` raise `ValueError` for anything that isn't a 13-digit CNIC number.

### Command line

```bash
pk-cnic 35202-1234567-1 42101-7654321-2
```

Numbers can also be piped on stdin. Exit code is `0` when all are valid and `1` otherwise.

## What the digits mean

| Part          | Digits | Meaning                                             |
| ------------- | ------ | --------------------------------------------------- |
| Locality code | 1–5    | First digit is the region; the rest narrow it down |
| Serial        | 6–12   | Sequence number                                     |
| Last digit    | 13     | Odd: male. Even: female                             |

Region by first digit, as commonly documented: 1 Khyber Pakhtunkhwa, 2 FATA (now part of Khyber Pakhtunkhwa), 3 Punjab, 4 Sindh, 5 Balochistan, 6 Islamabad, 7 Gilgit-Baltistan. Use the region and gender digits for consistency checks, not as the source of truth.

## Background

Why there's no check digit, what to do about it, and where CNIC checks fit in onboarding: [Validating a Pakistani CNIC number](https://aliahmed.si/blog/pakistan-cnic-number-validation/). For the wider verification flow: [How KYC identity verification works](https://aliahmed.si/blog/how-kyc-identity-verification-works/).

## License

MIT
