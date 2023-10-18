from app.bot.states.new_category import NewCategoryStates
from app.enums.dialogs import NewCategory

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.db.db import DB
from app.config.config import DB_CATEGORIES_TABLE, SUPER_ADMIN_CHAT_ID

router = Router()


@router.message(Command("new_category"),
                F.chat.id == SUPER_ADMIN_CHAT_ID)
async def new_category_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text=NewCategory.GET_TITLE
    )
    await state.set_state(NewCategoryStates.get_category_title)


@router.message(NewCategoryStates.get_category_title,
                F.chat.id == SUPER_ADMIN_CHAT_ID)
async def set_title(message: types.Message, state: FSMContext):
    await state.update_data(category_title=message.text)
    await message.answer(
        text=NewCategory.GET_LINK
    )
    await state.set_state(NewCategoryStates.get_category_link)


@router.message(NewCategoryStates.get_category_link,
                F.text.startswith("https://") &
                F.chat.id == SUPER_ADMIN_CHAT_ID)
async def set_link(message: types.Message, state: FSMContext):
    await state.update_data(category_link=message.text)
    await message.answer(
        text=NewCategory.GET_ADMIN_CHAT_ID
    )
    await state.set_state(NewCategoryStates.get_admin_chat_id)


@router.message(NewCategoryStates.get_admin_chat_id,
                F.chat.id == SUPER_ADMIN_CHAT_ID)
async def set_admin_chat_id(message: types.Message, state: FSMContext):
    await state.update_data(admin_chat_id=message.text)
    await message.answer(
        text=NewCategory.GET_CHANNEL_CHAT_ID
    )
    await state.set_state(NewCategoryStates.get_channel_chat_id)


@router.message(NewCategoryStates.get_channel_chat_id,
                F.chat.id == SUPER_ADMIN_CHAT_ID)
async def set_channel_chat_id(message: types.Message, state: FSMContext):
    await state.update_data(channel_chat_id=message.text)

    category_data = await state.get_data()
    db = DB()

    await db.insert(table_name=DB_CATEGORIES_TABLE,
                    title=category_data["category_title"],
                    link=category_data["category_link"],
                    admin_chat_id=category_data["admin_chat_id"],
                    channel_chat_id=category_data["channel_chat_id"])

    await message.answer(
        text=NewCategory.OK
    )

    await state.set_state(NewCategoryStates.get_category_link)
