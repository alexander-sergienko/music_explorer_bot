import requests
from config import LASTFM_API_KEY

def get_artist_info(artist_name):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("artist", {}).get("name", artist_name),
            "bio": data.get("artist", {}).get("bio", {}).get("summary", "Нет информации"),
            "url": data.get("artist", {}).get("url", ""),
        }
    return {"error": "Исполнитель не найден"}

def get_similar_artists(artist_name):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist={artist_name}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [artist["name"] for artist in data.get("similarartists", {}).get("artist", [])[:5]]
    return []

def get_genre_info(genre_name):
    url = f"http://ws.audioscrobbler.com/2.0/?method=tag.getinfo&tag={genre_name}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("tag", {}).get("name", genre_name),
            "description": data.get("tag", {}).get("wiki", {}).get("content", "Нет описания"),
            "url": f"https://www.last.fm/tag/{genre_name}",
        }
    return {"error": "Жанр не найден"}

def get_top_tracks():
    url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [{
            "name": track["name"],
            "artist": track["artist"]["name"]
        } for track in data.get("tracks", {}).get("track", [])]
    return []