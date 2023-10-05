from configparser import ConfigParser

config = ConfigParser()
config.read("./conf.ini")

TOKEN = config["BOT"]["TOKEN"]

BASE_WEBHOOK_URL = config["SERVER"]["BASE_WEBHOOK_URL"]

DB_HOST = config["DATABASE"]["HOST"]
DB_PORT = config["DATABASE"]["PORT"]
DB_USERNAME = config["DATABASE"]["USERNAME"]
DB_PASSWORD = config["DATABASE"]["PASSWORD"]
DB_DATABASE = config["DATABASE"]["DATABASE"]
