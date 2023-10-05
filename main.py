from app.ozon.ozon import Ozon
from app.db.db import DB

import logging
import requests
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    parser = Ozon("products")

    db = DB()

    categories = db.select(table_name="categories")

    for category in categories:
        logging.info(f"Parsing category: {category[1]}")

        parser.parse_category(category[2])
        parser.get_products_info()
        parser.save_products(category_id=category[0])


if __name__ == '__main__':
    main()
