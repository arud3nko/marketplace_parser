import logging
import send_admin_check

from app.ozon.ozon import Ozon
from app.wb.wb import WB
from app.db.db import DB
from app.config.config import (ITER_CATEGORY_ID, ITER_CATEGORY_NAME,
                               ITER_CATEGORY_WB_LINK, ITER_CATEGORY_OZON_LINK)


logging.basicConfig(level=logging.INFO, filename="info.log",
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    db = DB()

    table_categories = "categories"

    categories = db.select(table_categories)

    for category in categories:
        logging.info(f"Parsing category: {category[ITER_CATEGORY_NAME]}")

        parser = Ozon(table_name="products")
        parser.parse_category(url=category[ITER_CATEGORY_OZON_LINK])
        parser.save_products(category_id=category[ITER_CATEGORY_ID])

        parser = WB(table_name="products")
        parser.parse_category(url=category[ITER_CATEGORY_WB_LINK])
        parser.save_products(category_id=category[ITER_CATEGORY_ID])

    send_admin_check.main()


if __name__ == '__main__':
    main()
