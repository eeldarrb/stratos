import pytesseract
from PIL import Image
from pathlib import Path
from ..llm import llm_actions

IMAGE_TYPE = [".png", ".jpg", ".jpeg"]


def extract_text(file_path) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    try:
        if ext == ".pdf":
            return pytesseract.image_to_string(Image.open(file_path))

        elif ext in IMAGE_TYPE:
            return llm_actions.analyze_image(file_path)

        else:
            file = open(file_path, "r")
            return file.read()
    except Exception as e:
        print(f"Error while prepraring item: {e}")
        return ""
