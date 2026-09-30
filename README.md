# 🌱 PapriCore RAG: Enterprise-Grade Local AI for Greenhouse Operations

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)
![Foundry Local](https://img.shields.io/badge/Microsoft-Foundry_Local-blue?logo=windows)
![Offline](https://img.shields.io/badge/Status-100%25_Offline-success)

PapriCore is a fully local, privacy-first **Retrieval-Augmented Generation (RAG)** application engineered specifically for agricultural and greenhouse operations. By utilizing Microsoft Foundry Local SDK, it enables workers and management to query complex operational standards, performance metrics, and quality control guidelines instantly—without relying on cloud connectivity or exposing sensitive company data.

## 🎯 The Problem & The Solution
In large-scale greenhouse facilities (e.g., in Andijk, Netherlands), standardizing harvesting techniques, hygiene protocols, and packaging norms across a diverse workforce is challenging. 

**PapriCore solves this by:**
1. Transforming static company rulebooks (`guidelines.txt`) into an interactive, AI-driven knowledge base.
2. Running 100% offline, making it highly resilient in agricultural environments with unstable internet connections.
3. Ensuring zero data leakage, as all LLM inferences and vector searches occur directly on the local machine.

## 🏗️ Architecture & Workflow
The system utilizes a custom-built, lightweight RAG pipeline:
- **Ingestion:** Reads raw operational guidelines and chunks them into semantic paragraphs.
- **Embedding:** Uses **Qwen 3 Embedding (0.6b)** to convert text chunks into high-dimensional vectors.
- **Retrieval:** Employs **NumPy** to calculate Cosine Similarity, extracting the most relevant context based on the user's query.
- **Generation:** Feeds the retrieved context to **Qwen 2.5 Chat (0.5b)**, which strictly limits its answers to the provided operational data to prevent AI hallucinations.
- **Persistence:** Maintains user session state and chat history locally via an integrated **SQLite** database.

## 💻 Tech Stack
| Component | Technology |
|---|---|
| **Programming Language** | Python |
| **Local AI Engine** | Microsoft Foundry Local SDK (`winml`) |
| **Large Language Model (LLM)** | Qwen2.5-0.5b (Instruct) |
| **Embedding Model** | Qwen3-Embedding-0.6b |
| **Vector Math / Search** | NumPy (Cosine Similarity) |
| **Web Interface** | Streamlit |
| **Database (Memory)** | SQLite |

## 📂 Project Structure
```text
papricore_rag/
├── app.py                # Main Streamlit web application & SQLite integration
├── main.py               # CLI version of the RAG pipeline (for terminal use)
├── guidelines.txt        # The custom knowledge base (Domain context)
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules (excludes DB and cache)
└── README.md             # Project documentation# 🌱 PapriCore RAG: Enterprise-Grade Local AI for Greenhouse Operations

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)
![Foundry Local](https://img.shields.io/badge/Microsoft-Foundry_Local-blue?logo=windows)
![Offline](https://img.shields.io/badge/Status-100%25_Offline-success)

PapriCore is a fully local, privacy-first **Retrieval-Augmented Generation (RAG)** application engineered specifically for agricultural and greenhouse operations. By utilizing Microsoft Foundry Local SDK, it enables workers and management to query complex operational standards, performance metrics, and quality control guidelines instantly—without relying on cloud connectivity or exposing sensitive company data.

## 🎯 The Problem & The Solution
In large-scale greenhouse facilities (e.g., in Andijk, Netherlands), standardizing harvesting techniques, hygiene protocols, and packaging norms across a diverse workforce is challenging. 

**PapriCore solves this by:**
1. Transforming static company rulebooks (`guidelines.txt`) into an interactive, AI-driven knowledge base.
2. Running 100% offline, making it highly resilient in agricultural environments with unstable internet connections.
3. Ensuring zero data leakage, as all LLM inferences and vector searches occur directly on the local machine.

## 🏗️ Architecture & Workflow
The system utilizes a custom-built, lightweight RAG pipeline:
- **Ingestion:** Reads raw operational guidelines and chunks them into semantic paragraphs.
- **Embedding:** Uses **Qwen 3 Embedding (0.6b)** to convert text chunks into high-dimensional vectors.
- **Retrieval:** Employs **NumPy** to calculate Cosine Similarity, extracting the most relevant context based on the user's query.
- **Generation:** Feeds the retrieved context to **Qwen 2.5 Chat (0.5b)**, which strictly limits its answers to the provided operational data to prevent AI hallucinations.
- **Persistence:** Maintains user session state and chat history locally via an integrated **SQLite** database.

## 💻 Tech Stack
| Component | Technology |
|---|---|
| **Programming Language** | Python |
| **Local AI Engine** | Microsoft Foundry Local SDK (`winml`) |
| **Large Language Model (LLM)** | Qwen2.5-0.5b (Instruct) |
| **Embedding Model** | Qwen3-Embedding-0.6b |
| **Vector Math / Search** | NumPy (Cosine Similarity) |
| **Web Interface** | Streamlit |
| **Database (Memory)** | SQLite |

## 📂 Project Structure
```text
papricore_rag/
├── app.py                # Main Streamlit web application & SQLite integration
├── main.py               # CLI version of the RAG pipeline (for terminal use)
├── guidelines.txt        # The custom knowledge base (Domain context)
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules (excludes DB and cache)
└── README.md             # Project documentation
