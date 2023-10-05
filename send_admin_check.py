from app.db.db import DB

import logging
import requests
import json
import random


def send_admin_response(data: list, admin_chat_id: int, category_chat_id: int):

    _, title, price, price_discount, vendor_code, link, image_link, date, category_id = data
    item_dict = {
        "product_id": _,
        "admin_chat_id": admin_chat_id,
        "channel_chat_id": category_chat_id,
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
    requests.post("https://5667-95-26-197-141.ngrok-free.app/admin_ads",
                  data=json_data,
                  headers=header)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    db = DB()

    table_products = "products"
    table_sent_to_admin = "sent_to_admin"
    table_categories = "categories"

    categories = db.select(table_categories)

    for category in categories:
        selected_products = []

        products = db.select_where(table_name=table_products,
                                   where_cond="category_id",
                                   where_value=category[0])

        for i in range(5):
            selected_products.append(products.pop(random.randint(0, len(products) - 1)))

        for product in selected_products:
            db.delete(table_name=table_products,
                      where_cond="id",
                      where_value=product[0])

            db.insert(table_name=table_sent_to_admin,
                      product_id=product[0],
                      title=product[1],
                      price=product[2],
                      price_discount=product[3],
                      vendor_code=product[4],
                      link=product[5],
                      image_link=product[6],
                      created_at=product[7],
                      category_id=product[8])

            send_admin_response(product, category[4], category[5])


if __name__ == '__main__':
    main()
