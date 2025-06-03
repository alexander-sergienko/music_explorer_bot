from aiogram import Dispatcher
from aiogram.types import Message
from utils.logger import log_message
from api.lastfm import get_artist_info

async def artist_info_handler(message: Message):
    log_message(message.from_user.id, message.text, "Пользователь")
    args = message.get_args()
    if not args:
        response = "Пожалуйста, укажите имя исполнителя. Пример: /исполнитель Queen"
    else:
        info = get_artist_info(args)
        if "error" in info:
            response = "Исполнитель не найден. Попробуйте другое имя."
        else:
            response = f"🎤 {info['name']}

{info['bio']}
🔗 Подробнее: {info['url']}"
    log_message(message.from_user.id, response, "Бот")
    await message.answer(response)

async def placeholder_command(message: Message):
    log_message(message.from_user.id, message.text, "Пользователь")
    response = "Эта команда пока в разработке."
    log_message(message.from_user.id, response, "Бот")
    await message.answer(response)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(artist_info_handler, commands=["исполнитель"])
    dp.register_message_handler(placeholder_command, commands=["похожие", "жанр", "чарты"])
