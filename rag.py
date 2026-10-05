from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

embedding = OllamaEmbeddings(model="nomic-embed-text")

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

query = input("Ask a question: ")

docs = db.similarity_search(query, k=3)

context = "\n\n".join(doc.page_content for doc in docs)

prompt = f"""
Answer only from the following context.

Context:
{context}

Question:
{query}
"""

llm = ChatOllama(model="llama3.1")

response = llm.invoke(prompt)

print("\nAnswer:\n")
print(response.content)