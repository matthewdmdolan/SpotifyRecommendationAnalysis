import time
import pandas as pd
import requests
import spotipy
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from spotipy.oauth2 import SpotifyClientCredentials

import cfg

#initialising API call parameters
client_id = '6f7b976676cc46b5ab5be6667665957f'  # insert your client id
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

# Function to fetch data
def fetch_data():
    # Retrieve playlist_id by getting the Spotify URI of any playlist
    playlist_id = "https://open.spotify.com/playlist/62VOK2lfIEFF5GOjwE6XYj?si=cbc1640acceb44ee"

    def get_playlist_tracks(playlist_id):
        results = sp.playlist_items(playlist_id)
        tracks = results['items']
        while results['next']:
            time.sleep(3)  # Add a delay of 0.1 seconds between each request
            results = sp.next(results)
            tracks.extend(results['items'])
        return tracks

    # Now we can use this function to get all the tracks from the playlist.
    tracks = get_playlist_tracks(playlist_id)

    # The rest of your script remains the same, just replace the ids generation part
    ids = [item['track']['id'] for item in tracks]

    song_meta = {
        "id": [],
        "album": [],
        "name": [],
        "artist": [],
        "explicit": [],
        "popularity": [],
    }

    for song_id in ids:
        try:
            # get song's meta data
            meta = sp.track(song_id)

            # song id
            song_meta["id"].append(song_id)

            # album name
            album = meta["album"]["name"]
            song_meta["album"].append(album)

            # song name
            song = meta["name"]
            song_meta["name"].append(song)

            # artists name
            s = ", "
            artist = s.join([singer_name["name"] for singer_name in meta["artists"]])
            song_meta["artist"].append(artist)

            # explicit: lyrics could be considered offensive or unsuitable for children
            explicit = meta["explicit"]
            song_meta["explicit"].append(explicit)

            # song popularity
            popularity = meta["popularity"]
            song_meta["popularity"].append(popularity)

            # Pause for a short period to avoid hitting rate limits
            time.sleep(1)

        except Exception as e:
            print(f"Error processing song_id {song_id}: {e}")

    song_meta_df = pd.DataFrame.from_dict(song_meta)

    # check the song feature
    features = sp.audio_features(song_meta["id"])
    # change dictionary to dataframe
    features_df = pd.DataFrame.from_dict(features)

    # convert milliseconds to mins
    features_df["duration_ms"] = features_df["duration_ms"] / 60000

    # combine two dataframe
    final_df = song_meta_df.merge(features_df)



    # write the final DataFrame to a CSV file
    final_df.to_csv("spotify_data.csv", index=False)

# Code to fetch data if this script is directly run
if __name__ == "__main__":
    fetch_data()
