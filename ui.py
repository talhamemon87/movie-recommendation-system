import streamlit as st
from data_loader import load_data
from recommender import recommend_movies
from ai_model import build_similarity
from poster import fetch_movie_details

# ================================
# 🎨 PAGE CONFIG (Netflix style)
# ================================
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS (Netflix theme)
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
        color: white;
    }
    .stApp {
        background-color: #0f0f0f;
    }
    h1, h2, h3 {
        color: #E50914;
    }
    .movie-card {
        background-color: #1c1c1c;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ================================
# 📂 LOAD DATA
# ================================
movies = load_data()
similarity = build_similarity(movies)

# ================================
# 🎭 EXTRACT GENRES
# ================================
all_genres = set()
for g in movies['genres']:
    for genre in g.split('|'):
        all_genres.add(genre)

all_genres = sorted(list(all_genres))

# ================================
# 🎬 TITLE
# ================================
st.title("🎬 Movie Recommender")

# ================================
# 🎛️ FILTER SECTION
# ================================
st.sidebar.header("🎯 Filter Options")

selected_genres = st.sidebar.multiselect("Select Genres", all_genres)

min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5)
min_votes = st.sidebar.slider("Minimum Votes", 0, 500, 50)
min_year = st.sidebar.slider("Start Year", 1900, 2025, 2000)
max_year = st.sidebar.slider("End Year", 1900, 2025, 2020)
top_n = st.sidebar.slider("Number of Movies", 1, 20, 6)

# ================================
# 🔘 BUTTON
# ================================
if st.sidebar.button("🎬 Recommend"):

    if not selected_genres:
        st.warning("Please select at least one genre")
    else:
        results = recommend_movies(
            movies, selected_genres, min_rating, min_votes, min_year, max_year, top_n
        )

        st.subheader("🎯 Recommended Movies")

        if results.empty:
            st.error("No movies found")
        else:
            cols = st.columns(3)

            for i, (_, row) in enumerate(results.iterrows()):

                poster, description = fetch_movie_details(row['title'])

                with cols[i % 3]:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)

                    if poster:
                        st.image(poster)

                    st.markdown(f"### {row['title']}")
                    st.write(f"⭐ {round(row['avg_rating'],2)}")

                    if description:
                        st.caption(description[:150] + "...")

                    st.markdown('</div>', unsafe_allow_html=True)

# ================================
# 🤖 AI SECTION
# ================================
st.sidebar.header("🤖 AI Recommendation")

movie_name = st.sidebar.text_input("Enter Movie Name")

if st.sidebar.button("Find Similar"):

    if movie_name not in movies['title'].values:
        st.error("Movie not found")
    else:
        idx = movies[movies['title'] == movie_name].index[0]
        distances = similarity[idx]

        movie_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:7]

        st.subheader("🤖 Similar Movies")

        cols = st.columns(3)

        for i, m in enumerate(movie_list):
            movie = movies.iloc[m[0]]

            poster, description = fetch_movie_details(movie['title'])

            with cols[i % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)

                if poster:
                    st.image(poster)

                st.markdown(f"### {movie['title']}")

                if description:
                    st.caption(description[:150] + "...")

                st.markdown('</div>', unsafe_allow_html=True)