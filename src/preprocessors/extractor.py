import pymupdf
from pathlib import Path
from ..llm import llm_actions

IMAGE_TYPE = [".png", ".jpg", ".jpeg"]


def extract_text(file_path) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    try:
        if ext == ".pdf":
            text = ""
            doc = pymupdf.open(file_path)
            for page in doc:
                text += page.get_text()
            return text

        elif ext in IMAGE_TYPE:
            return llm_actions.analyze_image(file_path)

        else:
            file = open(file_path, "r")
            return file.read()
    except Exception:
        raise Exception("Error extracting text")
