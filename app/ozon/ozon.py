import json
import random
import os
import logging

from app.parser.parser import Parser
from bs4 import BeautifulSoup


def trigger(soup):
    check = soup.find("div", {"id": "paginatorContent"}).find('a').parent
    el = check if len(check.get("class")) > 1 else check.parent
    return f"{'.'.join(el.get('class'))}:last-child"


class Ozon(Parser):
    def __init__(self, table_name):
        super().__init__("ozon")
        self.table_name = table_name

    def parse_category(self, url: str):
        uri = random.randint(1, 10)
        super().get_category_pages(url=url,
                                   start=uri,
                                   end=uri,
                                   trigger=trigger,
                                   # pages_lambda=lambda x: x*3 + 1)
                                   pages_lambda=lambda x: x+1)
        self.get_products_info()

    def get_products_info(self):
        for page in os.listdir(f"./app/parseData/ozon/pages/{self._uuid}"):
            with open(f"./app/parseData/ozon/pages/{self._uuid}/{page}", "r") as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            items = soup.find_all("div", {"class": f"{self.trigger.split(':')[0].replace('.', ' ')}"})

            for product in items:
                title = product.find_all("a")[1]
                link = "https://ozon.ru" + title.get("href").split('/?')[0]
                vendor_code = link.split('-')[-1].replace('/', '') if '-' in link else link.split('/')[-1]
                image_link = product.find("img").get("src")

                price_discount = product.find("span", {"class": "tsHeadline500Medium"}).text.replace('\u2009', ' ')\
                    .replace(' ', '').replace('₽', '')
                price = product.find("span", {"class": "tsBodyControl400Small"}).text.replace('\u2009', ' ') \
                    .replace(' ', '').replace('₽', '')

                self.products.append({
                    "title": title.text,
                    "price": int(price) if price != '' else price_discount,
                    "price_discount": int(price_discount),
                    "vendor_code": vendor_code,
                    "link": link,
                    "image_link": image_link
                })

        super().check_if_product_exists()

    def get_category_items(self):
        # DEPRECATED
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



