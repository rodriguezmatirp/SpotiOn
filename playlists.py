from flask import Blueprint, redirect, current_app, session, request,send_from_directory

playlists = Blueprint('playlists', __name__)
caches_folder = './.spotify_caches/'

def session_cache_path():
    return caches_folder + session.get('uuid')

def spotify_class_object():
    return current_app.config["spotify_client_object"]

@playlists.route('/current/')
def current():
    spotify_object = spotify_class_object()
    cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

    if not spotify_object.validate(cache_handler=cache_handler):
        return redirect('/')

    sp = spotify_object.spotify_object()

    return sp.current_user_playlists()

@playlists.route('/<playlist_name>/',methods=['POST', 'GET', 'DELETE'])
def handle_playlist_request(playlist_name):
    spotify_object = spotify_class_object()
    cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

    if not spotify_object.validate(cache_handler=cache_handler):
        return redirect('/')

    sp = spotify_object.spotify_object()
    user_id = spotify_object.user_id

    if request.method == 'POST':
        description = request.args.get('description') if request.args.get('description') else ''
        public = request.args.get('public') if request.args.get('public') else False
        playlist = sp.user_playlist_create(user_id, name=playlist_name, description=description,public=public)
        return playlist

    elif request.method =='GET':
        if request.args.get('id'):
            return sp.playlist(request.args.get('id'))
        else:
            user_playlists = sp.current_user_playlists()
            for x in user_playlists["items"]:
                if x["name"] == playlist_name:
                    return sp.playlist(x["id"])
            return f'No playlist {playlist_name} created by user'

    elif request.method == 'DELETE':
        if request.args.get('id'):
            return sp.playlist(request.args.get('id'))
        else:
            user_playlists = sp.current_user_playlists()
            for x in user_playlists["items"]:
                if x["name"] == playlist_name:
                    sp.current_user_unfollow_playlist(x["id"])
                    return 'Successfully deleted'
            return f'No playlist {playlist_name} created by user'

@playlists.route('/update/<playlist_name>',methods=['POST','DELETE'])
def add_or_delete_tracks(playlist_name):
    spotify_object = spotify_class_object()
    cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

    if not spotify_object.validate(cache_handler=cache_handler):
        return redirect('/')

    sp = spotify_object.spotify_object()
    if not request.args.get('track_id'):
        return 'Please Provide track id to be added'
    track_id = request.args.get('track_id')

    if request.method == 'POST':
        sp.playlist_add_items(playlist_name, track_id)
        return 'Successfully added'
    elif request.method == 'DELETE':
        sp.playlist_remove_all_occurrences_of_items(playlist_name,track_id)
        return 'Successfully deleted'
    
@playlists.route('/<mode>/static/<path:path>')
@playlists.route('/<mode>/<mode_1>/static/<path:path>')
def send_static(mode,path,mode_1=None):
    return send_from_directory('templates/static', path)
