import requests
from config import LASTFM_API_KEY

def get_artist_info(artist_name: str) -> dict:
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "lang": "ru"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "artist" not in data:
        return {"error": "Исполнитель не найден"}
    artist = data["artist"]
    bio = artist["bio"]["summary"].split("<a")[0].strip()
    name = artist["name"]
    url = artist["url"]
    return {
        "name": name,
        "bio": bio,
        "url": url
    }
