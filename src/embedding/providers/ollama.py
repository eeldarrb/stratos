import config
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model=config.EMBEDDING_MODEL,
)
