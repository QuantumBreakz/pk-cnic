import pytest

from pk_cnic import Cnic, is_valid, main, normalize, parse


def test_parse_hyphenated():
    assert parse("35202-1234567-1") == Cnic("35202-1234567-1", "35202", "Punjab", "male")


def test_parse_digits_only_normalizes():
    c = parse("3520212345671")
    assert c.number == "35202-1234567-1"
    assert c.digits == "3520212345671"


def test_gender_digit():
    assert parse("42101-7654321-2").gender == "female"
    assert parse("42101-7654321-2").region == "Sindh"


def test_urdu_digits():
    assert normalize("۳۵۲۰۲-۱۲۳۴۵۶۷-۸") == "35202-1234567-8"
    assert parse("٣٥٢٠٢١٢٣٤٥٦٧١").number == "35202-1234567-1"


def test_unknown_region():
    assert parse("91234-1234567-1").region == "unknown"


@pytest.mark.parametrize(
    "bad",
    ["35202-1234567", "35202-12345671", "3520-21234567-1", "35202 1234567 1", "35202-1234567-1-", "", "abcde-fghijkl-m", "3520212345671x"],
)
def test_invalid(bad):
    assert not is_valid(bad)
    with pytest.raises(ValueError):
        parse(bad)


def test_whitespace_is_trimmed():
    assert is_valid("  35202-1234567-1\n")


def test_cli(capsys):
    assert main(["35202-1234567-1"]) == 0
    assert "region=Punjab" in capsys.readouterr().out
    assert main(["35202-1234567"]) == 1
