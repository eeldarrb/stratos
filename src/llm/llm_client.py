import config
from ollama import chat


def analyze_image(file_path):
    try:
        res = chat(
            model=config.IMAGE_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "what is in this picture?",
                    "images": [file_path],
                }
            ],
        )
        desc = res.message.content
        return desc
    except Exception:
        print("Error analyzing image:", file_path)
