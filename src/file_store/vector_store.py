from uuid import uuid4
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from .file_store import FileStore
from src.ingest.utils import get_filename, get_mimetype
from src.types.file_record import FileRecord


class VectorStore(FileStore):
    def __init__(self, embedding_model, uri):
        self._client = Chroma(
            collection_name="local_files",
            embedding_function=OllamaEmbeddings(model=embedding_model),
            persist_directory=uri,
        )

    def add(self, files: list[FileRecord]):
        docs = []
        doc_ids = [str(uuid4()) for _ in range(len(files))]
        for file in files:
            docs.append(self._file_to_document(file))
        self._client.add_documents(ids=[doc_ids], documents=docs)

    def update(self, file_path: str, new_file: FileRecord):
        doc_id = self._get_ids_by_path(file_path)
        if doc_id:
            new_doc = self._file_to_document(new_file)
            self._client.update_document(document_id=doc_id, document=new_doc)
        else:
            raise FileNotFoundError(file_path)

    def delete_by_path(self, file_path: str):
        doc_id = self._get_ids_by_path(file_path)
        if doc_id:
            self._client.delete(ids=[doc_id])
        else:
            raise FileNotFoundError(file_path)

    def move(self, old_path: str, new_path: str):
        res = self._get_documents_where(path=old_path)
        print(res)

        if res and res.get("ids"):
            doc_id = res["ids"][0]
            page_content = res["documents"][0]

            metadata = res["metadatas"][0]
            metadata["path"] = new_path
            metadata["source"] = get_filename(new_path)
            metadata["mimetype"] = get_mimetype(new_path)

            updated_doc = Document(page_content=page_content, metadata=metadata)
            self._client.update_document(document_id=doc_id, document=updated_doc)
        else:
            raise FileNotFoundError(old_path)

    def query(self, query: str, k: int = 10) -> list[tuple[FileRecord, float]]:
        files = []
        documents = self._client.similarity_search_with_score(query, k=k)
        for document, score in documents:
            file = self._document_to_file(document)
            files.append((file, score))
        return files

    def _get_documents_where(self, **kwargs):
        results = self._client.get(where=kwargs)
        return results

    # TODO: test the get id method
    def _get_ids_by_path(self, file_path: str) -> str:
        return self._client.get(where={"path": file_path}).get("ids", [])

    def _file_to_document(self, file: FileRecord) -> Document:
        return Document(
            page_content=file.text,
            metadata={
                "path": file.file_path,
                "mimetype": file.mimetype,
                "source": file.source,
            },
        )

    def _document_to_file(self, document: Document) -> FileRecord:
        text = document.page_content
        metadata = document.metadata

        file_path = metadata.get("path", "")
        source = metadata.get("source", "")
        mimetype = metadata.get("mimetype", "")

        return FileRecord(text, file_path, mimetype, source)
