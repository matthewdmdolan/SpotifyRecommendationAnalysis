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
from api import music_features


# Radar Chart with several heads from DataFrame
# Creating Radar Chart
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
# plt.show()