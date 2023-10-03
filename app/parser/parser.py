import undetected_chromedriver as uc
import uuid
import json
import time
import os
import logging

from app.config.config import driver_config, allowed_marketplaces


class Parser(object):
    def __init__(self, marketplace):
        if marketplace not in ("ozon", "wb"):
            raise ValueError(f"Error: incorrect marketplace. Allowed: {allowed_marketplaces}")

        self.marketplace = marketplace
        self._uuid = uuid.uuid4()

        self.driver = None
        self.driver_config = driver_config

        self.options = uc.ChromeOptions()
        self.options.page_load_strategy = 'normal'
        self.options.headless = False

        for option in self.driver_config["driverOptions"]:
            self.options.add_argument(option)

    def init_parser(self):
        try:
            self.driver = uc.Chrome(options=self.options)
            logging.info(f"Initialized parser type {self.marketplace}")
        except Exception as e:
            logging.error(f"Error while trying to initialize parser: {e}")

    def get_category_pages(self, url: str, start: int, end: int, pages_lambda=lambda x: x):
        try:
            os.makedirs(f"./app/parseData/{self.marketplace}/pages/{self._uuid}", exist_ok=True)
            logging.info(f"Created pages uuid directory {self._uuid}")
        except OSError as e:
            logging.error(f"Error while trying to create pages uuid directory: {e}")

        for i in [pages_lambda(x) for x in range(start-1, end)]:
            page = self.get_page(url + f"?page={i}")

            try:
                with open(f"./app/parseData/{self.marketplace}/pages/{self._uuid}/page_{i}.html", "w") as file:
                    file.write(page)
            except Exception as e:
                logging.error(f"Error while writing html file: {e}")
            finally:
                file.close()

    def get_items_data(self):
        try:
            os.makedirs(f"./app/parseData/{self.marketplace}/items/{self._uuid}", exist_ok=True)
            logging.info(f"Created items uuid directory {self._uuid}")
        except OSError as e:
            logging.error(f"Error while trying to create items uuid directory: {e}")

        try:
            with open(f"./app/parseData/{self.marketplace}/items/{self._uuid}.json", "r") as file:
                products = json.loads(file.read())
        except Exception as e:
            logging.error(f"Error while reading json file: {e}")
        finally:
            file.close()

        return list(products.values())

    def get_page(self, url):
        self.driver.get(url)
        time.sleep(5)

        page = self.driver.page_source

        return page

    def __quit(self):
        self.driver.quit()
