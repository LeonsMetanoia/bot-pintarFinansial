from db.database import Base, engine
from db.models.interaction import Interaction

print("🔧 Creating tables in smartfinance.db...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created.")
