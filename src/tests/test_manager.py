from ..managers import MemoryManager


class TestMemoryManager:
    def test_is_empty_storage(
        self,
        memory_manager: MemoryManager,
    ):
        assert len(memory_manager) == 0


class TestDataBaseManager:
    pass
