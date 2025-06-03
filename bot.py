from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import BOT_TOKEN
from utils.logger import log_message
import handlers

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class InputState(StatesGroup):
    artist = State()
    similar = State()
    genre = State()

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    log_message(message.from_user.id, message.text, "Пользователь")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["👤 Исполнитель", "👥 Похожие", "🎼 Жанр", "🔥 Чарт 🔥"]
    keyboard.add(*buttons)
    response = "🎵 Привет! Я — музыкальный гид. Выберите действие:"
    log_message(message.from_user.id, response, "Бот")
    await message.answer(response, reply_markup=keyboard)

@dp.message_handler(lambda m: m.text == "👤 Исполнитель")
async def ask_artist(message: types.Message):
    await message.answer("Введите имя исполнителя:")
    await InputState.artist.set()

@dp.message_handler(lambda m: m.text == "👥 Похожие")
async def ask_similar(message: types.Message):
    await message.answer("Введите имя исполнителя для поиска похожих:")
    await InputState.similar.set()

@dp.message_handler(lambda m: m.text == "🎼 Жанр")
async def ask_genre(message: types.Message):
    await message.answer("Введите название музыкального жанра:")
    await InputState.genre.set()

@dp.message_handler(lambda m: m.text == "🔥 Чарт 🔥")
async def show_chart(message: types.Message):
    from handlers import charts_handler
    await charts_handler(message)

# Обработка пользовательского ввода
@dp.message_handler(state=InputState.artist)
async def handle_artist_input(message: types.Message, state: FSMContext):
    from handlers import artist_info_handler_from_input
    await artist_info_handler_from_input(message)
    await state.finish()

@dp.message_handler(state=InputState.similar)
async def handle_similar_input(message: types.Message, state: FSMContext):
    from handlers import similar_artists_handler_from_input
    await similar_artists_handler_from_input(message)
    await state.finish()

@dp.message_handler(state=InputState.genre)
async def handle_genre_input(message: types.Message, state: FSMContext):
    from handlers import genre_info_handler_from_input
    await genre_info_handler_from_input(message)
    await state.finish()

handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)