import undetected_chromedriver as uc
import uuid
import json
import time
import os
import logging
import cloudscraper
import selenium.webdriver

from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

from app.config.config import driver_config, allowed_marketplaces
from app.db.db import DB


class Parser(object):
    def __init__(self, marketplace):
        if marketplace not in ("ozon", "wb"):
            raise ValueError(f"Error: incorrect marketplace. Allowed: {allowed_marketplaces}")

        self.marketplace = marketplace
        self._uuid = uuid.uuid4()

        self.driver = None
        self.driver_config = driver_config
        self.trigger = None

        self.options = None
        self.cookies = None

        self.db = DB()
        self.products = []
        self.table_name = None

        self.proxy = Proxy()
        self.proxy.proxy_type = ProxyType.MANUAL

        self.proxy.socks_proxy = "192.241.149.84:37455"
        self.proxy.socksVersion = 5

        # self.options = ChromiumOptions()
        # self.options.headless = True
        # # self.options.add_argument("--auto-open-devtools-for-tabs")
        #
        # for option in self.driver_config["driverOptions"]:
        #     self.options.add_argument(option)

    def init_parser(self):
        try:
            self.driver = uc.Chrome(options=self.set_options())
            logging.info(f"Initialized parser type {self.marketplace}")
        except Exception as e:
            logging.error(f"Error while trying to initialize parser: {e}")

    def set_options(self):
        self.options = ChromiumOptions()
        self.options.headless = True
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-browser-side-navigation")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--enable-javascript")
        self.options.add_argument("--blink-settings=imagesEnabled=false")
        self.options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

        return self.options

    def get_category_pages(self, url: str, start: int, end: int, trigger=None, pages_lambda=lambda x: x):
        try:
            os.makedirs(f"./app/parseData/{self.marketplace}/pages/{self._uuid}", exist_ok=True)
            logging.info(f"Created pages uuid directory {self._uuid}")
        except OSError as e:
            logging.error(f"Error while trying to create pages uuid directory: {e}")

        for i in [pages_lambda(x) for x in range(start - 1, end)]:
            page = self.get_page(url + f"?page={i}", trigger)

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

    def generate_trigger(self, trigger, source):
        soup = BeautifulSoup(source, 'lxml')
        self.trigger = trigger(soup)
        logging.info(f"Generated trigger {self.trigger}")

    def get_page(self, url, trigger=None):
        self.init_parser()
        self.driver.get(url)

        if trigger:
            tries = 0
            while tries < 2:
                if self.trigger is None:
                    self.generate_trigger(trigger, self.driver.page_source)

                try:
                    WebDriverWait(self.driver,
                                  timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME, self.trigger)))
                except TimeoutException:
                    logging.error(f"Timeout trigger: {trigger} for {url}")
                    self.generate_trigger(trigger, self.driver.page_source)
                    tries += 1
                    continue
                break

        page = self.driver.page_source

        if "Cloudflare" in page:
            logging.error(f"Detected by Cloudflare: {url}")
            return self.__quit()

        logging.info(f"Successfully got {url}")

        self.__quit()

        return page

    def save_products(self, category_id: int):
        for product in self.products:
            self.db.insert(table_name=self.table_name,
                           category_id=category_id,
                           **product)

    def __quit(self):
        self.driver.quit()
        logging.info("Quit driver")
