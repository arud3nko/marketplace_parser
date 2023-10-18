from aiogram import Router, types, F
from aiohttp import web

router = Router()


@router.message()
async def skip_any_messages(message: types.Message):
    """
    Отвечаем на неотслеживаемые сообщения

    :param message:
    :return:
    """
    return web.Response(status=401)
