from sqlalchemy.orm import Session
from server.models.market_models import MarketPrice
from datetime import datetime

def save_coin_prices(db: Session, coin_prices: list):
    for price_info in coin_prices:
        db_price = MarketPrice(
            market=price_info['market'],
            opening_price=price_info['opening_price'],
            high_price=price_info['high_price'],
            low_price=price_info['low_price'],
            trade_price=price_info['trade_price'],
            prev_closing_price=price_info['prev_closing_price'],
            timestamp=datetime.fromtimestamp(price_info['trade_timestamp'] / 1000)
        )
        db.add(db_price)
    db.commit()