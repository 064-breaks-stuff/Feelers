import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

SCOPES = (
    "user-read-private "
    "playlist-modify-public "
    "playlist-modify-private "
    "user-read-playback-state"
)

def get_spotify_client() -> spotipy.Spotify:
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=SCOPES,
        )
    )