import os
import tempfile
import streamlit as st

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

st.set_page_config(page_title="Smart PDF Assistant")

st.title("📄 Smart PDF Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    st.success("PDF uploaded successfully!")

    # Load PDF
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    # Embedding model
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    # Create Vector DB
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    question = st.text_input("Ask a question")

    if question:

        docs = db.similarity_search(
            question,
            k=4
        )

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = f"""
You are a PDF assistant.

Answer ONLY from the given context.

If the answer is not present, say:

"I couldn't find this information in the uploaded PDF."

Context:

{context}

Question:

{question}
"""

        llm = ChatOllama(
            model="llama3.1"
        )

        response = llm.invoke(prompt)

        st.subheader("Answer")

        st.write(response.content)