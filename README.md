
<p align="center">
  <img src="frontend/assets/banner.png" alt="AI Chatbot Banner" width="80%">
</p>


<h1 align="center">🤖 AI Chatbot Using LLMs — Multi-Domain Intelligent Assistant</h1>

<p align="center">
  <b>FastAPI Backend + Streamlit Frontend + RAG + Groq LLMs</b>
</p>

---

## 🔗 **Visit Deployed App**
👉 **Live Demo:** *<your deployed link here>*

---

## 📌 **About the Project**

This project is a **full-stack AI Assistant** built using:

- **FastAPI backend**
- **Groq LLMs** (Llama-3 series)
- **RAG (Retrieval-Augmented Generation)**
- **FAISS vector search**
- **Streamlit frontend** with a stunning cyber-themed UI
- **Domain routing system (Education / Coding / Medical / Legal / General)**

Unlike a simple chatbot, this system is engineered for **multi-domain intelligence**, **contextual reasoning**, **document-aware conversation**, and **production-ready deployment**.

It is designed as a complete template for creating **personal AI assistants**, **enterprise chatbots**, or **educational tools** that blend LLM reasoning with retrieved knowledge.

---

## 🚀 **Key Features**

### 🌐 Multi-Domain AI Assistant  
Automatically routes queries to specialized agents:
- Education agent  
- Coding/debugging agent  
- Medical Q&A agent  
- Legal understanding agent  
- General reasoning agent  

### 📚 RAG Pipeline (Document-Augmented AI)
Upload PDFs or text files → they are embedded → stored in FAISS → retrieved dynamically.

### ⚡ FastAPI Backend
- REST `/chat` endpoint  
- Streaming WebSocket `/stream` endpoint  
- `/upload` endpoint for RAG documents  
- Metadata routing + confidence scoring  

### 🖥️ Modern Streamlit Frontend
- Cyberpunk AI theme  
- Animated chat interface  
- Message timestamps  
- Smooth scroll  
- Chat history export (.json / .txt)  
- Sliding sidebar  
- Domain-aware UI highlighting  

### 🔒 Production Ready
- Environment variables  
- Modular architecture  
- Logging  
- Error fallbacks  
- Model deprecation protection  

---

## 🧠 **Models Used**

### 🔹 **Groq LLM (Primary Model)**  
The recommended model:
```

llama3-groq-8b-tool-use-preview

```

Reason:
- Extremely fast inference  
- Strong reasoning  
- Production stable  
- Supported by Groq’s latest API  

### 🔹 Sentence Transformer (Embeddings for RAG)
```

sentence-transformers/all-MiniLM-L6-v2

```

Used for:
- Document chunk embedding  
- Semantic similarity search  

### 🔹 FAISS (Vector Store)
Used for fast retrieval of relevant knowledge chunks.

---

## 🏗️ **System Architecture**

```

```
             USER
               │
               ▼
      ┌────────────────┐
      │  Streamlit UI  │
      │ (Chat + Upload)│
      └────────────────┘
               │ REST / WS
               ▼
    ┌───────────────────────┐
    │        FastAPI        │
    │  /chat /stream /upload│
    └───────────────────────┘
               │
 ┌─────────────┼─────────────┐
 ▼             ▼             ▼
```

Domain Router   Agents        RAG Engine
(LLM-based)   (5 domains)    (FAISS + Embeddings)
│
▼
Groq LLM API

```

---

## 📂 **Project Structure**

```

AI_Chatbot_using_LLMs/
│
├── src/
│   ├── api/
│   │   ├── server.py
│   │   ├── upload.py
│   │   ├── deps.py
│   │   └── schemas.py
│   │
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── education_agent.py
│   │   ├── coding_agent.py
│   │   ├── medical_agent.py
│   │   ├── legal_agent.py
│   │   ├── general_agent.py
│   │   └── prompts/
│   │
│   ├── rag/
│   │   ├── rag_pipeline.py
│   │   ├── loader.py
│   │   └── embedder.py
│   │
│   ├── router/
│   │   └── domain_router.py
│   │
│   ├── models/
│   │   └── llm.py
│   │
│   ├── utils/
│   │   └── context_manager.py
│   │
│   └── main.py
│
├── frontend/
│   ├── app.py
│   └── static/style.css
│
├── requirements.txt
└── README.md

````

---

# ⚙️ **Setup Instructions (Local Development)**

## 1️⃣ **Clone the Repository**
```bash
git clone <your repo link>
cd AI_Chatbot_using_LLMs
````

---

# 🔐 2️⃣ Create Environment Variables (`.env`)

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama3-groq-8b-tool-use-preview
```

---

# 🐍 3️⃣ Backend Setup (FastAPI)

### Create Conda environment:

```bash
conda create -n llm_backend python=3.10
conda activate llm_backend
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Start backend:

```bash
uvicorn src.api.server:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Test endpoint:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","message":"hello"}'
```

---

# 🖥️ 4️⃣ Frontend Setup (Streamlit)

Navigate to frontend:

```bash
cd frontend
streamlit run app.py
```

Frontend runs at:

```
http://localhost:8501
```

---

## 🧪 **API Endpoints**

### POST `/chat`

```
{
  "session_id": "123",
  "message": "Explain OOP"
}
```

### POST `/upload`

Upload PDFs or text for RAG.

### WebSocket `/stream`

For token streaming responses.

---

## 🚀 Deployment Guide

### Deploy Backend:

* Render
* Railway
* Azure App Service
* AWS EC2
* Docker container

### Deploy Frontend:

* Streamlit Community Cloud
* Docker container
* CloudRun

---

## 🤝 Contributing

Pull requests are welcome.
For major changes, open an issue first to discuss the proposal.

---

## 📄 License

MIT License (or your choice)

---

## ⭐ Support This Project

If this project helped you, consider giving a **star** ⭐ on GitHub!
