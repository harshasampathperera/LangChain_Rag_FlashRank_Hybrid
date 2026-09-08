from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# ============================================================
# PDF → CHUNKS → EMBEDDINGS → CHROMADB
# ============================================================


# ------------------------------------------------------------
# 1. LOAD PDF DOCUMENTS
# ------------------------------------------------------------

loader = PyPDFDirectoryLoader("./pdf_documents")

documents = loader.load()

print("PDF pages loaded:", len(documents))


# ------------------------------------------------------------
# 2. SPLIT DOCUMENTS INTO CHUNKS
# ------------------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Chunks created:", len(chunks))


# ------------------------------------------------------------
# 3. ADD CHUNK INFORMATION TO METADATA
# ------------------------------------------------------------

for i, chunk in enumerate(chunks):

    chunk.metadata["chunk_id"] = i

    # Keep only useful metadata
    chunk.metadata["source"] = chunk.metadata.get(
        "source",
        "unknown"
    )

    chunk.metadata["page"] = chunk.metadata.get(
        "page",
        "unknown"
    )


# ------------------------------------------------------------
# 4. CREATE EMBEDDING MODEL
# ------------------------------------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ------------------------------------------------------------
# 5. CONNECT TO CHROMADB
# ------------------------------------------------------------

vectorstore = Chroma(
    collection_name="pdf_docs",
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


# ------------------------------------------------------------
# 6. STORE DOCUMENT CHUNKS
# ------------------------------------------------------------

vectorstore.add_documents(
    documents=chunks
)


# ------------------------------------------------------------
# 7. DISPLAY INFORMATION
# ------------------------------------------------------------

print("\n============================================")
print("       Embedding Completed Successfully")
print("============================================")

print(f"PDF pages : {len(documents)}")
print(f"Chunks    : {len(chunks)}")
print("Embedding : nomic-embed-text")
print("Database  : ChromaDB")
print("Collection: pdf_docs")

print("\nDocuments successfully stored in ChromaDB!")