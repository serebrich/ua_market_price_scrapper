import requests
import json
from pprint import pprint
import pandas as pd
from scrapper_parent import ScrapperParent


class Silpo(ScrapperParent):

    def __init__(self):
        super().__init__()
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
                                    "To": 5000,
                                    "ingredients": False,
                                    "categoryId": None,
                                    "RangeFilters": {},
                                    "MultiFilters": {},
                                    "UniversalFilters": [],
                                    "CategoryFilter": [],
                                    "Promos": []}}

        self.df = pd.DataFrame(columns=['name', 'price', 'price_by'])

    def set_payload_to_category(self, category):
        self.request_payload['data']["categoryId"] = self.category[category]

    def get_items_json_by_category(self, category):
        self.set_payload_to_category(category)

        response = requests.post('https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal',
                                 headers=self.headers,
                                 data=json.dumps(self.request_payload))

        return response.json()['items']

    def add_to_df(self, items_json):
        data_for_df = {'name': [item['name'] for item in items_json],
                       'price': [item['price'] for item in items_json],
                       'price_by': [item['unit'] for item in items_json]}

        self.df = pd.concat([pd.DataFrame(data_for_df), self.df],)

    def run(self):
        for category in self.category.keys():
            items_json = self.get_items_json_by_category(category)
            self.add_to_df(items_json)
        self.write_to_sheet()



if __name__ == '__main__':
    silpo = Silpo()
    silpo.run()

