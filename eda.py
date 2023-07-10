from math import pi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
# from pygments.lexers import go
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import api
from matplotlib.ticker import FixedLocator

# Set global figure size and dpi settings
plt.rcParams['figure.figsize'] = (3, 32)
plt.rcParams['figure.dpi'] = 30

# CLI to run streamlit: streamlit run your_script.py [-- script args]

"""This way, when you import api.py in eda.py, it won't automatically run the data fetching code. Instead, you manually call api.fetch_data() when you're ready to fetch the data.
This also allows you to run api.py on its own to fetch data without doing any of the EDA, because fetch_data() will be called if api.py is the script that's directly run.
"""


def main():
    # Fetch the data
    data = api.fetch_data()


# Data to read CSV file from directory
def read_spotify_data(file_name):
    df = pd.read_csv(file_name)
    return df


# reading in data
music_features = read_spotify_data('spotify_data.csv')
print(music_features)

# no nulls identified which is great
music_features.info()

# Let's consider only numeric columns from the dataframe
numeric_columns = music_features.select_dtypes(include=np.number)

# initiating scaler for k means analysis
# TRY WITH DIFFERENT SCALER?
min_max_scaler = MinMaxScaler()
scaled_data = min_max_scaler.fit_transform(numeric_columns)
scaled_df = pd.DataFrame(scaled_data, columns=numeric_columns.columns)
print(scaled_df)

selected_columns = list(scaled_df.columns)
value = [np.mean(scaled_df[field]) for field in scaled_df]

# Create a dictionary by pairing column names with values
data_dict = {'attribute': selected_columns, 'value': value}
df_mean = pd.DataFrame(data_dict)
print(df_mean)

# Get the total number of categories
N = len(df_mean)
print(N)
# Calculate the angle for each axis on the radar chart
angles = [n / float(N) * 2 * pi for n in range(N)]

# Add the first angle to the end of the list to close the shape
angles += angles[:1]

# Create a new figure for the plot
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, polar=True)
ax.plot(angles[1:], df_mean['value'], linewidth=1, linestyle='solid')
ax.fill(angles[1:], df_mean['value'], 'b', alpha=0.1)

# Set the attribute names as tick labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(df_mean['attribute'])

# Set the FixedLocator for tick locations
ax.xaxis.set_major_locator(FixedLocator(angles[:-1]))

# Set the title of the plot
ax.set_title("Mean Scores For Each Meta Data Attribute Across All Songs ")

# Display the plot in Streamlit
st.pyplot(fig)

# Perform K-means clustering for different values of k
k_values = range(1, 10)
inertias = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_df)
    inertias.append(kmeans.inertia_)

# Plot the elbow curve as a line graph
plt.plot(k_values, inertias, marker='o', linestyle='--')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method')

##plt.show()

# Display the plot in Streamlit
st.pyplot(plt)

# replace with optimal k from plot
##NEED TO WORK OUT HOW TO DO THIS PROGRAMATICALLY
# optimal_k = 3

# Get the cluster assignments for each data point
cluster_assignments = kmeans.labels_
# Add the cluster assignments back into the original DataFrame
scaled_df['Cluster'] = cluster_assignments
# Print the DataFrame with the new 'Cluster' column
cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=scaled_df.columns[:-1])
print(cluster_centers)
# Plot all columns using a pair plot
# sns.pairplot(scaled_df, hue='Cluster', palette='Set1')
# # Display the plot in Streamlit
# st.pyplot(plt)

# List all your features
features = scaled_df.columns[:-1]  # Assumes 'Cluster' is the last column
for feature in features:
    plt.figure(figsize=(10, 6))  # Adjust size as needed
    sns.boxplot(x='Cluster', y=feature, data=scaled_df)
    plt.title('Boxplot of ' + feature + ' for each cluster')
    st.pyplot(plt)

# Looking at count of songs in each cluster
df_cluster_distribution = scaled_df['Cluster'].value_counts()
print(df_cluster_distribution)
# plt.pyplot.bar(x = 'Cluster', scaled_df['value_counts'),
#                                         'df_cluster_distribution)

angles = list(scaled_df[
                  ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness',
                   'tempo', 'valence']].columns)

angles.append(angles[0])
layoutdict = dict(
    radialaxis=dict(
        visible=True,
        range=[0, 1]
    ))

fig = go.Figure()

for k in k_values:
    subset = scaled_df[scaled_df['Cluster'] == k]
    data = [np.mean(subset[col]) for col in subset[
        ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
         'valence']].columns]
    data.append(data[0])
    fig.add_trace(go.Scatterpolar(
        r=data,
        theta=angles,
        fill='toself',
        name="Cluster " + str(k)))

fig.update_layout(
    polar=layoutdict,
    showlegend=True, template='plotly_dark')

st.plotly_chart(fig)

# plt.pyplot.bar(x, height, width=0.8, bottom=None, *, align='center', data=None, **kwargs)


with st.sidebar:
    add_radio = st.radio(
        "...",
        ("Home", "EDA", "ML")
    )

# [theme]
# base = "dark"
# primaryColor = "#2F4F4F"
# font= "arial"


##code that allows us to import EDA
if __name__ == "__main__":
    main()
