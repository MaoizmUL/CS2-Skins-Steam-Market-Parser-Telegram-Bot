from typing import List, Optional, Dict
from .market_item import Sticker, Charm

class Item:
    def __init__(self, id_: str, market_hash_name: str, price: float, inspect_link: str):
        self.__id = id_
        self.__market_hash_name = market_hash_name
        self.__price = price
        self.__stickers: List[Sticker] = []
        self.__charm: Optional[Charm] = None
        self.__float: str = ""
        self.__inspect_link = inspect_link
        self.__market_link: str = ""

    @property
    def id(self) -> str:
        return self.__id

    @property
    def market_hash_name(self) -> str:
        return self.__market_hash_name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stickers(self) -> List[Sticker]:
        return self.__stickers

    @stickers.setter
    def stickers(self, stickers: List[Sticker]):
        self.__stickers = stickers

    @property
    def charm(self) -> Optional[Charm]:
        return self.__charm

    @charm.setter
    def charm(self, charm: Optional[Charm]):
        self.__charm = charm

    @property
    def float(self):
        return self.__float

    @float.setter
    def float(self, item_float: str):
        self.__float = item_float

    @property
    def inspect_link(self):
        return self.__inspect_link

    @inspect_link.setter
    def inspect_link(self, inspect_link: str):
        self.__inspect_link = inspect_link

    @property
    def market_link(self):
        return self.__market_link

    @market_link.setter
    def market_link(self, market_link: str):
        self.__market_link = market_link

    def add_stickers(self, protocol: str, proxy_list, sticker_names: List[str], cache: Dict[str, Optional[float]]):
        for sticker_name in sticker_names:
            self.stickers.append(Sticker(sticker_name))

        for sticker in self.stickers:
            sticker.get_price(protocol, proxy_list, "Sticker", cache)

    def add_charm(self, protocol:str, proxy_list, charm_name: str, cache: Dict[str, Optional[float]]):
        self.charm = Charm(charm_name)
        self.charm.get_price(protocol, proxy_list, "Charm", cache)

    def display(self):
        print(f"{self.market_hash_name}\nassetid: {self.id}\nprice: {self.price}\nFloat: {self.float}")
        if self.stickers:
            print("Stickers:")
            for sticker in self.stickers:
                print(f"\t{sticker.market_hash_name} -> {sticker.price}")
        if self.charm:
            print("Charm:")
            print(f"\t{self.charm.market_hash_name} -> {self.charm.price}")
        print(f"Market URL: {self.market_link}")