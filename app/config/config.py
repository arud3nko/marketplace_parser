from configparser import ConfigParser

driver_config = {
    "driverOptions": [
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-automation",
        "--disable-extensions",
        "--dns-prefetch-disable",
        "--disable-gpu",
        "--disable-infobars",
        "--disable-dev-shm-usage",
        "--disable-browser-side-navigation",
        "--no-exit",
        "--enable-javascript",
        "--blink-settings=imagesEnabled=false"
    ],
    "driverMode": "normal"
}

allowed_marketplaces = ["ozon"]

config = ConfigParser()
config.read("./conf.ini")

TOKEN = config["BOT"]["TOKEN"]

BASE_WEBHOOK_URL = config["SERVER"]["BASE_WEBHOOK_URL"]

DB_HOST = config["DATABASE"]["HOST"]
DB_PORT = config["DATABASE"]["PORT"]
DB_USERNAME = config["DATABASE"]["USERNAME"]
DB_PASSWORD = config["DATABASE"]["PASSWORD"]
DB_DATABASE = config["DATABASE"]["DATABASE"]


