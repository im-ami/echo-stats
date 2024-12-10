from flask import session, redirect
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from config.settings import client_id, client_secret, redirect_uri, scope

def get_cache_handler():
    return FlaskSessionCacheHandler(session)

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_handler=get_cache_handler(),
        show_dialog=True
    )

sp_oauth = get_spotify_oauth()

def get_spotify():
    cache_handler = get_cache_handler()
    token_info = cache_handler.get_cached_token()
    
    if not token_info:
        return None
        
    # Check if token needs refresh
    if sp_oauth.is_token_expired(token_info):
        try:
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            cache_handler.save_token_to_cache(token_info)
        except:
            return None
            
    return Spotify(auth=token_info['access_token'])

