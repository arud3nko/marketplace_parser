import logging

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

from aiohttp import web

from app.db.db import DB
from app.bot.bot import bot

from contextlib import suppress

router = Router()


@router.callback_query(F.data.startswith("send_to_channel::"))
async def send_to_channel_query(callback: types.CallbackQuery):
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

📌 *{price_discount} ₽* \| ~{price} ₽~

Код товара: {vendor_code}

Смотреть на [OZON]({link})

❤️ \- Супер
👍🏻 \- Пойдёт
😐 \- Не очень
💵 \- Дороговато
""".replace('.', '\.')

    await bot.send_photo(chat_id=category[0][-1],
                         photo=image_link,
                         caption=message,
                         reply_markup=None,
                         parse_mode=ParseMode.MARKDOWN_V2)

    await callback.message.delete()

    return web.Response(status=200)


@router.callback_query(F.data.startswith("drop_post::"))
async def send_to_channel_query(callback: types.CallbackQuery):
    product_id = int(callback.data.split("::")[1])

    db = DB()

    await db.delete(table_name="sent_to_admin",
                    where_cond="product_id",
                    where_value=product_id)

    await callback.message.delete()


@router.message()
async def skip_any_messages(message: types.Message):
    return web.Response(status=401)
