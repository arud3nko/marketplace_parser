from app.ozon.ozon import Ozon

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

parser = Ozon()

parser.init_parser()

parser.parse_category("https://www.ozon.ru/category/aksessuary-dlya-telefonov-15511/")

parser.get_category_items()

parser.get_products_html()
