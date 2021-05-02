from flask import Blueprint, redirect, current_app, session, request

search = Blueprint('search', __name__)
caches_folder = './.spotify_caches/'

def session_cache_path():
    return caches_folder + session.get('uuid')

def spotify_class_object():
    return current_app.config["spotify_client_object"]

@search.route('/<query>/')
def search_track(query):
    spotify_object = spotify_class_object()
    cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

    if not spotify_object.validate(cache_handler=cache_handler):
        return redirect('/')

    sp = spotify_object.spotify_object()
    limit = request.args.get('limit') if request.args.get('limit') else 10

    return sp.search(q=query, limit=limit, type='track')