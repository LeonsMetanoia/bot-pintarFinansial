from sqlalchemy.orm import Session
from db.models.interaction import Interaction

def save_interaction(
    db: Session,
    sender_username: str,
    message: str,
    response: str,
    message_id: str
):
    interaction = Interaction(
        sender_username=sender_username,
        message=message,
        response=response,
        message_id=message_id
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)

def is_message_already_processed(db: Session, message_id: str) -> bool:
    return db.query(Interaction).filter(Interaction.message_id == message_id).first() is not None
