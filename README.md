# spotipy-api-k-means-song-recommendation-tool

The project was born out of my love for a long-running disco playlist that I've made over the years. The problem is, as the playlist has grown,  the recommendations by the app have become more diffuse and less meaningful. Therefore, I've reached a point where I now probably have to break 
it down into smaller playlists in order to keep the recommendation system useful. 

The analysis uses Spotipy's API to gain information on song metadata for each song within the playlist. As shown below:

Acousticness: Measure of acoustic quality (1.0 being most acoustic).
Danceability: How suitable the track is for dancing (1.0 being most danceable).
Energy: Perceptual measure of intensity and activity (1.0 being most energetic).
Instrumentalness: Likelihood of the track being instrumental (1.0 being most likely).
Key: Overall key of the track (integer values representing pitch classes).
Liveness: Detects the presence of an audience (1.0 represents a live track).
Loudness: Overall loudness of a track in decibels (dB).
Speechiness: Presence of spoken words (1.0 being talk, like a podcast). 
Tempo: Speed or pace of a given piece in BPM.
Time_Signature: Beats per measure of a track.
Valence: Musical positiveness (1.0 being most positive).


Firstly, the mean for each metadata attribute is plotted in order to provide a profile analysis of the playlist. Following some transformations, 
I decided to use a K-means analysis to try and identify sub-groups within the playlist, so I can get back to the glory years of being treated to lovely obscure disco tracks every time I go for a walk. 
The EDA and K-means analysis are both visualised using streamlit. Moreover, apache Airflow is utilised to orchestrate API calls and transformations.

 

 
