import os

from src.types.file_record import FileRecord
from .file_store import FileStore

from src.preprocessors.chunker import chunk_text
from src.preprocessors.extractor import extract_text
from src.ingest.utils import get_filename, get_mimetype


class FileService:
    def __init__(self, store: FileStore):
        self._store = store

    def process_path(self, file_path):
        if os.path.isdir(file_path):
            for root, _, files in os.walk(file_path):
                for file in files:
                    if not file.startswith("."):
                        path = os.path.join(root, file)
                        self.add_file(path)
        else:
            self.add_file(file_path)

    def add_file(self, file_path):
        try:
            file_records = []

            raw_text = extract_text(file_path)
            chunks = chunk_text(raw_text)

            # TODO: change source to base file name?
            for chunk in chunks:
                mimetype = get_mimetype(file_path)
                source = get_filename(file_path)
                file_record = FileRecord(chunk, file_path, mimetype, source)
                file_records.append(file_record)

            self._store.add(file_records)

        except Exception as e:
            print(f"Error processing file {e}")

    def delete_file(self, file_path):
        self._store.delete_by_path(file_path)
