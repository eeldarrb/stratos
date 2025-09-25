from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    return chunks
