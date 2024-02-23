from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from server.utils.get_coin_price import  fetch_and_save_coin_prices
from server.router import auth
from server.router import market_router, log_router

app = FastAPI()

scheduler = AsyncIOScheduler()
scheduler.start()
scheduler.add_job(fetch_and_save_coin_prices, 'interval', minutes=1)

app.include_router(auth.router)
app.include_router(market_router.router, prefix="/market", tags=["market"])
app.include_router(log_router.router, tags=["log"])