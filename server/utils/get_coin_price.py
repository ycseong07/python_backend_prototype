import requests
from server.database.database import SessionLocal
from server.crud.market_crud import save_coin_prices

def get_coin_prices():
    markets = "KRW-BTC,KRW-ETH,KRW-XRP"
    url = f"https://api.upbit.com/v1/ticker?markets={markets}"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_and_save_coin_prices():
    coin_prices = get_coin_prices()
    db = SessionLocal()
    try:
        save_coin_prices(db, coin_prices)
    finally:
        db.close()