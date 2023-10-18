import json

import requests

from app.config.config import (BASE_WEBHOOK_URL, TABLE_PRODUCTS, TABLE_SENT_TO_ADMIN, TABLE_CATEGORIES,
                               ITER_CATEGORY_ID, ITER_PRODUCT_ID, ITER_PRODUCT_TITLE, ITER_PRODUCT_PRICE,
                               ITER_PRODUCT_PRICE_DISCOUNT,
                               ITER_PRODUCT_VENDOR_CODE, ITER_PRODUCT_LINK, ITER_PRODUCT_IMAGE_LINK,
                               ITER_PRODUCT_CREATED_AT, NUMBER_OF_PRODUCTS_TO_SELECT,
                               ITER_CATEGORY_ADMIN_CHAT_ID, ITER_CATEGORY_CHANNEL_CHAT_ID,
                               ITER_CATEGORY_MULTI_CHANNEL_CHAT_ID, WEBHOOK_PATH)
from app.db.db import DB


def send_admin_response(data: list, admin_chat_id: int, category_chat_id: str, multi_chat_id: str):
    _, title, price, price_discount, vendor_code, link, image_link, date, category_id = data
    item_dict = {
        "product_id": _,
        "admin_chat_id": admin_chat_id,
        "channel_chat_id": category_chat_id,
        "multi_chat_id": multi_chat_id,
        "title": title,
        "price": int(price),
        "price_discount": int(price_discount),
        "vendor_code": vendor_code,
        "link": link,
        "image_link": image_link,
        "category_id": category_id
    }

    json_data = json.dumps(item_dict)

    header = {"Content-Type": "application/json"}
    requests.post(f"{BASE_WEBHOOK_URL}/{WEBHOOK_PATH}",
                  data=json_data,
                  headers=header)


def main():
    db = DB()

    categories = db.select(TABLE_CATEGORIES)

    for category in categories:
        products = db.select_where(table_name=TABLE_PRODUCTS,
                                   where_cond="category_id",
                                   where_value=category[ITER_CATEGORY_ID])

        selected_products = products[-NUMBER_OF_PRODUCTS_TO_SELECT:]

        for product in selected_products:
            db.delete(table_name=TABLE_PRODUCTS,
                      where_cond="id",
                      where_value=product[ITER_PRODUCT_ID])

            db.insert(table_name=TABLE_SENT_TO_ADMIN,
                      product_id=product[ITER_PRODUCT_ID],
                      title=product[ITER_PRODUCT_TITLE],
                      price=product[ITER_PRODUCT_PRICE],
                      price_discount=product[ITER_PRODUCT_PRICE_DISCOUNT],
                      vendor_code=product[ITER_PRODUCT_VENDOR_CODE],
                      link=product[ITER_PRODUCT_LINK],
                      image_link=product[ITER_PRODUCT_IMAGE_LINK],
                      created_at=product[ITER_PRODUCT_CREATED_AT],
                      category_id=category[ITER_CATEGORY_ID])

            send_admin_response(product,
                                category[ITER_CATEGORY_ADMIN_CHAT_ID],
                                category[ITER_CATEGORY_CHANNEL_CHAT_ID],
                                category[ITER_CATEGORY_MULTI_CHANNEL_CHAT_ID])


if __name__ == '__main__':
    main()
