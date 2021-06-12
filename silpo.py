import requests
import json
from pprint import pprint


class Silpo:

    def __init__(self):
        self.category = {'Fruits and Veg': 374, 'Alcohol': 22}
        self.headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.77 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://shop.silpo.ua',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://shop.silpo.ua/',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
        }

        self.request_payload = {"method": "GetSimpleCatalogItems",
                                "data": {
                                    "basketGuid": "5b3333c5-f563-490e-b6db-4595746bdd56",
                                    "deliveryType": 1,
                                    "filialId": 1990,
                                    "From": 1,
                                    "businessId": 1,
                                    "To": 30000,
                                    "ingredients": False,
                                    "categoryId": None,
                                    "RangeFilters": {},
                                    "MultiFilters": {},
                                    "UniversalFilters": [],
                                    "CategoryFilter": [],
                                    "Promos": []}}

    def set_payload_to_category(self, category):
        self.request_payload['data']["categoryId"] = self.category[category]

    def get_items_json_by_category(self, category):
        self.set_payload_to_category(category)

        response = requests.post('https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal',
                                 headers=self.headers,
                                 data=json.dumps(self.request_payload))

        return response.json()['items']
