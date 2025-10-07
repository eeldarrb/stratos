import os
import config
import typer
from src.file_service import FileService
from src.listener_service import start_listener
from src.file_store.vector_store import VectorStore


app = typer.Typer()
vector_store = VectorStore(config.EMBEDDING_MODEL, config.DATABASE_URI)
file_service = FileService(vector_store)


@app.command()
def start():
    start_listener(file_service, config.PATHS_TO_WATCH)


@app.command()
def query(query: str):
    files = file_service.query_files(query)

    for index, file_path in enumerate(files):
        file_name = os.path.basename(file_path)
        print(f"{index + 1}: {file_name}")


if __name__ == "__main__":
    app()
