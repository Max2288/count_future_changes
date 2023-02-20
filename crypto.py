import time
import pandas as pd
from binance.client import Client
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
FUTURE = 'ETHUSDT'
PERIOD = 60


client = Client(API_KEY, API_SECRET)


def get_futures_price(symbol: str) -> float:
    """Get future price.

    Args:
        symbol (str): future's name.

    Returns:
        float: it's price.
    """
    futures_price = client.futures_mark_price(symbol=symbol)
    return float(futures_price['markPrice'])


def calculate_ema(prices: List[float], n: int) -> float:
    """Calculating an exponential moving average of a futures price.

    Args:
        prices (List[float]): list with prices.
        n (int): number of periods.

    Returns:
        float: EMA.
    """
    return pd.Series(prices).ewm(span=n, min_periods=n).mean().iloc[-1]


def main() -> None:
    """Сounts the price change."""    
    while True:
        price = get_futures_price(FUTURE)
        prices = [get_futures_price(FUTURE) for _ in range(PERIOD)]
        ema = calculate_ema(prices, PERIOD)
        change = (price - ema) / ema
        print(change)
        if abs(change) > 0.01:
            direction = "вверх" if change > 0 else "вниз"
            print(
                f"Цена ETHUSDT изменилась на {change:.2%} {direction} за последние 60 минут.")
        time.sleep(10)


if __name__ == '__main__':
    main()
