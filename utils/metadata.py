from pathlib import Path

def enrich_metadata(documents):

    for doc in documents:

        source = doc.metadata.get("source", "")

        doc.metadata["file_name"] = Path(source).name

    return documents