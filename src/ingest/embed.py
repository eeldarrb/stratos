import os
import config
from pathlib import Path
from ..vector_store.vector_store import VectorStore
from .extractor import extract_text
from src.types.file_record import FileRecord


def process_file(file_path):
    vector_store = VectorStore(config.EMBEDDING_MODEL, config.DATABASE_URI)
    items: list[FileRecord] = []

    if os.path.isdir(file_path):
        for root, _, subfiles in os.walk(file_path):
            for subfile in subfiles:
                if not subfile.startswith("."):
                    subfile_path = os.path.join(root, subfile)
                    items.append(create_item(subfile_path))
    else:
        items.append(create_item(file_path))

    vector_store.add(items)


def create_item(file_path) -> FileRecord:
    text = extract_text(file_path)
    path = Path(file_path)
    ext = path.suffix.lower()
    filename = path.name

    return FileRecord(text, file_path, ext, source=filename)
