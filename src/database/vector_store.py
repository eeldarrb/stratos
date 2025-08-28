import config
from uuid import uuid4
from langchain_milvus import Milvus


class VectorStore:
    def __init__(self, embeddings, uri=config.DATABASE_URI):
        self.vector_store = Milvus(
            embedding_function=embeddings,
            connection_args={"uri": uri},
        )

    def add_document(self, document):
        uuid = str(uuid4())
        self.vector_store.add_documents(documents=document, ids=uuid)

    def delete_document(self, document_id):
        self.vector_store.delete(ids=document_id)

    def search(self, query, k=10):
        results = self.vector_store.similarity_search_with_score(query=query, k=k)
        return results

    # def update_document():
