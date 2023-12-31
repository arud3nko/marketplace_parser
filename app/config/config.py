from configparser import ConfigParser

ALLOWED_MARKETPLACES = ["ozon", "wb"]

# конфиги айдишников для работы с бд

ITER_CATEGORY_NAME = 1
ITER_CATEGORY_ID = 0
ITER_CATEGORY_OZON_LINK = -1
ITER_CATEGORY_WB_LINK = -2
ITER_CATEGORY_ADMIN_CHAT_ID = 3
ITER_CATEGORY_CHANNEL_CHAT_ID = 4
ITER_CATEGORY_MULTI_CHANNEL_CHAT_ID = 5

ITER_PRODUCT_ID = 0
ITER_PRODUCT_TITLE = 1
ITER_PRODUCT_PRICE = 2
ITER_PRODUCT_PRICE_DISCOUNT = 3
ITER_PRODUCT_VENDOR_CODE = 4
ITER_PRODUCT_LINK = 5
ITER_PRODUCT_IMAGE_LINK = 6
ITER_PRODUCT_CREATED_AT = 7
ITER_PRODUCT_CATEGORY_ID = 8

NUMBER_OF_PRODUCTS_PER_MARKETPLACE = 2
NUMBER_OF_PRODUCTS_TO_SELECT = NUMBER_OF_PRODUCTS_PER_MARKETPLACE * 2  # выбираем последние элементы массива из products


TABLE_PRODUCTS = "products"
TABLE_SENT_TO_ADMIN = "sent_to_admin"
TABLE_CATEGORIES = "categories"


config = ConfigParser()
config.read("./conf.ini")

TOKEN = config["BOT"]["TOKEN"]

BASE_WEBHOOK_URL = config["SERVER"]["BASE_WEBHOOK_URL"]
WEBHOOK_PATH = config["SERVER"]["WEBHOOK_PATH"]

DB_HOST = config["DATABASE"]["HOST"]
DB_PORT = config["DATABASE"]["PORT"]
DB_USERNAME = config["DATABASE"]["USERNAME"]
DB_PASSWORD = config["DATABASE"]["PASSWORD"]
DB_DATABASE = config["DATABASE"]["DATABASE"]


