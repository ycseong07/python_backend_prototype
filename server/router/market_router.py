from fastapi import APIRouter
from server.utils.get_coin_price import get_coin_prices

router = APIRouter()

@router.get("/coin-prices")
async def coin_prices():
    return get_coin_prices()