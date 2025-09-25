from abc import ABC, abstractmethod
from src.types.file_record import FileRecord


class FileStore(ABC):
    @abstractmethod
    def add(self, files: list[FileRecord]):
        pass

    @abstractmethod
    def update(self, file_path: str, new_file: FileRecord):
        pass

    @abstractmethod
    def delete_by_path(self, file_path: str):
        pass

    @abstractmethod
    def move(self, old_path: str, new_path: str):
        pass

    @abstractmethod
    def query(self, query: str, k: int = 10) -> list[tuple[FileRecord, float]]:
        pass
