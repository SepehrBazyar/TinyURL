import re as regex


class URLValidator:
    def __init__(
        self,
        pattern: str = r"^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?$",
    ):
        self.pattern = regex.compile(pattern)

    def is_valid(self, url: str) -> bool:
        return bool(self.pattern.match(url))


url_validator = URLValidator()
