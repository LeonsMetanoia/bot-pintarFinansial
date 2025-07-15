from instagrapi import Client
import os
import pickle
from dotenv import load_dotenv
from instagrapi.exceptions import ChallengeRequired
from db.database import SessionLocal
from db.crud.interaction import save_interaction, is_message_already_processed
from datetime import datetime
from services.coingecko_service import get_crypto_price as get_crypto_price_api

# Load environment variables
load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
SESSION_FILE = f"{USERNAME}_session.json"

cl = Client()

# Map coin keywords to CoinGecko IDs
COIN_KEYWORDS = {
    "bitcoin": "bitcoin",
    "eth": "ethereum",
    "ethereum": "ethereum",
    "doge": "dogecoin",
    "sol": "solana",
    "bnb": "binancecoin"
}


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
    coin_id = COIN_KEYWORDS.get(coin_name.lower())
    if coin_id:
        return get_crypto_price_api(coin_id)
    return None


def generate_bot_response(text: str) -> str:
    text = text.lower()
    triggered_coin = None

    for keyword in COIN_KEYWORDS.keys():
        if keyword in text:
            triggered_coin = keyword
            break

    if triggered_coin:
        price = get_crypto_price(triggered_coin)
        if price is not None:
            return f"Harga {triggered_coin.capitalize()} saat ini: ${price:,.2f}"
        else:
            return f"Maaf, harga {triggered_coin} tidak tersedia saat ini."
    else:
        return "Maaf, saya belum mengerti pertanyaanmu. Coba sebutkan nama coin seperti 'bitcoin', 'eth', 'doge', dll."


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
                    text = message.text
                    username = cl.user_info(sender_id).username
                except Exception as e:
                    print(f"❌ Gagal ambil pengirim: {e}")
                    continue

                response_msg = generate_bot_response(text)

                try:
                    cl.direct_send(response_msg, [sender_id])
                    print(f"📨 DM dari @{username}: {text}")
                    print(f"🤖 Bot membalas: {response_msg}")

                    save_interaction(
                        db=db,
                        sender_username=username,
                        message=text,
                        response=response_msg,
                        message_id=message_id
                    )
                except Exception as e:
                    print(f"❌ Gagal kirim ke @{username}: {e}")

    finally:
        db.close()


def simulate_bot_response(message_text: str, sender_username: str = "tester") -> str:
    message_id = f"sim_{datetime.utcnow().timestamp()}"
    response_msg = generate_bot_response(message_text)

    db = SessionLocal()
    try:
        save_interaction(
            db=db,
            sender_username=sender_username,
            message=message_text,
            response=response_msg,
            message_id=message_id
        )
    finally:
        db.close()

    print(f"[SIMULASI] DM: {message_text}")
    print(f"[SIMULASI] Respon: {response_msg}")

    return response_msg
