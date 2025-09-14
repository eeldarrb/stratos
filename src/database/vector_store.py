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
            collection_name="local_files",
            embedding_function=embeddings,
            persist_directory=uri,
        )

    def add_items(self, items: list[Item]):
        docs = []
        uuids = []
        for item in items:
            uuids.append(str(uuid4()))
            docs.append(
                Document(
                    page_content=item.text,
                    metadata={"path": item.file_path, "mimetype": item.mimetype},
                )
            )
        self.vector_store.add_documents(documents=docs, ids=uuids)

    def delete_document(self, document_id):
        self.vector_store.delete(ids=document_id)

    def search(self, query, k=10):
        results = self.vector_store.similarity_search_with_score(query=query, k=k)
        return results

    def update_document(self, file_path, new_item):
        doc_ids = self.vector_store.get(where={"path": file_path}).get("ids")

        if doc_ids:
            doc_id = doc_ids[0]
            updated_doc = Document(
                page_content=new_item.text,
                metadata={"path": new_item.file_path, "mimetype": new_item.mimetype},
            )
            self.vector_store.update_document(doc_id, updated_doc)
