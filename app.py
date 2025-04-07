import streamlit as st
import pandas as pd
import pickle
import nltk
nltk.download('punkt')  # Or any other resource you’re using like 'stopwords'
from model import recommend  # only import what's needed!

# Load cleaned dataset
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_spotify_data.csv")

# Load precomputed TF-IDF vectorizer and matrix
@st.cache_resource
def load_model():
    with open("tfidf_vectorizer.pkl", "rb") as f:
        tf_id = pickle.load(f)
    with open("tfidf_matrix.pkl", "rb") as f:
        tf_matrix = pickle.load(f)
    return tf_id, tf_matrix

# ---------------- Streamlit App UI -------------------

st.set_page_config(page_title=" 🎧 Music Recommender", layout="wide")
st.markdown("<h1 style='color:#f92672;'>🎵 Music Recommender</h1>", unsafe_allow_html=True)
st.write("Enter a mood, feeling, or some lyrics, and get song suggestions!")

input_text = st.text_area("Your Input Text", "")

if st.button("Recommend Songs"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("🎶 Finding the best songs for you..."):
            ds = load_data()
            tf_id, tf_matrix = load_model()
            results = recommend(input_text, ds, tf_id, tf_matrix)
        if results:
            st.success("Here are your recommendations:")
            for song in results:
                col1, col2 = st.columns([1, 4])
                with col1:
                    if song['image_url']:
                        st.image(song['image_url'], width=120)
                with col2:
                    st.markdown(f"**{song['name']}** by *{song['artist']}*")
                    st.markdown(f"[🎧 Listen on Spotify]({song['external_url']})")
                    if song['preview_url']:
                        st.audio(song['preview_url'], format="audio/mp3")
        else:
            st.error("No matching songs found.")
# ---------------- Footer -------------------
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 10px 0;
            background-color: #0e1117;
            color: gray;
            text-align: center;
            font-size: 0.85rem;
            z-index: 100;
        }
    </style>
    <div class="footer">
         Made with ❤️ by <strong>Anshul</strong> 🎧🎶
    </div>
""", unsafe_allow_html=True)

