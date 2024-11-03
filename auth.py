from flask import session, redirect
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from config import client_id, client_secret, redirect_uri, scope

cache_handler = FlaskSessionCacheHandler(session)

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

def get_spotify():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        return None  # Return None if the token is invalid
    
    return Spotify(auth_manager=sp_oauth)  # Create a new Spotify instance each time

