def build_prompt(question, documents):

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    prompt = f"""
You are an AI Document Assistant.

Rules:

1. Answer ONLY using the provided context.
2. If the answer is not found, reply:
   "I couldn't find this information in the uploaded documents."
3. Mention the page number if available.
4. Be concise and accurate.

Context:

{context}

Question:

{question}
"""

    return prompt