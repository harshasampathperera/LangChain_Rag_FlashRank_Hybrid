from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank

# ============================================================
# 1. CREATE EMBEDDING MODEL
# ============================================================

embeddings = OllamaEmbeddings(model="nomic-embed-text")


# ============================================================
# 2. CONNECT TO CHROMADB
# ============================================================

vectorstore = Chroma(
    collection_name="pdf_docs",
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)


# ============================================================
# 3. CREATE VECTOR RETRIEVER
# ============================================================
#
# We retrieve 10 documents first.
# Later the reranker will select the best 5.
#

vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})


# ============================================================
# 4. LOAD DOCUMENTS FROM CHROMADB
# ============================================================
#
# BM25 needs access to the actual document text.
#

data = vectorstore.get(include=["documents", "metadatas"])


# ============================================================
# 5. CONVERT CHROMA DOCUMENTS TO LANGCHAIN DOCUMENTS
# ============================================================

documents = [
    Document(page_content=text, metadata=metadata)
    for text, metadata in zip(data["documents"], data["metadatas"])
]


print("\nDocuments loaded from ChromaDB:", len(documents))


# ============================================================
# 6. CREATE BM25 KEYWORD RETRIEVER
# ============================================================
#
# BM25 looks for important keywords in the documents.
#

bm25_retriever = BM25Retriever.from_documents(documents)

bm25_retriever.k = 10


# ============================================================
# 7. CREATE HYBRID SEARCH
# ============================================================
#
# Hybrid Search combines:
#
# 50% Vector Search
# 50% BM25 Keyword Search
#

hybrid_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever], weights=[0.5, 0.5]
)


# ============================================================
# 8. CREATE RERANKER
# ============================================================
#
# FlashRank looks at the question and retrieved documents
# and selects the most relevant documents.
#

# reranker = FlashrankRerank(
# )

reranker = FlashrankRerank(model="ms-marco-TinyBERT-L-2-v2", top_n=5)
# ============================================================
# 9. CREATE FINAL RETRIEVER
# ============================================================
#
# Pipeline:
#
# Hybrid Search
#      ↓
# 10 candidate chunks
#      ↓
# FlashRank
#      ↓
# Best 5 chunks
#

reranking_retriever = ContextualCompressionRetriever(
    base_retriever=hybrid_retriever, base_compressor=reranker
)


# ============================================================
# 10. CREATE LLM
# ============================================================

llm = ChatOllama(model="llama3.2:1b")


# ============================================================
# 11. CREATE CHAT HISTORY
# ============================================================

chat_history = []


# ============================================================
# 12. CREATE PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.

Answer the user's question using the PDF information
and the conversation history.

Use the PDF information when it is relevant.

If the PDF does not contain enough information,
you may use your general knowledge.

CONVERSATION HISTORY:

{chat_history}


PDF INFORMATION:

{context}


CURRENT QUESTION:

{question}


ANSWER:
""")


# ============================================================
# 13. START CONVERSATION
# ============================================================

print("\n============================================")
print("       LangChain Hybrid RAG Chatbot")
print("============================================")
print("Type 'exit' to quit.")
print()


while True:

    # --------------------------------------------------------
    # Get user question
    # --------------------------------------------------------

    question = input("You: ")

    # --------------------------------------------------------
    # Exit chatbot
    # --------------------------------------------------------

    if question.lower() == "exit":

        print("\nGoodbye!")

        break

    # --------------------------------------------------------
    # HYBRID SEARCH + RERANKING
    # --------------------------------------------------------

    print("\nSearching documents...")

    documents = reranking_retriever.invoke(question)

    # --------------------------------------------------------
    # SHOW NUMBER OF DOCUMENTS
    # --------------------------------------------------------

    print(f"Retrieved {len(documents)} relevant chunks.")

    # --------------------------------------------------------
    # COMBINE RETRIEVED DOCUMENTS
    # --------------------------------------------------------

    context = "\n\n".join(document.page_content for document in documents)

    # --------------------------------------------------------
    # CONVERT CHAT HISTORY TO TEXT
    # --------------------------------------------------------

    history_text = "\n".join(
        f"User: {user_question}\nAI: {answer}" for user_question, answer in chat_history
    )

    # --------------------------------------------------------
    # CREATE FINAL PROMPT
    # --------------------------------------------------------

    messages = prompt.invoke(
        {"chat_history": history_text, "context": context, "question": question}
    )

    # --------------------------------------------------------
    # SEND PROMPT TO LLM
    # --------------------------------------------------------

    print("\nGenerating answer...")

    response = llm.invoke(messages)

    # --------------------------------------------------------
    # GET ANSWER
    # --------------------------------------------------------

    answer = response.content

    # --------------------------------------------------------
    # DISPLAY ANSWER
    # --------------------------------------------------------

    print("\n============================================")
    print("AI:")
    print("============================================")

    print(answer)

    # --------------------------------------------------------
    # SAVE CHAT HISTORY
    # --------------------------------------------------------

    chat_history.append((question, answer))
