from langchain_ollama import OllamaEmbeddings

from config import EMBEDDING_MODEL


def get_embedding_model():
    """
    Returns the embedding model.
    """

    return OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )