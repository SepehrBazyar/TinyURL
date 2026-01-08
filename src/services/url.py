import random
import string

from ..exceptions import (
    DuplicateDataError,
    ShortCodeLeak,
    URLError,
)
from ..managers import (
    BaseManager,
    memory_manager,
)
from ..utils import (
    URLValidator,
    url_validator,
)


class URLShortener:
    def __init__(
        self,
        manager: BaseManager,
        validator: URLValidator,
        short_length: int = 5,
    ):
        self.manager = manager
        self.validator = validator
        self.short_length = short_length

    def shorten(self, url: str) -> str:
        if not self.validator.is_valid(url):
            raise URLError("Invalid URL")

        for _ in range(5):
            short_code = self._generate_short_code(short_length=self.short_length)
            try:
                self.manager.write(url, short_code)
            except DuplicateDataError:
                continue

            break
        else:
            raise ShortCodeLeak("End of Data")

        return "http://127.0.0.1:8000/" + short_code

    def get_original(self, short_code: str) -> str:
        return self.manager.read(short_code)

    def _generate_short_code(self, short_length: int) -> str:
        base = string.ascii_letters + string.digits
        return "".join(random.choices(base, k=short_length))


url_shortener_service = URLShortener(
    manager=memory_manager,
    validator=url_validator,
    short_length=4,
)
