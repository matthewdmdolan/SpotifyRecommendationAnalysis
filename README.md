# spotipy-api-k-means-song-recommendation-tool

The project was born out of my love for a long-running disco playlist that I've made over the years. The problem is, as the playlist has grown, 
the recommendations by the app have become more diffuse and less meaningful. Therefore, I've reached a point where I now probably have to break it down 
into smaller playlists in order to keep the recommendation system useful. 

As a result, I decided to use a k-means analysis to try and identify sub-groups within the playlist so I can get back to the glory years of being treated to lovely obscure disco tracks every time I go for a walk. 

The analysis uses Spotipy's API to gain information on song metadata for each song within the playlist. 

Firstly, the mean for each song attribute is plotted in order to provide a basis for future recommendations recommendations 
