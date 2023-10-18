import os
import random

from bs4 import BeautifulSoup

from app.parser.parser import Parser


# не используем для вб
def trigger(soup):
    return "product-card-list"


class WB(Parser):
    def __init__(self, table_name):
        super().__init__("wb")
        self.table_name = table_name

    def parse_category(self, url: str):
        uri = random.randint(1, 10)
        super().get_category_pages(url=url,
                                   start=uri,
                                   end=uri,
                                   trigger=trigger,
                                   # pages_lambda=lambda x: x*3 + 1)
                                   pages_lambda=lambda x: x+1,
                                   pages_link="&")
        self.get_products_info()

    def get_products_info(self):
        for page in os.listdir(f"./app/parseData/wb/pages/{self._uuid}"):
            with open(f"./app/parseData/wb/pages/{self._uuid}/{page}", "r") as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            items = soup.find_all("div", {"class": "product-card__wrapper"})

            for product in items:
                title = product.find("span", {"class": "product-card__name"})
                link = product.find("a").get("href")
                vendor_code = None
                image_link = product.find("img").get("src")

                price_discount = product.find("ins", {"class": "price__lower-price"}).text.replace(u"\xa0", "")\
                    .replace('₽', '')
                price = product.find("del").text.replace(u"\xa0", "")\
                    .replace('₽', '')

                self.products.append({
                    "title": title.text.replace("/ ", ""),
                    "price": int(price) if price != '' else price_discount,
                    "price_discount": int(price_discount),
                    "vendor_code": vendor_code,
                    "link": link,
                    "image_link": image_link
                })

        super().check_if_product_exists()
