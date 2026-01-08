import random
import string

from ..exceptions import URLError
from ..utils import url_validator


class URLShortener:
    def __init__(
        self,
        short_length: int = 5,
    ):
        self.short_length = short_length

    def shorten(self, url: str) -> str:
        if not url_validator.is_valid(url):
            raise URLError("Invalid URL")

        short_code = self._generate_short_code(short_length=self.short_length)
        return "http://127.0.0.1:8000/" + short_code

    def get_original(self, short_code: str) -> str:
        pass

    def _generate_short_code(self, short_length: int) -> str:
        base = string.ascii_letters + string.digits
        return "".join(random.choices(base, k=short_length))


url_shortener_service = URLShortener(
    short_length=4,
)
