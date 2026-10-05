from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader

from utils.index_tracker import is_indexed


def load_pdf(pdf_path: str):
    """
    Load a single PDF and return LangChain Document objects.
    """

    loader = PyMuPDFLoader(pdf_path)

    return loader.load()


def load_all_pdfs(upload_folder="uploads"):

    documents = []

    upload_path = Path(upload_folder)

    for pdf in upload_path.glob("*.pdf"):

        docs = load_pdf(str(pdf))

        documents.extend(docs)

    return documents


def load_new_pdfs(upload_folder="uploads"):

    documents = []

    upload_path = Path(upload_folder)

    for pdf in upload_path.glob("*.pdf"):

        if is_indexed(pdf.name):

            print(f"Skipping {pdf.name}")

            continue

        print(f"Loading {pdf.name}")

        docs = load_pdf(str(pdf))

        documents.extend(docs)

    return documents