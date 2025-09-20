# translator.py
import random
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET
))

# Map moods to Spotify playlist IDs
mood_playlists = {
    "happy": "5K8KZLcYTHNdvrp2EcqoeV", # Happy Hits!
    "sad": "1uSBO26jwXUK39sCFqCQh6", # Life Sucks
    "relaxed": "0jRTrfyTEBHOSpp050erHI", # Chill Vibes
    "neutral": "7wc7MGoNRFgHZoygNryPZ8" # Pop Mix
}

# AI: Sentiment analysis
def analyze_mood_from_text(user_text: str) -> str:
    blob = TextBlob(user_text)
    polarity = blob.sentiment.polarity

    if polarity > 0.4:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    elif -0.3 <= polarity <= 0.1:
        return "relaxed"
    else:
        return "neutral"

# Fetch random song from Spotify playlist
def get_song_from_spotify(mood: str) -> dict:
    if mood not in mood_playlists:
        return {"title": "No playlist found", "url": None}

    playlist_id = mood_playlists[mood]
    results = sp.playlist_items(playlist_id, limit=20)
    tracks = results["items"]

    if not tracks:
        return {"title": "No tracks found", "url": None}

    track = random.choice(tracks)["track"]
    return {
        "title": f"{track['name']} - {track['artists'][0]['name']}",
        "url": track["external_urls"]["spotify"]
    }