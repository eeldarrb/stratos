from dataclasses import dataclass


@dataclass()
class FileRecord:
    text: str
    file_path: str
    mimetype: str
    source: str
