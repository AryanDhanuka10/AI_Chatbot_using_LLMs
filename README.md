
---

# 📘 **AI Chatbot Using LLMs — Multi-Domain Intelligent Assistant**

<p align="center">
  <img src="frontend/src/assets/banner.png" alt="AI Chatbot Banner" width="720">
</p>

A full-stack **LLM-powered AI Chatbot** built with a modern, scalable architecture:

* 🧠 **OpenAI GPT-4o / GPT-3.5**
* ⚡ **FastAPI Backend**
* 💻 **React Frontend (Vite)**
* 🔍 **RAG (Retrieval-Augmented Generation)**
* 🧩 **Modular Multi-Agent System**
* 🔒 **Safe, Domain-Restricted Prompting**

This system supports **5 intelligent domains**:

* 🎓 Education
* 💻 Coding
* ⚕️ Medical (safe, non-prescriptive explanations)
* ⚖️ Legal (non-advisory explanations)
* 💬 General conversation

---

# 🌐 **Live Deployment**

👉 **🚀 [Open the Live AI Chatbot](https://ai-chatbot-using-ll-ms.vercel.app/)**

---

# 🎯 **Key Features**

## 🧠 **1. Domain-Aware Multi-Agent System**

Every query is classified into one expert domain:

| Domain    | Purpose                                     |
| --------- | ------------------------------------------- |
| Education | Theory, explanations, step-by-step learning |
| Coding    | Debugging, optimization, code generation    |
| Medical   | Safe educational medical insights           |
| Legal     | Legal concepts (educational only)           |
| General   | Normal conversation & reasoning             |

Each domain uses a **custom engineered prompt template** for structured, safe, high-quality responses.

---

## 📚 **2. RAG Pipeline (PDF/TXT Upload + FAISS Retrieval)**

Supports:

* PDF/TXT ingestion
* Text extraction
* Chunking
* Embedding via **HuggingFace SentenceTransformers (MiniLM-L6-v2)**
* FAISS vector indexing
* Top-K semantic retrieval

⭐ **Hugging Face Transformers are used for embeddings only**
Inference is done using **OpenAI GPT models**, not HF models.

---

## 💻 **3. Modern React Frontend (Vite)**

UI includes:

* ✨ Animated AI typing
* 🕒 Timestamps
* 📜 Chat history export
* 🎛️ Sliding sidebar
* 🗂️ File upload for RAG
* 🎨 Domain-colored chat bubbles
* ⬇️ Smooth auto-scroll
* 🔔 Toast notifications

Frontend lives in **`/frontend/src/`**.

---

## ⚡ **4. FastAPI Backend**

Endpoints:

| Method | Endpoint  | Description              |
| ------ | --------- | ------------------------ |
| POST   | `/chat`   | Main chat interface      |
| POST   | `/upload` | Document ingestion (RAG) |
| GET    | `/health` | Health check             |
| WS     | `/stream` | Streamed responses       |

---

## 🧩 **5. Clean Modular Architecture**

Includes:

* Agents
* Prompt templates
* RAG system
* Domain router
* OpenAI LLM wrapper
* Context manager

Everything is clean, extendable, and production-ready.

---

# 📦 **Tech Stack**

### **Frontend**

* React (Vite)
* Axios
* Tailwind (optional)

### **Backend**

* FastAPI
* **OpenAI GPT-4o / GPT-3.5** (primary LLM)
* **HuggingFace SentenceTransformers** (embedding only)
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
│           ├── ChatArea.jsx
│           ├── InputArea.jsx
│           ├── Sidebar.jsx
│           └── Toast.jsx
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

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Create `.env`

```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o   # recommended
```

## 5️⃣ Start backend

```bash
uvicorn src.api.server:app --reload
```

Backend URL:
➡ **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

# 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:
➡ **[http://localhost:5173](http://localhost:5173)**

---

# 📤 API Example

```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id":"test","message":"Explain binary search"}'
```

---

# 🧪 RAG Usage

Upload PDFs/TXT → backend indexes → GPT uses retrieved knowledge automatically.

---

# 📦 **Additional Notes**

### ✔ HuggingFace Transformers

Used **only for embedding** inside RAG:

```
sentence-transformers/all-MiniLM-L6-v2
```

### ✔ LLM Inference

Powered entirely by **OpenAI GPT-4o / GPT-3.5**.

---

# 📄 License

MIT License © 2025 — **Aryan Dhanuka**

---

# ⭐ Support

If this project helped you, please **star the repository** ⭐.

---

