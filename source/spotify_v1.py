import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .scope import SCOPE

class SpotifyClientAPI(object):
    user_id = None
    client_id = None
    client_secret = None
    auth_manager = None

    def __init__(self,client_id,client_secret, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def authenticate(self, cache_path):
        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path)
        self.auth_manager = spotipy.oauth2.SpotifyOAuth(scope=SCOPE,
                                                        cache_handler=cache_handler,
                                                        show_dialog=True)
        return cache_handler

    def validate(self,cache_handler):
        return self.auth_manager.validate_token(cache_handler.get_cached_token())

    def spotify_object(self):  
        return spotipy.Spotify(auth_manager=self.auth_manager)
