import config
from dataclasses import dataclass
from uuid import uuid4
from langchain_chroma import Chroma
from langchain_core.documents import Document


@dataclass()
class Item:
    text: str
    file_path: str
    mimetype: str
    source: str


class VectorStore:
    def __init__(self, embeddings, uri=config.DATABASE_URI):
        self.vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=uri,
        )

    def add_items(self, items: list[Item]):
        docs = []
        uuids = []
        for item in items:
            uuids.append(str(uuid4()))
            metadata = {"path": item.file_path, "mimetype": item.mimetype}
            docs.append(Document(page_content=item.text, metadata=metadata))
        self.vector_store.add_documents(documents=docs, ids=uuids)

    def delete_document(self, document_id):
        self.vector_store.delete(ids=document_id)

    def search(self, query, k=10):
        results = self.vector_store.similarity_search_with_score(query=query, k=3)
        return results

    # def update_document():
