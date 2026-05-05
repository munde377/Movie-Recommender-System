import pickle
import streamlit as st
import requests

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Center Container */
.main-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 40px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 40px rgba(0,0,0,0.5);
    text-align: center;
    margin-top: 50px;
}

/* Title */
.title {
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    color: #94a3b8;
    margin-bottom: 30px;
}

/* Button Style */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 250px;
    font-size: 16px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px rgba(99,102,241,0.7);
}

/* Movie Card */
.movie-card {
    text-align: center;
}

.movie-title {
    font-size: 14px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------- HEADER UI --------------------
st.markdown("""
<div class="main-container">
    <div class="title">🎬 Movie Recommender System</div>
    <div class="subtitle">Discover your next favorite movie</div>
</div>
""", unsafe_allow_html=True)

# -------------------- LOAD DATA --------------------
movies = pickle.load(open("movie.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# -------------------- FUNCTIONS --------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "https://via.placeholder.com/500"
        data = response.json()
        if data.get('poster_path') is None:
            return "https://via.placeholder.com/500"
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except:
        return "https://via.placeholder.com/500"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# -------------------- INPUT UI --------------------
st.markdown("<br>", unsafe_allow_html=True)

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "🎥 Type or select a movie",
    movie_list
)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------- BUTTON --------------------
if st.button("✨ Show Recommendation"):

    names, posters = recommend(selected_movie)

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)