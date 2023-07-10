import json
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from math import pi
import cfg
import time
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from spotipy.oauth2 import SpotifyClientCredentials
import tekore as tk

def authorize():
 CLIENT_ID = "6f7b976676cc46b5ab5be6667665957f"
 CLIENT_SECRET = cfg.api_key
 app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
 return tk.Spotify(app_token)

#initialising API call parameters
client_id =  # insert your client id
client_secret = cfg.api_key  # insert your client secret id here
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

# Create a custom session
session = requests.Session()
retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 502 ])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Create a Spotipy client with our custom session
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_session=session)

def fetch_data():
    # Retrieve playlist_id by getting the Spotify URI of any playlist
    playlist_id = "https://open.spotify.com/playlist/62VOK2lfIEFF5GOjwE6XYj?si=cbc1640acceb44ee"
    results = sp.playlist(playlist_id)

    # added in sleep to avoid the spotify api
    def get_playlist_tracks(playlist_id):
        results = sp.playlist_items(playlist_id)
        tracks = results['items']
        retries = 0
        while results['next']:
            time.sleep(3)  # Add a delay of 0.1 seconds between each request
            results = sp.next(results)
            tracks.extend(results['items'])
            return tracks

    # Now we can use this function to get all the tracks from the playlist.
    tracks = get_playlist_tracks(playlist_id)

    # The rest of your script remains the same, just replace the ids generation part
    ids = [item['track']['id'] for item in tracks]