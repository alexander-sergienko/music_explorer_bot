from aiogram import Dispatcher
from aiogram.types import Message
from utils.logger import log_message
from api.lastfm import get_artist_info, get_similar_artists, get_genre_info, get_top_tracks

# FSM: пользователь вводит имя исполнителя
async def artist_info_handler_from_input(message: Message):
    log_message(message.from_user.id, message.text, "Пользователь")
    info = get_artist_info(message.text)
    if "error" in info:
        response = "Исполнитель не найден. Попробуйте другое имя."
    else:
        response = f"🎤 {info['name']}\n\n{info['bio']}\n🔗 Подробнее: {info['url']}"
    log_message(message.from_user.id, response, "Бот")
    await message.answer(response)

# FSM: пользователь вводит имя для поиска похожих
async def similar_artists_handler_from_input(message: Message):
    log_message(message.from_user.id, message.text, "Пользователь")
    artists = get_similar_artists(message.text)
    if not artists:
        response = "Похожие исполнители не найдены."
    else:
        response = f"🎵 Похожие на {message.text}:\n\n" + "\n".join(f"{i+1}. {artist}" for i, artist in enumerate(artists[:5]))
    log_message(message.from_user.id, response, "Бот")
    await message.answer(response)

# FSM: пользователь вводит жанр
async def genre_info_handler_from_input(message: Message):
    log_message(message.from_user.id, message.text, "Пользователь")
    info = get_genre_info(message.text)
    if "error" in info:
        response = "Жанр не найден. Попробуйте другой."
    else:
        response = f"🎶 Жанр {info['name']}:\n\n{info['description']}\n🔗 Подробнее: {info['url']}"
    log_message(message.from_user.id, response, "Бот")
    await message.answer(response)

# /чарты — всегда доступен
async def charts_handler(message: Message):
    log_message(message.from_user.id, message.text, "Пользователь")
    tracks = get_top_tracks()
    if not tracks:
        response = "Чарт временно недоступен."
    else:
        response = "🔥 Топ-10 песен из мирового чарта Last.fm:\n\n" + "\n".join(f"{i+1}. {track['name']} - {track['artist']}" for i, track in enumerate(tracks[:10]))
    log_message(message.from_user.id, response, "Бот")
    await message.answer(response)

def register_handlers(dp: Dispatcher):
    pass  # FSM-обработчики регистрируются напрямую в bot.py