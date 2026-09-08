# LangChain RAG with Hybrid Search and FlashRank Reranking

A beginner-friendly **Retrieval-Augmented Generation (RAG)** project built with **LangChain, ChromaDB, Ollama, BM25 Hybrid Search, and FlashRank Reranking**.

This project allows you to ask questions about a collection of PDF documents and receive answers based on the information retrieved from those documents.

---

## 🚀 Project Overview

This project demonstrates an advanced RAG pipeline:

```text
                    PDF Documents
                         │
                         ▼
                ┌─────────────────┐
                │ PDF Loader      │
                │ PyPDFDirectory  │
                │ Loader          │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Splitting  │
                │                 │
                │ Chunk Size:1000 │
                │ Overlap: 200    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Ollama Embedding │
                │ nomic-embed-text │
                └────────┬────────┘
                         │
                         ▼
                    ┌─────────┐
                    │ ChromaDB│
                    └─────────┘
                         │
                         │
User Question ──────────┤
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Vector Search            BM25 Search
       Semantic Search          Keyword Search
              │                     │
              └──────────┬──────────┘
                         ▼
                  Hybrid Search
                         │
                         ▼
                FlashRank Reranker
                         │
                         ▼
                  Top 5 Documents
                         │
                         ▼
                    Ollama LLM
                    llama3.2:1b
                         │
                         ▼
                       Answer
```

---

## ✨ Features

* 📄 Read multiple PDF documents
* ✂️ Split documents into smaller chunks
* 🧠 Generate embeddings using Ollama
* 🗄️ Store embeddings in ChromaDB
* 🔎 Semantic vector search
* 🔤 BM25 keyword search
* 🔀 Hybrid Search combining vector + BM25 retrieval
* 📊 FlashRank document reranking
* 🤖 Local LLM using Ollama
* 💬 Conversational question answering
* 🔒 Runs locally without sending documents to a cloud LLM API

---

## 🛠️ Technologies Used

| Technology        | Purpose                   |
| ----------------- | ------------------------- |
| Python            | Programming language      |
| LangChain         | RAG application framework |
| LangChain Classic | Retriever components      |
| ChromaDB          | Vector database           |
| Ollama            | Local AI model runtime    |
| nomic-embed-text  | Embedding model           |
| llama3.2:1b       | Local chat model          |
| BM25              | Keyword-based retrieval   |
| FlashRank         | Document reranking        |
| PyPDF             | PDF processing            |

---

## 📁 Project Structure

```text
LangChain_RAG_FlashRank_Hybrid/
│
├── .venv/
│
├── pdf_documents/
│   ├── PowerBI.pdf
│   ├── DAX.pdf
│   └── MicrosoftFabric.pdf
│
├── chroma_db/
│
├── LangChain_Embedding.py
│
├── LLM_RAG_RRank_Hybrid.py
│
├── README.md
│
└── .gitignore
```

### Main Files

**`LLM_PDF_LangChain_Embedding.py`**

Responsible for:

* Loading PDF documents
* Splitting text into chunks
* Creating embeddings
* Storing documents and embeddings in ChromaDB

**`LLM_RAG_RRank_Hybrid.py`**

Responsible for:

* Loading the ChromaDB vector store
* Performing vector search
* Performing BM25 keyword search
* Combining results using Hybrid Search
* Reranking results with FlashRank
* Sending relevant context to the Ollama LLM
* Maintaining conversation history

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/LangChain_RAG_FlashRank_Hybrid.git
```

Move into the project:

```powershell
cd LangChain_RAG_FlashRank_Hybrid
```

---

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv) PS D:\LLMProject\LangChain_RAG_FlashRank_Hybrid>
```

---

## 3. Install Python Dependencies

```powershell
python -m pip install langchain langchain-community langchain-classic langchain-chroma langchain-ollama langchain-text-splitters pypdf rank-bm25 flashrank
```

---

# 🤖 Install Ollama

Download and install Ollama from:

https://ollama.com/

After installation, verify:

```powershell
ollama --version
```

---

## Download the AI Models

### Embedding Model

```powershell
ollama pull nomic-embed-text
```

### Chat Model

```powershell
ollama pull llama3.2:1b
```

Verify installed models:

```powershell
ollama list
```

You should have:

```text
nomic-embed-text
llama3.2:1b
```

---

# 📄 Add PDF Documents

Place your PDF files inside:

```text
pdf_documents/
```

For example:

```text
pdf_documents/
├── PowerBI.pdf
├── DAX.pdf
└── MicrosoftFabric.pdf
```

You can replace these PDFs with your own documents.

---

# 🧠 Step 1 — Create the Vector Database

Run:

```powershell
python LangChain_Embedding.py
```

The program will:

```text
PDF Documents
      ↓
Load PDFs
      ↓
Split Text
      ↓
Create Embeddings
      ↓
Store in ChromaDB
```

Example output:

```text
PDF pages loaded: 150
Chunks created: 500

Successfully stored documents in ChromaDB!
```

The vector database will be stored in:

```text
chroma_db/
```

---

# 🔎 Step 2 — Run RAG

Run:

```powershell
python LLM_RAG_RRank_Hybrid.py
```

You can then ask questions:

```text
You: What is DirectQuery in Power BI?
```

The system retrieves relevant information from the PDF documents and sends the best context to the local LLM.

---

# 🔀 How Hybrid Search Works

Traditional vector search searches based on **meaning**.

For example:

```text
Question:
How can I connect Power BI directly to a database?
```

Vector search can understand that:

```text
DirectQuery
```

is related to the question even when the exact word is not present.

However, vector search can sometimes struggle with exact technical terms.

For example:

```text
CALCULATE
SUMX
DP-600
DirectQuery
OneLake
```

This is where **BM25 keyword search** is useful.

### Hybrid Search

This project combines:

```text
Vector Search
      +
BM25 Keyword Search
      ↓
Hybrid Search
```

The system uses both semantic meaning and exact keyword matching.

---

# 🎯 Why Use Reranking?

Hybrid search can return several potentially relevant documents.

For example:

```text
Question
   ↓
Hybrid Search
   ↓
10 candidate chunks
   ↓
FlashRank
   ↓
5 best chunks
   ↓
LLM
```

FlashRank evaluates the relevance of the retrieved documents against the question and improves the ordering of the results.

Therefore:

### Retrieval

Find potentially relevant documents.

### Reranking

Find the **most relevant documents among those candidates**.

---

# 🧩 RAG Pipeline

The complete pipeline is:

```text
                 USER QUESTION
                       │
                       ▼
              ┌─────────────────┐
              │  Vector Search  │
              └────────┬────────┘
                       │
                       │
              ┌────────▼────────┐
              │   BM25 Search   │
              └────────┬────────┘
                       │
                       ▼
                HYBRID SEARCH
                       │
                       ▼
              Candidate Documents
                       │
                       ▼
              ┌─────────────────┐
              │    FlashRank    │
              │    Reranking    │
              └────────┬────────┘
                       │
                       ▼
                 Top Documents
                       │
                       ▼
                Context + Query
                       │
                       ▼
              ┌─────────────────┐
              │   Ollama LLM    │
              │   llama3.2:1b   │
              └────────┬────────┘
                       │
                       ▼
                     ANSWER
```

---

# 💬 Conversational RAG

The application maintains conversation history.

Example:

```text
You:
What is Power BI?

AI:
Power BI is Microsoft's business intelligence platform...

You:
What are its main components?

AI:
The main components include Power BI Desktop,
Power BI Service, Power Query, and DAX...
```

The previous conversation is included in the prompt so that follow-up questions can be understood in context.

---

# ⚙️ Important Configuration

## Chunk Size

The document splitter uses:

```python
chunk_size=1000
```

This means the text is divided into chunks of approximately 1000 characters.

## Chunk Overlap

```python
chunk_overlap=200
```

The overlap helps preserve context between neighbouring chunks.

---

## Number of Retrieved Documents

The vector retriever initially retrieves:

```python
k=10
```

The Hybrid Search combines candidate documents from:

```text
Vector Search → 10
BM25 Search   → 10
```

FlashRank then selects the best:

```python
top_n=5
```

---

# 🧪 Experimentation

One of the goals of this project is to understand how different RAG configurations affect retrieval quality.

You can experiment with:

### Chunk Size

```text
500
1000
1500
2000
```

### Chunk Overlap

```text
50
100
200
300
```

### Number of Retrieved Documents

```text
k=3
k=5
k=10
k=20
```

### Hybrid Search Weights

For example:

```python
weights=[0.5, 0.5]
```

This gives equal importance to:

```text
Vector Search = 50%
BM25 Search   = 50%
```

You can experiment with different weights depending on your documents and questions.

---

# 🧠 What This Project Demonstrates

This project is designed to learn the evolution of RAG:

```text
Basic RAG
   ↓
Vector Search
   ↓
Better Chunking
   ↓
Hybrid Search
   ↓
Reranking
   ↓
Conversational RAG
```

It demonstrates how retrieval quality can be improved before information is passed to the LLM.

---

# 🔐 Local AI

The project uses Ollama to run the models locally.

```text
Your PDF
   ↓
Local Embedding Model
   ↓
Local ChromaDB
   ↓
Local Retrieval
   ↓
Local FlashRank
   ↓
Local LLM
```

This makes the project useful for experimenting with RAG without requiring a paid cloud LLM API.

---

# 📚 Example Questions

If your PDF collection contains Power BI, DAX, and Microsoft Fabric documentation, you can ask:

```text
What is Power BI?
```

```text
What is the difference between Import mode and DirectQuery?
```

```text
What is DAX?
```

```text
What does the CALCULATE function do?
```

```text
What is Microsoft Fabric?
```

```text
What is OneLake?
```

```text
What is a Fabric Lakehouse?
```

```text
What is the difference between a Lakehouse and a Warehouse?
```

---

# 🚧 Future Improvements

Possible improvements include:

* [ ] Better metadata filtering
* [ ] Persistent BM25 index
* [ ] Query rewriting
* [ ] Multi-query retrieval
* [ ] Improved conversation memory
* [ ] Source citations in answers
* [ ] PDF page references
* [ ] Streaming LLM responses
* [ ] Web-based UI
* [ ] Streamlit interface
* [ ] FastAPI backend
* [ ] Evaluation of retrieval accuracy
* [ ] RAGAS evaluation
* [ ] Experiment with different embedding models
* [ ] Experiment with different reranking models

---

# 🎓 Learning Objectives

This project helps understand the following concepts:

* Large Language Models (LLMs)
* Retrieval-Augmented Generation (RAG)
* Embeddings
* Vector Databases
* Semantic Search
* Keyword Search
* BM25
* Hybrid Search
* Reciprocal Rank Fusion
* Reranking
* Contextual Retrieval
* Prompt Engineering
* Conversational RAG
* Local LLMs
* Ollama
* LangChain

---

# 📌 Project Status

**Status:** Learning / Experimental Project

This project is being developed as a practical way to learn modern RAG architectures using open-source and locally running AI technologies.

---

# 👨‍💻 Author

**Harsha Sampath**

Senior Engineer – Business Intelligence & Data Analytics

Areas of interest:

* Power BI
* Microsoft Fabric
* Data Engineering
* Data Analytics
* Python
* PySpark
* LLMs
* RAG
* Generative AI

---

## ⭐ If You Find This Project Useful

Feel free to ⭐ star the repository and use the project as a starting point for your own RAG experiments.
