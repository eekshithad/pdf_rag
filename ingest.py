from utils.pdf_loader import load_new_pdfs
from utils.metadata import enrich_metadata
from utils.chunker import split_documents
from utils.index_tracker import mark_indexed

from rag.embeddings import get_embedding_model
from rag.vectorstore import (load_or_create_db, add_documents)

print("=" * 60)
print("PDF INGESTION")
print("=" * 60)

# -----------------------------
# Load only new PDFs
# -----------------------------
print("\nLoading PDFs...")

docs = load_new_pdfs()

print(f"Loaded {len(docs)} pages")

# No new PDFs
if len(docs) == 0:
    print("\nNo new PDFs found.")
    print("Vector database is already up to date.")
    exit()

# -----------------------------
# Enrich metadata
# -----------------------------
docs = enrich_metadata(docs)

# -----------------------------
# Split into chunks
# -----------------------------
print("\nChunking...")

chunks = split_documents(docs)

print(f"Created {len(chunks)} chunks")

# -----------------------------
# Create embeddings & store
# -----------------------------
print("\nCreating embeddings...")

embedding = get_embedding_model()


db = load_or_create_db(embedding)

add_documents(db, chunks)

# -----------------------------
# Update index tracker
# -----------------------------
indexed = set()

for doc in docs:

    file_name = doc.metadata["file_name"]

    if file_name not in indexed:

        mark_indexed(
            file_name,
            doc.metadata.get("total_pages", 0)
        )

        indexed.add(file_name)

print("\nIndexed files updated.")

print("\nDone!")