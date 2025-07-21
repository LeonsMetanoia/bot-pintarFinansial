from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader

import chromadb
import os

persist_dir = "./chroma_db"

# Inisialisasi komponen
llm = Ollama(model="mistral")
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

# Set default settings secara global
Settings.llm = llm
Settings.embed_model = embed_model
Settings.node_parser = text_splitter

# Fungsi untuk get_query_engine
def get_query_engine():
    try:
        # Load dokumen dari direktori
        docs = SimpleDirectoryReader("data/docs-bot").load_data()
        print(f"📄 Jumlah dokumen dibaca: {len(docs)}")

        # Tampilkan 3 contoh dokumen pertama
        for i, doc in enumerate(docs[:3]):
            print(f"\n📘 Dokumen #{i+1}")
            print(f"➡️ Nama file asal: {doc.metadata.get('file_name', 'Tidak diketahui')}")
            print(f"📝 Cuplikan isi: {doc.text[:200]}...")

        # Setup Chroma dan Storage Context
        db = chromadb.PersistentClient(path=persist_dir)
        chroma_store = ChromaVectorStore(chroma_collection=db.get_or_create_collection("finance_bot"))

        # Buat index dari dokumen
        index = VectorStoreIndex.from_documents(
            documents=docs,
            vector_store=chroma_store,
        )

        # Kembalikan query engine
        return index.as_query_engine()

    except Exception as e:
        print(f"❌ Error creating query engine: {e}")
        raise

# Fungsi utama untuk digunakan dari luar
def get_llm_response(query: str) -> str:
    engine = get_query_engine()
    response = engine.query(query)
    return str(response)
