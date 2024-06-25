from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'Cookie Cream'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except Exception as e:
        print(f"Wanna come in? Plz 🙏 login. Error: {e}")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iter*50)['items']
        iter += 1
        for item in items:
            track = item['track']
            song_name = f"{track['name']} - {track['artists'][0]['name']}"
            all_songs.append(song_name)
        if len(items) < 50:
            break

    print(all_songs[0])
    df = pd.DataFrame(all_songs, columns=["song names"])
    df.to_csv('songs.csv', index=False)
    return "done"

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("Token info not found in session.")
    now = int(time.time())
    
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-library-read")

if __name__ == '__main__':
    app.run(debug=True)
