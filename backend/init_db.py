# backend/init_db.py

from db.database import Base, engine
from db.models import interaction  # ⬅️ import model agar dikenali SQLAlchemy

print("📦 Membuat struktur tabel di smartfinance.db...")
Base.metadata.create_all(bind=engine)
print("✅ Tabel berhasil dibuat.")
