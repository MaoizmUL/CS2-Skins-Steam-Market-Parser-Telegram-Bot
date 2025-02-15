import time
import random
import requests
from urllib.parse import quote
from fake_useragent import UserAgent
from requests.exceptions import ReadTimeout

def fetch_proxy_list(proxy_list, protocol="http", limit = 250, max_attempts = 5):
    url = f"https://proxylist.geonode.com/api/proxy-list?protocols={protocol}&limit={limit}&page=1&sort_by=lastChecked&sort_type=desc"
    headers = {"User-Agent": UserAgent().random}

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                proxies = response.json().get("data", [])
                for proxy in proxies:
                    proxy_address = f"{protocol}://{proxy.get('ip')}:{proxy.get('port')}"
                    proxy_list.append(proxy_address)

                print(f"Retrieved {len(proxy_list)} proxies.")
                return protocol

            elif response.status_code in [401, 403]:
                print(f"Access denied (HTTP {response.status_code}). Check API requirements.")
                return

            else:
                print(f"Unexpected error: HTTP {response.status_code}. Retrying...")

        except requests.exceptions.ReadTimeout:
            print(f"Request timed out. Retrying ({attempt}/{max_attempts})...")

        time.sleep(3)

    print("Max attempts reached. Failed to fetch proxies.")

def fetch_market_listings(protocol:str, proxy_list, skin_name:str):
    url = f"https://steamcommunity.com/market/listings/730/{quote(skin_name)}/render/?query=&start=0&count=10&country=RU&language=english&currency=5"
    headers = {"User-Agent": UserAgent().random}

    while True:
        proxy = {protocol: random.choice(proxy_list)}
        print(f"Current proxy: {proxy}")
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("Received 429 Too Many Requests. Switching proxy...")
            else:
                print(f"Failed to fetch market listings: {response.status_code}. Retrying...")

        except ReadTimeout:
            print("Request timed out. Retrying with a different proxy...")

        time.sleep(5)

def fetch_float_value(protocol:str, proxy_list, inspect_link:str, max_attempts=5):
    url = f"https://tradeit.gg/api/steam/v1/steams/float-item-finder?inspectLink={inspect_link}"
    headers = {"User-Agent": UserAgent().random}

    for attempt in range(max_attempts):
        proxy = {protocol: random.choice(proxy_list)}
        print(f"Current proxy: {proxy}")
        try:
            print(f"Attempt {attempt + 1}: Fetching float value for {inspect_link}")
            response = requests.get(url, headers=headers, proxies=proxy, timeout=20)

            if response.status_code == 200:
                return response.json().get("paintwear")
            print(f"Failed to get float value: {response.status_code}. Retrying...")
        except ReadTimeout:
            print("ReadTimeout occurred. Retrying...")
        time.sleep(5)

    print("Max attempts reached. Could not fetch float value.")
    return None