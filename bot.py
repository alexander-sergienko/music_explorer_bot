from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from config import BOT_TOKEN
from utils.logger import log_message
import handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: Message):
    log_message(message.from_user.id, message.text, "Пользователь")
    response = "🎵 Привет! Я — музыкальный гид.\n\nДоступные команды:\n" \
               "/исполнитель <имя> — информация об исполнителе\n" \
               "/похожие <имя> — похожие исполнители\n" \
               "/жанр <жанр> — описание музыкального жанра\n" \
               "/чарты — топ-10 песен"
    log_message(message.from_user.id, response, "Бот")
    await message.answer(response)

handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
