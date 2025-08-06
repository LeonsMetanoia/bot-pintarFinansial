# 🤖 Bot PintarFinansial

**Bot PintarFinansial** is an intelligent chatbot system designed to educate users on financial topics. It integrates seamlessly with Instagram Direct Messages (DM) using [Instagrapi](https://github.com/adw0rd/instagrapi), and answers user questions based on a collection of finance-related documents using Retrieval-Augmented Generation (RAG).

---

## 🧠 Features

- **RAG-based Financial Knowledge Bot**: Uses the LlamaIndex framework to retrieve information from indexed documents and generate responses.
- **Local LLM Deployment**: Runs a local AI model (`Mistral 7B`) using [Ollama](https://ollama.com/) for private, fast, and secure inference.
- **Instagram DM Integration**: Automatically responds to user questions sent to your Instagram account via Instagrapi.
- **FastAPI Backend**: Backend server developed using [FastAPI](https://fastapi.tiangolo.com/) for efficient API handling and chatbot logic.
- **In-memory Caching with Redis**: Previously asked questions are cached using [Redis](https://redis.io/) for faster responses and reduced processing.
- **Document Chunking with ChromaDB**: Stores and manages PDF/document chunks in a vector database using [ChromaDB](https://www.trychroma.com/).
- **SQLite Relational Database**: Stores structured data and conversation logs using SQLite.
- **Planned React Frontend**: A web interface is planned using React for an alternative frontend user experience.

---

## ⚙️ Tech Stack

| Component               | Technology         |
|------------------------|--------------------|
| Programming Language   | Python             |
| AI Model               | Mistral 7B (via Ollama) |
| Retrieval Framework    | LlamaIndex         |
| Vector Store           | ChromaDB           |
| Relational Database    | SQLite             |
| Caching                | Redis              |
| API Framework          | FastAPI            |
| Social Media Bot       | Instagrapi (Instagram DM) |
| Frontend (Planned)     | React              |

---

## 🛠️ Setup Instructions

> _Detailed setup instructions coming soon. Please stay tuned._

---

## 🚀 Future Plans

- Develop an interactive web frontend using React
- Improve question rephrasing and follow-up handling
- Add admin dashboard for document upload and analytics

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

- [Ollama](https://ollama.com/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [ChromaDB](https://www.trychroma.com/)
- [Instagrapi](https://github.com/adw0rd/instagrapi)
- [FastAPI](https://fastapi.tiangolo.com/)
