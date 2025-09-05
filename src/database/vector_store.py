import config
from uuid import uuid4
from langchain_chroma import Chroma
from langchain_core.documents import Document


class VectorStore:
    def __init__(self, embeddings, uri=config.DATABASE_URI):
        self.vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=uri,
        )

    def add_item(self, text, file_path, mimetype):
        uuid = str(uuid4())
        print(uuid)
        doc = Document(
            page_content=text,
            metadata={
                "path": file_path,
                "mimetype": mimetype,
            },
        )
        self.vector_store.add_documents(documents=[doc], ids=uuid)

    def delete_document(self, document_id):
        self.vector_store.delete(ids=document_id)

    def search(self, query, k=10):
        results = self.vector_store.similarity_search_with_score(query=query, k=3)
        return results

    # def update_document():
