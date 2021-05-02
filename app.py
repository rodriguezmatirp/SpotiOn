from flask import Flask, redirect, request, url_for, session, render_template, send_from_directory
from spotipy.oauth2 import SpotifyOAuth
from flask_session import Session
import os, uuid, spotipy,dotenv

from source import spotify_v1
from user_routes import user_routes
from playlists import playlists
from tracks import tracks
from search import search
from download import download

app = Flask(__name__, static_url_path='')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(playlists, url_prefix='/playlists')
app.register_blueprint(tracks, url_prefix='/tracks')
app.register_blueprint(search, url_prefix='/search')
app.register_blueprint(download, url_prefix='/download')

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

Session(app)

dotenv.load_dotenv('.env')

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')

@app.route('/')
def index():
    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotify_object.authenticate(cache_path=session_cache_path())

    if request.args.get("code"):
        spotify_object.auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not spotify_object.validate(cache_handler=cache_handler):
        auth_url = spotify_object.auth_manager.get_authorize_url()
        return render_template('login.html', title='SignIn',auth_url=auth_url)

    sp = spotify_object.spotify_object()
    spotify_object.user_id = sp.me()["id"]
    return redirect('/tracks/top/')

@app.route('/sign_out')
def sign_out():
    try:
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('templates/static', path)

if __name__ == '__main__':
    spotify_object = spotify_v1.SpotifyClientAPI(os.getenv('SPOTIPY_CLIENT_ID'), os.getenv('SPOTIPY_CLIENT_SECRET'))
    
    app.config["spotify_client_object"] = spotify_object
    app.run(debug=True)
