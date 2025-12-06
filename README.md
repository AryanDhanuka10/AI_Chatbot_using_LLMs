Understood — your directory structure has **changed completely**, and your **frontend is now React**, NOT Streamlit.

Your old README is now **incorrect**, **misleading**, and references components you no longer use.

So here is a **fully corrected, clean, formatted, React-compatible README.md**, designed exactly for your **current project structure**.

---

# ✅ **FINAL README.md FOR YOUR PROJECT — FULLY UPDATED FOR REACT + FASTAPI + RAG**

## ✔ Matches your directory structure

## ✔ Mentions all technologies you ACTUALLY use now

## ✔ Professional, deploy-ready, corporate style

## ✔ Clean formatting + image fixed

## ✔ No Streamlit, No outdated components

## ✔ Ready for GitHub

---

# 📘 **AI Chatbot Using LLMs — Multi-Domain Intelligent Assistant**

<p align="center">
  <img src="https://cdn.pixabay.com/photo/2023/03/21/14/40/ai-7868011_1280.jpg" alt="AI Chatbot Banner" width="720">
</p>

A full-stack **LLM-powered AI Chatbot** built with a modern architecture:

* 🧠 **Groq LLMs (Llama-3.1)**
* ⚡ **FastAPI Backend**
* 💻 **React Frontend (Vite)**
* 🔍 **RAG (Retrieval-Augmented Generation)**
* 🧩 **Modular Multi-Agent System**
* 🔒 **Safe Domain-Restricted Prompts**

This system supports **5 intelligent domains**:

* 🎓 Education
* 💻 Coding
* ⚕️ Medical (Safe explanations only)
* ⚖️ Legal (Non-advisory)
* 💬 General conversation

---

# 🌐 **Live Deployment**

👉 **Deployed Link:** [(https://ai-chatbot-using-ll-ms.vercel.app/)]


# 🎯 **Key Features**

### 🧠 **1. Domain-Aware Multi-Agent System**

The Domain Router classifies every query into one of:

| Domain    | Purpose                                     |
| --------- | ------------------------------------------- |
| Education | Concepts, theory, step-by-step explanations |
| Coding    | Debugging, optimization, code generation    |
| Medical   | Safe educational medical explanations       |
| Legal     | Educational legal descriptions              |
| General   | General conversation, reasoning             |

Each agent has its own **expert prompt template** optimized for structured, high-quality responses.

---

### 📚 **2. RAG Pipeline (PDF/TXT Upload + FAISS Retrieval)**

Your backend supports:

* PDF/TXT ingestion
* Chunking
* Embedding using **all-MiniLM-L6-v2**
* FAISS vector indexing
* Top-K retrieval for relevant context

---

### 💻 **3. Modern React Frontend**

Your frontend (in `/frontend/src/`) includes:

* **Animated chat messages**
* **Typing animation for AI**
* **Timestamps**
* **Chat history export**
* **Sliding sidebar**
* **Domain highlighting**
* **File upload for RAG**
* **Smooth scroll-to-bottom**
* **Toast notifications**

---

### ⚡ **4. FastAPI Backend**

Endpoints:

| Method | Endpoint  | Function              |
| ------ | --------- | --------------------- |
| POST   | `/chat`   | Main REST chat        |
| POST   | `/upload` | Add documents for RAG |
| GET    | `/health` | Health check          |
| WS     | `/stream` | Token streaming       |

---

### 🧩 **5. Clean Modular Architecture**

* Agents
* Prompt templates
* RAG pipeline
* Domain routing
* LLM wrapper
* Context memory

Everything extendable & replaceable.

---

# 📦 **Tech Stack**

### **Frontend**

* React
* Vite
* Axios
* Tailwind (optional)

### **Backend**

* FastAPI
* Groq API (Llama-3.1-70B / 8B)
* Sentence Transformers
* FAISS CPU
* PyPDF2

---

# 📂 **Project Structure**

```
aryandhanuka10-ai_chatbot_using_llms/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── template.py
├── .dockerignore
├── .env.example
│
├── config/
│   └── settings.py
│
├── frontend/
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── components/
│       │   ├── ChatArea.jsx
│       │   ├── InputArea.jsx
│       │   ├── Sidebar.jsx
│       │   └── Toast.jsx
│
└── src/
    ├── main.py
    ├── api/
    │   ├── server.py
    │   ├── upload.py
    │   ├── deps.py
    │   └── schemas.py
    │
    ├── agents/
    │   ├── base_agent.py
    │   ├── coding_agent.py
    │   ├── education_agent.py
    │   ├── general_agent.py
    │   ├── legal_agent.py
    │   ├── medical_agent.py
    │   └── prompts/
    │       ├── base_prompt.py
    │       ├── coding_prompt.py
    │       ├── education_prompt.py
    │       ├── general_prompt.py
    │       ├── legal_prompt.py
    │       └── medical_prompt.py
    │
    ├── rag/
    │   ├── loader.py
    │   ├── vectorstore.py
    │   ├── embedder.py
    │   ├── retriever.py
    │   └── rag_pipeline.py
    │
    ├── models/
    │   └── llm.py
    │
    ├── router/
    │   └── domain_router.py
    │
    └── utils/
        └── context_manager.py
```

---

# 🛠️ **Setup Instructions**

## 1️⃣ Clone the repository

```bash
git clone https://github.com/aryandhanuka10/ai_chatbot_using_llms.git
cd ai_chatbot_using_llms
```

---

# ⚙️ Backend Setup

## 2️⃣ Create environment

```bash
conda create -n llm_backend python=3.10 -y
conda activate llm_backend
```

## 3️⃣ Install backend dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Create `.env` file

```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile   # recommended
```

## 5️⃣ Start backend

```bash
uvicorn src.api.server:app --reload
```

Backend → [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

# 💻 Frontend Setup

Navigate to frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend → [http://localhost:5173](http://localhost:5173)

---

# 📤 API Example

### Request:

```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id":"test","message":"Explain binary search"}'
```

---

# 🧪 RAG Usage

Upload PDFs/TXT from the frontend sidebar → backend indexes them → responses include retrieved knowledge.

---

# 📄 License

MIT License © 2025 — Aryan Dhanuka

---

# ⭐ Support

If this project helped you, please ⭐ the repository.

