import config
from src.file_service import FileService
from src.listener_service import start_listener
from src.file_store.vector_store import VectorStore


def main():
    vector_store = VectorStore(config.EMBEDDING_MODEL, config.DATABASE_URI)
    file_service = FileService(vector_store)
    start_listener(file_service, config.PATHS_TO_WATCH)


if __name__ == "__main__":
    main()
