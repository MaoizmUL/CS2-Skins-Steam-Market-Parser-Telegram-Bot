import re
from entities import Item
from urllib.parse import quote
from market_fetcher import fetch_market_listings, fetch_float_value

def process_skin_data(protocol: str, proxy_list, skin_name: str, stickers_cache, charms_cache, items_cache, collected_items):
    market_data = fetch_market_listings(protocol, proxy_list, skin_name)
    listing_info = market_data.get("listinginfo", {})
    assets = market_data.get("assets", {}).get("730", {}).get("2", {})

    item_prices = {info.get("asset", {}).get("id"): round((float(info.get("converted_price", 0)) / 100) * 1.1499, 2) for info in
                   listing_info.values()}

    for asset_id, asset_data in assets.items():
        item_id = asset_data.get("id")
        if item_id in items_cache:
            continue

        price = item_prices.get(item_id, 0)
        inspect_link = asset_data.get("market_actions", [{}])[0].get("link", "").replace("%assetid%", str(item_id))
        inspect_link = quote(inspect_link, safe="")

        item = Item(item_id, skin_name, price, inspect_link)
        print(f"Processing item {item.id}: {item.market_hash_name} at {item.price}")

        for description in asset_data.get("descriptions", []):
            if description.get("name") == "sticker_info":
                stickers = re.findall(r'title="Sticker: (.*?)"', description.get("value", ""))
                item.add_stickers(protocol, proxy_list, stickers, stickers_cache)
            elif description.get("name") == "keychain_info":
                charm_match = re.findall(r'title="Charm: (.*?)"', description.get("value", ""))
                if charm_match:
                    item.add_charm(protocol, proxy_list, charm_match[0], charms_cache)

        if item.stickers:
            sticker_filter = " ".join(f"Sticker | {s.market_hash_name} " for s in item.stickers)
            item.market_link = f"https://steamcommunity.com/market/listings/730/{quote(item.market_hash_name, safe='')}?filter={quote(sticker_filter, safe='')}"

            collected_items.append(item)
            item.float = fetch_float_value(protocol, proxy_list, item.inspect_link)
            item.display()

        if item.charm:
            item.market_link += f" Charm | {item.charm.market_hash_name}"

        items_cache[item_id] = skin_name