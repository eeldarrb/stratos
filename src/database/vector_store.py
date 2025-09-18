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

    def search(self, query, k=10):
        results = self.vector_store.similarity_search_with_score(query=query, k=k)
        return results

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

    def move_document(self, old_path, new_path):
        result = self._get_item_by_path(old_path)
        if result:
            doc_id, item = result
            self.vector_store.update_document(
                doc_id,
                Document(
                    page_content=item.text,
                    metadata={"path": new_path, "mimetype": item.mimetype},
                ),
            )

    def update_document(self, file_path, new_item: Item):
        result = self._get_item_by_path(file_path)
        if result:
            doc_id, _ = result
            self.vector_store.update_document(
                doc_id,
                Document(
                    page_content=new_item.text,
                    metadata={
                        "path": new_item.file_path,
                        "mimetype": new_item.mimetype,
                    },
                ),
            )

    def delete_document(self, file_path):
        result = self._get_item_by_path(file_path)
        if result:
            doc_id, _ = result
            self.vector_store.delete(ids=[doc_id])

    def _get_item_by_path(self, file_path: str) -> tuple[str, Item] | None:
        result = self.vector_store.get(where={"path": file_path})
        ids = result.get("ids")
        texts = result.get("documents")
        metadatas = result.get("metadatas")

        if ids and texts and metadatas and len(ids) == 1:
            id = ids[0]
            text = texts[0]
            metadata = metadatas[0]

            item = Item(
                text=text,
                file_path=metadata.get("path"),
                mimetype=metadata.get("mimetype"),
                source=metadata.get("source", ""),
            )
            return id, item
        return None
