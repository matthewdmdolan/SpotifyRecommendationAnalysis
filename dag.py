from airflow import DAG
from airflow.utils.dates import datetime
import pendulum
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from sklearn.preprocessing import MinMaxScaler
import cfg
import time
from datetime import datetime, timedelta

# Set the UTC timezone
local_tz = pendulum.timezone("UTC")

# Spotify API credentials
cfg = {
    "api_key": cfg.api_key
}

# Define the timezone
local_tz = pendulum.timezone("GMT")  # Replace "your_timezone" with your desired timezone

# Define the DAG
dag = DAG(
    dag_id="process-spotify-playlist",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60)
)


def ProcessPlaylistData():
    # Task to get playlist data
    @task
    def get_data():
        ids = []
        for item in results["tracks"]["items"]:
            track = item["track"]["id"]
            ids.append(track)

        song_meta = {
            "id": [],
            "album": [],
            "name": [],
            "artist": [],
            "explicit": [],
            "popularity": [],
        }

        for song_id in ids:
            meta = sp.track(song_id)  # Get song's meta data

            song_meta["id"].append(song_id)
            song_meta["album"].append(meta["album"]["name"])
            song_meta["name"].append(meta["name"])
            artist = ", ".join([singer_name["name"] for singer_name in meta["artists"]])
            song_meta["artist"].append(artist)
            song_meta["explicit"].append(meta["explicit"])
            song_meta["popularity"].append(meta["popularity"])

        song_meta_df = pd.DataFrame.from_dict(song_meta)
        return song_meta_df

    # Task to get audio features for songs
    @task
    def get_audio_features(song_meta_df):
        song_ids = song_meta_df["id"].to_list()
        features = sp.audio_features(song_ids)
        features_df = pd.DataFrame.from_dict(features)
        features_df["duration_ms"] = features_df["duration_ms"] / 60000
        final_df = song_meta_df.merge(features_df)
        return final_df

    # Task for data pre-processing
    @task
    def preprocess_data(final_df):
        scaler = MinMaxScaler()
        music_features = final_df[
            [
                "danceability",
                "energy",
                "loudness",
                "speechiness",
                "acousticness",
                "instrumentalness",
                "liveness",
                "valence",
                "tempo",
                "duration_ms",
            ]
        ]
        music_features.loc[:] = scaler.fit_transform(music_features.loc[:])
        return music_features

    # Task to plot radial chart
    @task
    def plot_radial_chart(music_features):
        fig = plt.figure(figsize=(10, 10))
        categories = list(music_features.columns)
        N = len(categories)
        value = list(music_features.mean())
        value += value[:1]
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        plt.polar(angles, value, color="red")
        plt.fill(angles, value, alpha=0.7, color="purple")
        plt.title("Playlist Audio Features", size=20, y=1.05)
        plt.xticks(angles[:-1], categories, size=15, color="purple")
        plt.yticks(color="black", size=15)
        plt.show()

    # Define the tasks
    process_spotify_playlist_task = PythonOperator(
        task_id="process_spotify_playlist",
        python_callable=process_spotify_playlist,
        dag=dag
    )

    get_audio_features_task = PythonOperator(
        task_id="get_audio_features",
        python_callable=get_audio_features,
        dag=dag
    )

    plot_radial_chart_task = PythonOperator(
        task_id="plot_radial_chart",
        python_callable=plot_radial_chart,
        dag=dag
    )

    # Define the task dependencies
    process_spotify_playlist_task >> get_audio_features_task >> plot_radial_chart_task



