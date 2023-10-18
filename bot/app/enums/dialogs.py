from enum import StrEnum


class NewCategory(StrEnum):
    GET_TITLE = "Отправьте название категории"
    GET_LINK = "Отправьте ссылку на категорию"
    GET_ADMIN_CHAT_ID = "Отправьте ID админ-чата"
    GET_CHANNEL_CHAT_ID = "Отправьте ID (никнейм) канала"
    OK = "Категория успешно добавлена"
