# 🏥 MediAssist AI
### Intelligent Multimodal Healthcare Assistant using Agentic AI, RAG, LangGraph, MCP and FastAPI

## 📌 Project Overview

Healthcare organizations deal with a large volume of unstructured and structured data such as Standard Operating Procedures (SOPs), discharge summaries, prescriptions, medical reports, and patient records stored in databases. Retrieving accurate information from these sources is often time-consuming and prone to errors.

**MediAssist AI** is an intelligent healthcare assistant that combines **Retrieval-Augmented Generation (RAG)**, **Multimodal AI**, **Model Context Protocol (MCP)**, and **Agentic AI** to provide accurate, grounded, and context-aware responses from healthcare documents, medical images, and hospital databases.

The system minimizes hallucinations by retrieving relevant context before generating responses and always provides answers grounded in trusted data sources.

---

# 🎯 Problem Statement

Healthcare professionals often need to retrieve information from multiple sources:

- Hospital SOP documents
- Patient discharge summaries
- Medical prescriptions
- Laboratory reports
- Hospital database
- Insurance documentation

Traditional keyword search is inefficient, while standalone Large Language Models (LLMs) may generate hallucinated or unsupported answers.

The challenge is to build a unified AI assistant capable of:

- Understanding natural language questions
- Searching multiple document formats
- Reading medical images and prescriptions
- Querying hospital databases
- Providing accurate, source-grounded responses
- Reducing hallucinations

---

# 💼 Business Logic

The application intelligently routes each user query to the appropriate processing pipeline.

### Document Questions

```
User Question
      │
      ▼
Planner Agent
      │
      ▼
RAG Pipeline
      │
Retrieve Relevant Chunks
      │
Groq LLM
      │
Grounded Answer
```

---

### Medical Image Questions

```
Medical Image
      │
      ▼
EasyOCR
      │
      ▼
Vision LLM
      │
      ▼
Structured Medical Summary
      │
      ▼
Vector Database
      │
      ▼
Grounded Response
```

---

### Database Questions

```
User Question
      │
      ▼
Planner Agent
      │
      ▼
MCP Agent
      │
      ▼
PostgreSQL
      │
      ▼
Reasoning Agent
      │
      ▼
Answer
```

---

# ⭐ Features

## 📄 Document Intelligence

- PDF processing
- DOCX support
- TXT support
- CSV support
- Semantic document search
- Source citation

---

## 🖼️ Multimodal AI

Supports:

- Medical prescriptions
- Laboratory reports
- Scanned documents
- Images

Capabilities:

- OCR using EasyOCR
- Vision LLM analysis
- Structured medical summaries

---

## 🤖 Agentic AI

Implemented using LangGraph.

Agents include:

- Input Guardrail
- Planner Agent
- Retriever Agent
- Multimodal Agent
- MCP Agent
- Reasoning Agent
- Output Guardrail

---

## 📚 Retrieval-Augmented Generation (RAG)

Pipeline:

- Document Loading
- Text Chunking
- Embedding Generation
- FAISS Indexing
- Semantic Retrieval
- Context-Aware Answer Generation

Benefits:

- Reduces hallucinations
- Improves answer quality
- Source-grounded responses

---

## 🗄️ Model Context Protocol (MCP)

The MCP Agent interacts with PostgreSQL for structured queries.

Supported tools:

- Search Patients
- Patient History
- Laboratory Results
- Payment Summary

---

## 📊 Monitoring

Provides:

- System Health API
- Processing Statistics
- Request Monitoring

---

## 🧪 Evaluation Framework

Supports automated evaluation using a Golden Dataset.

Evaluation Metrics:

- Accuracy
- Faithfulness
- Grounding
- Relevance
- Completeness
- Hallucination Rate
- Confidence Score
- Response Time

---

# 🏗️ Tech Stack

## Backend

- FastAPI
- Python

## Frontend

- Streamlit

## AI Framework

- LangChain
- LangGraph

## LLM

- Groq LLM

## Embeddings

- Sentence Transformers

## Vector Database

- FAISS

## OCR

- EasyOCR

## Vision Processing

- Hugging Face Transformers

## Database

- PostgreSQL

## Deployment

- Docker

---

# 📁 Project Structure

```
MediAssist_AI_CapstoneProj/

│
├── App/
│   ├── backend/
│   ├── frontend/
│   ├── data/
│   └── store/
│
├── backend.dockerfile
├── frontend.dockerfile
├── requirements_backend.txt
├── requirements_frontend.txt
├── .dockerignore
└── README.md
```

---

# ⚙️ Setup Guide

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/MediAssist_AI_CapstoneProj.git

cd MediAssist_AI_CapstoneProj
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

Backend

```bash
pip install -r requirements_backend.txt
```

Frontend

```bash
pip install -r requirements_frontend.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key

DB_HOST=your_host

DB_PORT=5432

DB_NAME=your_database

DB_USER=your_username

DB_PASSWORD=your_password
```

---

## 5. Start Backend

```bash
uvicorn backend.app:app --reload
```

Backend URL

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

## 6. Start Frontend

```bash
streamlit run frontend/Chat.py
```

Frontend URL

```
http://localhost:8501
```

---

# 🐳 Docker Deployment

## Build Backend

```bash
docker build -f backend.dockerfile -t mediassist-backend .
```

Run Backend

```bash
docker run -d \
--name mediassist-backend \
-p 8000:8000 \
--env-file .env \
mediassist-backend
```

---

## Build Frontend

```bash
docker build -f frontend.dockerfile -t mediassist-frontend .
```

Run Frontend

```bash
docker run -d \
--name mediassist-frontend \
-p 8501:8501 \
-e BACKEND_URL=http://host.docker.internal:8000 \
mediassist-frontend
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home |
| POST | /upload | Upload documents/images |
| POST | /ask | Ask questions |
| GET | /files | List uploaded files |
| DELETE | /delete/{filename} | Delete file |
| GET | /system-health | System monitoring |

---

# 🚀 Future Enhancements

- Hybrid Search (BM25 + Vector Search)
- Persistent Cloud Storage
- User Authentication
- Kubernetes Deployment
- Medical Knowledge Graph Integration
- Redis Caching
- Multi-language Support
- Audit Logging
- Role-Based Access Control

---

# 👩‍💻 Author

**Priyanka Nikam**

AI/ML Engineer | GenAI | Agentic AI | RAG | LangGraph | FastAPI

---

# 📄 License

This project is intended for educational, research, and demonstration purposes.