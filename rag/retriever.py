from rag.embeddings import get_embedding_model
from rag.vectorstore import load_vector_db

from config import TOP_K


class Retriever:

    def __init__(self):

        self.embedding = get_embedding_model()

        self.db = load_vector_db(self.embedding)

    def search(self, question):

        docs = self.db.similarity_search(
            question,
            k=TOP_K
        )

        return docs