from instagrapi import Client
import os
import pickle
from dotenv import load_dotenv
from instagrapi.exceptions import ChallengeRequired
from db.database import SessionLocal
from db.crud.interaction import save_interaction, is_message_already_processed
from datetime import datetime

# Load .env
load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
SESSION_FILE = f"{USERNAME}_session.json"

cl = Client()

def login_if_needed():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "rb") as f:
                session = pickle.load(f)
                cl.set_settings(session)
                cl.login(USERNAME, PASSWORD)
        else:
            cl.login(USERNAME, PASSWORD)
            with open(SESSION_FILE, "wb") as f:
                pickle.dump(cl.get_settings(), f)
        print(f"✅ Login berhasil sebagai @{cl.username}")
    except ChallengeRequired:
        print("❌ ChallengeRequired: Verifikasi diperlukan.")
        raise
    except Exception as e:
        print(f"❌ Login gagal: {str(e)}")
        raise

def get_crypto_price(coin_name: str):
    if coin_name.lower() == "bitcoin":
        return 69000.00
    return None

def check_and_respond_to_dm():
    login_if_needed()
    db = SessionLocal()

    try:
        threads = cl.direct_threads(amount=10)

        for thread in threads:
            for message in reversed(thread.messages):  # proses dari lama ke baru
                if not message.text:
                    continue

                message_id = str(message.id)
                if is_message_already_processed(db, message_id):
                    continue

                try:
                    sender_id = message.user_id
                    text = message.text.lower()
                    username = cl.user_info(sender_id).username
                except Exception as e:
                    print(f"❌ Gagal ambil pengirim: {e}")
                    continue

                if "bitcoin" in text:
                    price = get_crypto_price("bitcoin")
                    if price:
                        msg = f"Harga Bitcoin saat ini: ${price:,.2f}"
                        try:
                            cl.direct_send(msg, [sender_id])
                            print(f"📨 DM dari @{username}: {text}")
                            print(f"🤖 Bot membalas: {msg}")

                            save_interaction(
                                db=db,
                                sender_username=username,
                                message=text,
                                response=msg,
                                message_id=message_id
                            )
                        except Exception as e:
                            print(f"❌ Gagal kirim ke @{username}: {e}")
    finally:
        db.close()
