import logging

from aiogram import Router, types, F
from aiogram.enums import ParseMode

from aiohttp import web

from app.db.db import DB
from app.bot.bot import bot

router = Router()


@router.callback_query(F.data.startswith("send_to_channel::"))
async def send_to_channel_query(callback: types.CallbackQuery):
    """
    Отправка товара в канал
    :param callback:
    :return:
    """
    product_id = int(callback.data.split("::")[1])

    db = DB()

    product = await db.select_where(table_name="sent_to_admin",
                                    where_cond="product_id",
                                    where_value=product_id)

    _, title, price, price_discount, vendor_code, link, image_link, date, category_id, pid = product[0]

    category = await db.select_where(table_name="categories",
                                     where_cond="id",
                                     where_value=category_id)

    message = f"""*{title}*

📌 *{price_discount} ₽* | ~{price} ₽~

Код товара: {vendor_code}

Смотреть на [OZON]({link})

❤️ - Супер
👍🏻 - Пойдёт
😐 - Не очень
💵 - Дороговато

#{str(category[0][1]).replace(' ', '_').lower()}
"""

    message = message.replace('.', '\.')\
                     .replace('|', '\|')\
                     .replace('-', '\-')\
                     .replace('#', '\#')\
                     .replace('_', '\_')\
                     .replace('!', '\!')

    await bot.send_photo(chat_id=category[0][-1],
                         photo=image_link,
                         caption=message,
                         reply_markup=None,
                         parse_mode=ParseMode.MARKDOWN_V2)

    await callback.message.delete()

    logging.info(f"Sent post to channel {category[0][-1]} | Product ID {product_id}")

    return web.Response(status=200)


@router.callback_query(F.data.startswith("drop_post::"))
async def drop_post(callback: types.CallbackQuery):
    """
    Удаление товара из админ-чата
    :param callback:
    :return:
    """
    product_id = int(callback.data.split("::")[1])

    db = DB()

    await db.delete(table_name="sent_to_admin",
                    where_cond="product_id",
                    where_value=product_id)

    await callback.message.delete()
