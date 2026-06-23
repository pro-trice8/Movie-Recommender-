import streamlit as st
import pickle 
import requests
import streamlit.components.v1 as components

# cache data loads for efficiency
def load_data():
    movies = pickle.load(open("movie_list.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    movies_list = movies["title"].values
    return movies, similarity, movies_list

movies, similarity, movies_list = load_data()

st.title("🎬 Movie Recommendation System")
st.markdown("Choose a movie from the sidebar and get five similar titles with their posters.")

# --- custom styling -------------------------------------------------
st.markdown(
    """
    <style>
    /* app background and font */
    .stApp {
        background-color: #f0f2f6;
        color: #333;
    }
    /* sidebar styling */
    .css-1d391kg { /* container around sidebar buttons/inputs */
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
    }
    /* title style */
    .streamlit-expanderHeader {
        color: #4a148c;
    }
    /* main title font */
    h1 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        color: #000000; /* black title */
    }
    /* button styling */
    .stButton>button {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
        background-color: #4a148c;
        color: white;
    }
    /* movie card container */
    .movie-card {
        display: inline-block;
        vertical-align: top;
        margin: 0.5rem;
        width: 220px;
        text-align: center;
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #ffffff;
        color: #000 !important; /* enforce black text */
    }
    .movie-card *,
    .movie-card h3,
    .movie-card h2,
    .movie-card h1,
    .movie-card p,
    .movie-card div,
    .movie-card span {
        color: #000 !important;
        background-color: #ffffff !important;
    }
    .movie-card img {
        display: block;
        margin: 0 auto;
        max-height: 300px;
        width: auto;
    }
    .movie-overview {
        font-size: 0.95rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
        color: #000000 !important;
        background-color: #ffffff;
        line-height: 1.5;
        margin-top: 0.5rem;
        padding: 0.35rem 0.45rem;
        border-radius: 4px;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------

# TMDB configuration — read the key from Streamlit secrets (keeps it private)
API_KEY = "8013126b74d7fcf75a65915317ba6f1d"

def fetch_movie_details(movie_id):
    """Return TMDB poster URL and overview for a given movie ID."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()
    poster_path = data.get("poster_path")
    poster = "https://image.tmdb.org/t/p/w500" + poster_path if poster_path else ""
    overview = data.get("overview", "")
    return poster, overview

# sidebar inputs
selectvalue = st.sidebar.selectbox("Select movie", movies_list)


def recommend(movie):
  index = movies[movies['title']==movie].index[0]
  distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
  recommend_movies = []
  for i in distance[1:6]:
    recommend_movies.append(movies_list[i[0]])
  return recommend_movies


if st.sidebar.button("Show Recommend"):
    recommended = recommend(selectvalue)
    # fetch posters and overviews for each recommendation
    details = []  # list of (poster, overview)
    for title in recommended:
        movie_id = movies[movies["title"] == title]["id"].values[0]
        details.append(fetch_movie_details(movie_id))

    cols = st.columns(len(recommended))  # responsive columns
    for col, title, (poster, overview) in zip(cols, recommended, details):
        with col:
            st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
            # render title manually so we can control color explicitly
            st.markdown(f"<h3 style='color:#000; margin-top:0;'>{title}</h3>", unsafe_allow_html=True)
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.write("No poster available")
            if overview:
                st.markdown(f"<div class='movie-overview' style='color:#000000 !important; background-color:#ffffff !important; font-weight:600;'>{overview}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)