from langchain_chroma import Chroma

from config import CHROMA_DB_PATH


def load_or_create_db(embedding):
    """
    Load an existing ChromaDB database.
    If it doesn't exist, Chroma will create it automatically.
    """

    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding
    )

    return db


def add_documents(db, chunks):
    """
    Add new document chunks to the existing database.
    """

    if not chunks:
        print("No new chunks to add.")
        return

    db.add_documents(chunks)

    print(f"Added {len(chunks)} chunks to ChromaDB.")


def load_vector_db(embedding):
    """
    Used during querying.
    """

    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding
    )