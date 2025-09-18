from dataclasses import dataclass


@dataclass()
class Item:
    text: str
    file_path: str
    mimetype: str
    source: str
