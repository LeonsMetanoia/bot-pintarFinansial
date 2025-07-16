import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
try:
    REDIS_TTL = int(os.getenv("REDIS_TTL", "60").split()[0])
except ValueError:
    REDIS_TTL = 60


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

def get_cached_price(coin_id: str):
    return redis_client.get(coin_id)

def set_cached_price(coin_id: str, price: float):
    redis_client.setex(coin_id, REDIS_TTL, price)
