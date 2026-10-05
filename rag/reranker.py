from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):
        print("Loading Cross Encoder...")
        self.model = CrossEncoder("BAAI/bge-reranker-base")

    def rerank(self, question, documents, top_k=4):
        """
        Rerank retrieved documents.
        """

        pairs = [
            (question, doc.page_content)
            for doc in documents
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(scores, documents),
            key=lambda x: x[0],
            reverse=True
        )

        return [doc for score, doc in ranked[:top_k]]