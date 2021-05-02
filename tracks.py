from flask import Blueprint, redirect, current_app, session, request, render_template, send_from_directory

tracks = Blueprint('tracks', __name__)
caches_folder = './.spotify_caches/'

def session_cache_path():
    return caches_folder + session.get('uuid')

def spotify_class_object():
    return current_app.config["spotify_client_object"]

@tracks.route('/saved/',methods=['POST','GET','DELETE'])
def saved_tracks():
    spotify_object = spotify_class_object()
    cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

    if not spotify_object.validate(cache_handler=cache_handler):
        return redirect('/')

    sp = spotify_object.spotify_object()

    if request.method == 'POST':
        track_id = request.args.get('track_id') 
        if track_id == None:
            return 'Provide Track ID'
        # if not sp.current_user_saved_tracks_contains([track_id]):
        sp.current_user_saved_tracks_add([track_id])
        return 'Successfully added'
        # return 'Present in saved library already'

    elif request.method == 'GET':
        limit = request.args.get('limit') if request.args.get('limit') else 20
        return sp.current_user_saved_tracks(limit=limit)

    elif request.method == 'DELETE':
        track_id = request.args.get('track_id')
        if track_id == None:
           return 'Provide Track ID'
        if sp.current_user_saved_tracks_contains([track_id]):
            sp.current_user_saved_tracks_delete([track_id])
            return 'Successfully deleted'
        return 'Check track id as its not there in saved'

@tracks.route('/top/')
def top_tracks():
    spotify_object = spotify_class_object()
    cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

    if not spotify_object.validate(cache_handler=cache_handler):
        return redirect('/')

    sp = spotify_object.spotify_object()

    limit = request.args.get('limit') if request.args.get('limit') else 20
    user_top_tracks = sp.current_user_top_tracks(limit=limit)
    # return user_top_tracks
    return render_template('top_tracks.html', title='home',username=sp.me()["display_name"], active_page='dashboard', top_tracks = user_top_tracks)


@tracks.route('/<mode>/static/<path:path>')
def send_static(mode,path):
    return send_from_directory('templates/static', path)
