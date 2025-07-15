from sqlalchemy.orm import Session
from db.models.interaction import Interaction
from sqlalchemy.exc import SQLAlchemyError

def save_interaction(
    db: Session,
    sender_username: str,
    message: str,
    response: str,
    message_id: str
):
    """
    Menyimpan interaksi user ke database.
    """
    try:
        interaction = Interaction(
            sender_username=sender_username,
            message=message,
            response=response,
            message_id=message_id
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        print(f"💾 Disimpan ke DB: @{sender_username} - {message}")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"❌ Gagal menyimpan interaksi ke DB: {e}")

def is_message_already_processed(db: Session, message_id: str) -> bool:
    """
    Mengecek apakah pesan dengan ID ini sudah pernah diproses sebelumnya.
    """
    interaction = db.query(Interaction).filter(Interaction.message_id == message_id).first()
    if interaction:
        print(f"🔁 Pesan sudah pernah diproses: {message_id}")
        return True
    return False
