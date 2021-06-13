from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd




def getPlaylists(user, name, sp):
    id = ""
    playlists = sp.user_playlists(user)
    for list in playlists['items']:
        if list['name'] == name:
            id = list['id']
    return id

def customTrackExtender(user, id, sp):
    results = sp.user_playlist_tracks(user, id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def getPlaylistTracks(user, id, sp):
    name = []
    artist = []
    ids = []
    tracks = customTrackExtender(user, id, sp)
    for track in tracks:
        name.append(track['track']['name'])
        ids.append(track['track']['id'])
        artist.append(track['track']['artists'][0]['name'])
    tracks = pd.DataFrame({'name': name,'id': ids, 'artist':artist})
    return(tracks)

def getTrackFeatures(ids, sp):
    dance = []
    energy = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    tempo = []
    valence = []
    id1 = []
    for id in ids:
        features = sp.audio_features(id)[0]
        dance.append(features['danceability'])
        energy.append(features['energy'])
        key.append(features['key'])
        loudness.append(features['loudness'])
        mode.append(features['mode'])
        speechiness.append(features['speechiness'])
        acousticness.append(features['acousticness'])
        instrumentalness.append(features['instrumentalness'])
        liveness.append(features['liveness'])
        tempo.append(features['tempo'])
        valence.append(features['valence'])
        id1.append(features['id'])
    feature_df = pd.DataFrame({"danceability":dance, "energy": energy,
                               "key": key, 'loudness':loudness,
                               "mode":mode, 'speechiness':speechiness,
                               'acousticness':acousticness, 'instrumentalness':instrumentalness,
                               'liveness':liveness, 'tempo':tempo,
                               'valence':valence, 'id':id1})
    return(feature_df)

if __name__ == "__main__":
    load_dotenv()

    client = os.getenv("ID")
    secret = os.getenv("SECRET")

    client_credentials_manager = SpotifyClientCredentials(client_id=client, client_secret=secret)
    token = os.getenv("TOKEN")

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    id = getPlaylists('hufinger18', 'Shit Kickin Country', sp)

    list = getPlaylistTracks('hufinger18', id, sp)

    features = getTrackFeatures(list['id'], sp)

    joined = pd.merge(list, features)
    print(joined.head())

