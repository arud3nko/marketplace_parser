import json
import time
import os
import logging

from app.parser.parser import Parser
from bs4 import BeautifulSoup


class Ozon(Parser):
    def __init__(self):
        super().__init__("ozon")

    def parse_category(self, url: str):
        super().get_category_pages(url=url,
                                   start=1,
                                   end=3,
                                   pages_lambda=lambda x: x*3 + 1)

    def get_category_items(self):
        products = {}
        for page in os.listdir(f"./app/parseData/ozon/pages/{self._uuid}"):
            with open(f"./app/parseData/ozon/pages/{self._uuid}/{page}", "r") as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            el = soup.find_all("a", {"class": "tile-hover-target r1i ri2"})

            for tag in el:
                products[tag.text] = tag.get("href")

        with open(f"./app/parseData/ozon/items/{self._uuid}.json", "w") as file:
            file.write(json.dumps(products, ensure_ascii=False, indent=4))

    def get_products_html(self):
        products = super().get_items_data()

        i = 0
        for product in products:
            page = self.get_page(f"https://www.ozon.ru{product.split('/?')[0]}")

            try:
                with open(f"./app/parseData/{self.marketplace}/items/{self._uuid}/product_{i}.html", "w") as file:
                    file.write(page)
                logging.info(f"https://www.ozon.ru{product.split('/?')[0]}")
            except Exception as e:
                logging.error(f"Error while trying to write product .html: {e}")
            finally:
                file.close()

            i += 1



