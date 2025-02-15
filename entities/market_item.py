import time
import random
import requests
from requests import ReadTimeout
from typing import Dict, Optional
from fake_useragent import UserAgent


class MarketItem:
    def __init__(self, market_hash_name: str):
        self.__market_hash_name = market_hash_name
        self.__price: Optional[float] = None

    @property
    def market_hash_name(self) -> str:
        return self.__market_hash_name

    @market_hash_name.setter
    def market_hash_name(self, market_hash_name: str):
        self.__market_hash_name = market_hash_name

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, price: float):
        self.__price = price

    def get_price(self, protocol:str, proxy_list, category: str, cache: Dict[str, Optional[float]]) -> None:
        if self.market_hash_name in cache:
            self.price = cache[self.market_hash_name]
            return

        url = f"https://steamcommunity.com/market/listings/730/{category} | {self.market_hash_name}/render/?query=&start=0&country=EN&language=english&currency=5"
        headers = {"User-Agent": UserAgent().random}

        while True:
            proxy = {protocol: random.choice(proxy_list)}
            print(f"Proxy has been changed to: {proxy}")
            try:
                print(f"Fetching price for {self.market_hash_name}")
                response = requests.get(url, headers=headers, proxies=proxy, timeout=10)

                if response.status_code == 200:
                    listing_info = response.json().get("listinginfo", {})
                    for info_id, info_value in listing_info.items():
                        self.price = round((float(info_value.get("converted_price", 0)) / 100) * 1.149878309, 2)
                        break

                    cache[self.market_hash_name] = self.price
                    return
                elif response.status_code == 429:
                    print("Received 429 Too Many Requests. Switching proxy...")
                else:
                    print(f"Failed to fetch market listings: {response.status_code}. Retrying...")

            except ReadTimeout:
                print("Request timed out. Retrying with a different proxy...")

            time.sleep(5)

class Sticker(MarketItem):
    pass

class Charm(MarketItem):
    pass