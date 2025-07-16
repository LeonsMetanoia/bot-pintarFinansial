from instagrapi import Client
import os
import pickle
from dotenv import load_dotenv
from instagrapi.exceptions import ChallengeRequired
from db.database import SessionLocal
from db.crud.interaction import save_interaction, is_message_already_processed
from datetime import datetime
from services.coingecko_service import get_crypto_price as get_crypto_price_api
from services.redis_service import get_cached_price, set_cached_price
from services.llm_service import get_llm_response  # LLM via LlamaIndex + Ollama

# Load environment variables
load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
SESSION_FILE = f"{USERNAME}_session.json"

cl = Client()

# Keyword to CoinGecko ID mapping
COIN_KEYWORDS = {
    "bitcoin": "bitcoin",
    "btc": "bitcoin",
    "eth": "ethereum",
    "ethereum": "ethereum",
    "doge": "dogecoin",
    "sol": "solana",
    "solana": "solana",
    "bnb": "binancecoin",
    "xrp": "xrp",
    "trx": "tron"
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
        cached_price = get_cached_price(coin_id)
        if cached_price:
            print(f"💾 Ambil dari Redis: {coin_id} = ${cached_price}")
            return float(cached_price)
        try:
            price = get_crypto_price_api(coin_id)
            set_cached_price(coin_id, price)
            print(f"🌐 Ambil dari CoinGecko dan simpan ke Redis: {coin_id} = ${price}")
            return price
        except Exception as e:
            print(f"❌ Gagal mengambil harga dari CoinGecko: {e}")
    return None

def generate_bot_response(text: str) -> str:
    text = text.lower().strip()

    # Step 1: Cari apakah cocok dengan coin
    for keyword in COIN_KEYWORDS.keys():
        if keyword in text:
            price = get_crypto_price(keyword)
            if price is not None:
                return f"Harga {keyword.capitalize()} saat ini: ${price:,.2f}"
            else:
                return f"Maaf, harga {keyword} tidak tersedia saat ini."

    # Step 2: Jika tidak cocok → tanya ke LLM
    print("🧠 Pertanyaan dikirim ke LLM...")
    llm_answer = get_llm_response(text)
    return llm_answer

def check_and_respond_to_dm():
    login_if_needed()
    db = SessionLocal()

    try:
        threads = cl.direct_threads(amount=10)

        for thread in threads:
            if not thread.messages:
                continue

            for message in reversed(thread.messages):
                if not message.text:
                    continue

                message_id = str(message.id)
                if is_message_already_processed(db, message_id):
                    print(f"🔁 Pesan sudah pernah diproses: {message_id}")
                    continue

                text = message.text.strip()
                sender_id = message.user_id

                try:
                    username = getattr(message.user, "username", None)
                    if not username:
                        username = f"id_{sender_id}"
                except Exception as e:
                    print(f"❌ Gagal ambil username: {e}")
                    username = f"id_{sender_id}"

                print(f"📨 DM dari @{username}: {text}")
                response_msg = generate_bot_response(text)

                try:
                    cl.direct_send(response_msg, [sender_id])
                    print(f"🤖 Bot membalas: {response_msg}")

                    save_interaction(
                        db=db,
                        sender_username=username,
                        message=text,
                        response=response_msg,
                        message_id=message_id
                    )
                    print(f"💾 Disimpan ke DB: @{username} - {text}")
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
