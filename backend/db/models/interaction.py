from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.database import Base

class Interaction(Base):
    __tablename__ = 'interactions'

    id = Column(Integer, primary_key=True, index=True)
    sender_username = Column(String)
    message = Column(String)
    response = Column(String)
    message_id = Column(String, unique=True, index=True)  # ✅ Kolom baru
    timestamp = Column(DateTime, default=datetime.utcnow)
