from sqlalchemy import Column, Integer, String, Numeric, DateTime
from server.database.database import Base

class MarketPrice(Base):
    __tablename__ = 'price'
    __table_args__ = {'schema': 'market'}

    id = Column(Integer, primary_key=True)
    market = Column(String(20)) 
    opening_price = Column(Numeric)
    high_price = Column(Numeric)
    low_price = Column(Numeric)
    trade_price = Column(Numeric)
    prev_closing_price = Column(Numeric)
    timestamp = Column(DateTime)