# model.py

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

nltk.download('punkt')
stemmer = PorterStemmer()

# Clean input text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n', ' ', text)
    return text

# Tokenize and stem
def tokenize(text):
    tokens = word_tokenize(text)
    return " ".join([stemmer.stem(token) for token in tokens])

# Spotify setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="902e0ca28f86404bb58a0f21945d8781",
    client_secret="e292c204818d4ffc9c44d97304575e18"
))

def get_spotify_preview(song_title):
    results = sp.search(q=song_title, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        return {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'preview_url': track['preview_url'],
            'external_url': track['external_urls']['spotify'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
        }
    return None

# Recommend similar songs
def recommend(text, ds, tf_id, tf_matrix):
    cleaned = clean_text(text)
    tokenized = tokenize(cleaned)
    text_vector = tf_id.transform([tokenized])
    cosine_sim = cosine_similarity(text_vector, tf_matrix).flatten()
    similar_indices = cosine_sim.argsort()[-11:][::-1]

    recommendations = []
    for idx in similar_indices[1:]:  # Skip the input itself
        song_title = ds.iloc[idx]['song']
        info = get_spotify_preview(song_title)
        if info:
            recommendations.append(info)
    return recommendations
