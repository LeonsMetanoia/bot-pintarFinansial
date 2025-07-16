# backend/services/llm_service.py

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import logging

# Inisialisasi logger
logger = logging.getLogger(__name__)

# 1. Inisialisasi LLM lokal (pastikan `ollama run mistral` sedang berjalan)
llm = Ollama(model="mistral")

# 2. Inisialisasi model embedding lokal (gratis, tidak butuh API key)
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 3. Fungsi membuat query engine dengan LLM + embedding lokal
def get_query_engine():
    try:
        docs = SimpleDirectoryReader("data/crypto-docs").load_data()
        index = VectorStoreIndex.from_documents(docs, embed_model=embed_model)
        query_engine = index.as_query_engine(llm=llm)
        logger.info("✅ Query engine berhasil dibuat.")
        return query_engine
    except Exception as e:
        logger.error(f"❌ Gagal membuat query engine: {e}")
        raise

# 4. Inisialisasi query engine saat aplikasi start
query_engine = get_query_engine()

# 5. Fungsi untuk memproses pertanyaan
def get_llm_response(question: str) -> str:
    try:
        response = query_engine.query(question)
        return str(response)
    except Exception as e:
        logger.error(f"❌ Error saat menjawab pertanyaan: {e}")
        return f"Terjadi error saat menjawab pertanyaan: {e}"
