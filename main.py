from processing import process_skin_data
from market_fetcher import fetch_proxy_list

def main():
    print("Starting program...")
    proxy_list = []
    protocol = fetch_proxy_list(proxy_list)

    if not proxy_list:
        print("No working proxies found.")
        return

    print(f"The {protocol} protocol was chosen...")

    for proxy in proxy_list:
        print(proxy)

    skins_to_check = ["AK-47 | Elite Build (Well-Worn)", "AK-47 | Safari Mesh (Field-Tested)", "AK-47 | Elite Build (Field-Tested)", "AK-47 | Slate (Field-Tested)"]
    collected_items = []

    items_cache, stickers_cache, charms_cache = {}, {}, {}

    while True:
        for skin in skins_to_check:
            process_skin_data(protocol, proxy_list, skin, stickers_cache, charms_cache, items_cache, collected_items)

if __name__ == "__main__":
    main()