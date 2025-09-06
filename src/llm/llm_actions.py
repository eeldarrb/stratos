import config
from ollama import chat


def analyze_image(file_path) -> str:
    desc = ""
    try:
        res = chat(
            model=config.IMAGE_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Describe the contents of the image. Do not include any preamble.",
                    "images": [file_path],
                }
            ],
        )
        desc = res.message.content or ""
    except Exception:
        print("Error analyzing image:", file_path)
    return desc
