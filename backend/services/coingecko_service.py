import requests

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

def get_crypto_price(coin_id: str, vs_currency: str = "usd") -> float:
    url = f"{COINGECKO_API_URL}/simple/price"
    params = {
        "ids": coin_id.lower(),
        "vs_currencies": vs_currency.lower()
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get(coin_id, {}).get(vs_currency)
    else:
        print(f"❌ Gagal mengambil harga dari CoinGecko: {response.status_code}")
        return None
