from aiogram.fsm.state import StatesGroup, State


class NewCategoryStates(StatesGroup):
    """
    Машина состояний
    """
    get_category_title = State()
    get_category_link = State()
    get_admin_chat_id = State()
    get_channel_chat_id = State()
