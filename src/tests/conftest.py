import pytest

from ..managers import MemoryManager


@pytest.fixture(
    scope="class",
    # autouse=True,
)
def memory_manager():
    manager = MemoryManager()
    manager.create()
    return manager
