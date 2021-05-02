from flask import Blueprint,redirect,current_app,session, render_template,send_from_directory

user_routes = Blueprint('user_routes',__name__)
caches_folder = './.spotify_caches/'

def session_cache_path():
    return caches_folder + session.get('uuid')

def spotify_class_object():
    return current_app.config["spotify_client_object"]

@user_routes.route('/profile/')
def current_user():
    cache_handler = spotify_class_object().authenticate(cache_path=session_cache_path())

    if not spotify_class_object().validate(cache_handler=cache_handler):
        return redirect('/')

    sp = spotify_class_object().spotify_object()
    current_profile = sp.current_user()
    return render_template('profile.html', title='Profile', active_page='profile',username=sp.me()["display_name"], user=current_profile)


@user_routes.route('/<mode>/static/<path:path>')
def send_static(mode, path):
    return send_from_directory('templates/static', path)
