from fastapi import FastAPI
from pydantic import BaseModel
import MetaTrader5 as mt5

app = FastAPI()

# --------------------------------------------------
# MT5 Login Config (YOU WILL ADD YOUR VALUES IN RENDER)
# --------------------------------------------------
ACCOUNT = None
PASSWORD = None
SERVER = None


def connect_mt5():
    if not mt5.initialize():
        return False

    if ACCOUNT and PASSWORD and SERVER:
        login_result = mt5.login(ACCOUNT, PASSWORD, SERVER)
        return login_result
    return False


class Order(BaseModel):
    symbol: str
    volume: float
    sl: float | None = None
    tp: float | None = None


@app.post("/buy")
def buy(order: Order):
    connect_mt5()
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": order.symbol,
        "volume": order.volume,
        "type": mt5.ORDER_TYPE_BUY,
        "sl": order.sl,
        "tp": order.tp,
        "magic": 10001,
        "deviation": 20
    }
    result = mt5.order_send(request)
    return {"result": result._asdict()}


@app.post("/sell")
def sell(order: Order):
    connect_mt5()
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": order.symbol,
        "volume": order.volume,
        "type": mt5.ORDER_TYPE_SELL,
        "sl": order.sl,
        "tp": order.tp,
        "magic": 10001,
        "deviation": 20
    }
    result = mt5.order_send(request)
    return {"result": result._asdict()}


@app.get("/positions")
def get_positions():
    connect_mt5()
    positions = mt5.positions_get()
    if positions is None:
        return {"positions": []}
    return {"positions": [p._asdict() for p in positions]}


@app.get("/info")
def info():
    connect_mt5()
    acc_info = mt5.account_info()
    return acc_info._asdict() if acc_info else {"error": "Not connected"}
