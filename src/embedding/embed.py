import os
from pathlib import Path
from .providers import ollama
from ..database.vector_store import VectorStore
from .extractor import extract_text
from .item import Item


def process_file(file_path):
    vector_store = VectorStore(ollama.embeddings)
    items: list[Item] = []

    if os.path.isdir(file_path):
        for root, _, subfiles in os.walk(file_path):
            for subfile in subfiles:
                if not subfile.startswith("."):
                    subfile_path = os.path.join(root, subfile)
                    items.append(create_item(subfile_path))
    else:
        items.append(create_item(file_path))

    vector_store.add_items(items)


def create_item(file_path) -> Item:
    text = extract_text(file_path)
    path = Path(file_path)
    ext = path.suffix.lower()
    filename = path.name

    return Item(text, file_path, ext, source=filename)
