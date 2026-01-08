import logging

from .base import BaseManager
from ..exceptions import (
    DuplicateDataError,
    NotExistError,
)

logger = logging.getLogger(__name__)


class MemoryManager(BaseManager):
    def __init__(self):
        self.__storage = None

    def create(self):
        if self.__storage is None:
            self.__storage = {}

    def write(self, url, short_code):
        if short_code in self.__storage.keys():
            raise DuplicateDataError("Duplicate Short Code")

        self.__storage[short_code] = url

    def read(self, short_code):
        try:
            result = self.__storage[short_code]
        except KeyError as e:
            logger.exception(e)
            raise NotExistError("No Value") from e

        return result


memory_manager = MemoryManager()
memory_manager.create()
