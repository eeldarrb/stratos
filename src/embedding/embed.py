import os
import pytesseract
from PIL import Image
from pathlib import Path
from .providers import ollama
from ..database.vector_store import VectorStore, Item
from ..llm import llm_actions

IMAGE_TYPE = [".png", ".jpg", ".jpeg"]


def create_item_from_file(file_path) -> Item:
    path = Path(file_path)
    file_name = path.name
    ext = path.suffix.lower()
    text = ""

    try:
        if ext == ".pdf":
            text = pytesseract.image_to_string(Image.open(file_path))

        elif ext in IMAGE_TYPE:
            text = llm_actions.analyze_image(file_path)

        else:
            file = open(file_path, "r")
            text = file.read()
    except Exception as e:
        print(f"Error while prepraring item: {e}")
        text = ""

    return Item(text, file_path, ext, source=file_name)


def process_file(file_path):
    vector_store = VectorStore(ollama.embeddings)
    items: list[Item] = []

    if os.path.isdir(file_path):
        for root, _, subfiles in os.walk(file_path):
            for subfile in subfiles:
                if not subfile.startswith("."):
                    subfile_path = os.path.join(root, subfile)
                    items.append(create_item_from_file(subfile_path))
    else:
        items.append(create_item_from_file(file_path))

    vector_store.add_items(items)
