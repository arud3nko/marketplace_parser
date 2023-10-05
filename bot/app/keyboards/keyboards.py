from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


# def build_kb_accept(ID: int) -> InlineKeyboardMarkup:
#     inline_kb_accept = [
#         [InlineKeyboardButton(text="Принять".upper(), callback_data=f"accept_order::{ID}")]
#     ]
#
#     return InlineKeyboardMarkup(inline_keyboard=inline_kb_accept)


def build_kb_send_to_channel(ID: int) -> InlineKeyboardMarkup:
    inline_kb_accept_post = [
        [InlineKeyboardButton(text="Опубликовать".upper(), callback_data=f"send_to_channel::{ID}")],
        [InlineKeyboardButton(text="Удалить".upper(), callback_data=f"drop_post::{ID}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_accept_post)


# def build_kb_confirm_delivery(ID: int) -> InlineKeyboardMarkup:
#     inline_kb_confirm_send_to_delivery = [
#         [InlineKeyboardButton(text="Подтвердить".upper(), callback_data=f"confirm_delivery::{ID}"),
#          InlineKeyboardButton(text="Отменить".upper(), callback_data=f"cancel_delivery::{ID}")]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=inline_kb_confirm_send_to_delivery)
#
#
# def build_kb_cancel_delivery(ID: int) -> InlineKeyboardMarkup:
#     inline_kb_cancel_delivery = [
#         [InlineKeyboardButton(text="Отменить доставку".upper(), callback_data=f"cancel_delivery::{ID}")]
#     ]
#
#     return InlineKeyboardMarkup(inline_keyboard=inline_kb_cancel_delivery)
