from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents,
    chunk_size=800,
    chunk_overlap=150
):
    """
    Split documents into overlapping chunks while
    preserving metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    return chunks