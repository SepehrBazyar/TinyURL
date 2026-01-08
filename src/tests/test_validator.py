from ..utils import url_validator


def test_url_valid():
    assert url_validator.is_valid("https://google.com")


def test_url_invalid():
    assert not url_validator.is_valid("incorrect")
