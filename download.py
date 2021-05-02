from flask import Blueprint, send_from_directory, redirect, current_app, session, request, render_template, url_for
from source import downloader

download = Blueprint('download', __name__)
caches_folder = './.spotify_caches/'

def session_cache_path():
    return caches_folder + session.get('uuid')

def spotify_class_object():
    return current_app.config["spotify_client_object"]

@download.route('/query/', methods=["POST", "GET"])
def download_file():
    if request.method == "POST":
        form = request.form.to_dict()
        spotify_object = spotify_class_object()
        cache_handler = spotify_object.authenticate(cache_path=session_cache_path())
        if not spotify_object.validate(cache_handler=cache_handler):
            return redirect('/')
        query = form["search_query"].replace(' ', '+')
        download_type = form["type"]
        sp = spotify_object.spotify_object()

        if query == '' or query.strip() == '':
            return render_template('download.html', title='Downloads', active_page='download', username=sp.me()["display_name"], status=False, query=query, type=download_type)

        if download_type == 'video' :
            out_file = downloader.download_video(query=query)
        elif download_type == 'audio':
            out_file = downloader.download_audio(query=query)
        else:
            return f'Invalid download type - {download_type}', 200

        if out_file != False :
            return render_template('download.html', title='Downloads', active_page='download', username=sp.me()["display_name"], status=True, query=query, out_file=out_file, type=download_type)
        return render_template('download.html', title='Downloads', active_page='download', username=sp.me()["display_name"], status=False, query=query, type=download_type)

    elif request.method == "GET":
        spotify_object = spotify_class_object()
        cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

        if not spotify_object.validate(cache_handler=cache_handler):
            return redirect('/')

        download_type = request.args.get('download_type') if request.args.get('download_type') else 'AUDIO'
        if request.args.get('search'):
            query = request.args.get('search')
        else :
            return "Provide Query"
        query = query.replace(' ', '+')
        if download_type.upper() == 'VIDEO':
            out_file = downloader.download_video(query=query)

        elif download_type.upper() == 'AUDIO':
            out_file = downloader.download_audio(query=query)

        else:
            return f'Invalid download type - {download_type}', 200

        if out_file != '':
            return f'Successfully downloaded {download_type.lower()} file - {out_file}', 200
        return 'Download failed', 400
    
@download.route('/')
def index():
    spotify_object = spotify_class_object()
    cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

    if not spotify_object.validate(cache_handler=cache_handler):
        return redirect('/')
    sp = spotify_object.spotify_object()
    return render_template('download.html', title='Downloads', active_page='download', username=sp.me()["display_name"])


@download.route('/<mode>/static/<path:path>')
def send_static(path, mode=None):
    return send_from_directory('templates/static', path)
