# 🎬 Movie Recommendation System

A content-based movie recommender that suggests five similar films for any
selected title, complete with posters and plot overviews fetched live from
the TMDB API. Built with Python and Streamlit.

## How it works

The app uses **content-based filtering**. Each movie is represented as a
vector built from its metadata (genres, keywords, cast, and overview), and
similarity between movies is measured using **cosine similarity**. When you
pick a movie, the app finds the five closest vectors and returns them as
recommendations.

## Features

- Select any movie from a searchable dropdown.
- Get five content-similar recommendations instantly.
- Live poster and plot overview for each recommendation via the TMDB API.
- Clean, custom-styled card layout.

## Tech stack

Python, Pandas, scikit-learn (CountVectorizer + cosine similarity),
Streamlit, TMDB API.

## Project structure

- `app.py` — the Streamlit application.
- `movie_list.pkl` — preprocessed movie metadata.
- `data.csv` — source movie data.
- `generate_similarity.py` — regenerates the similarity matrix (see below).

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/pro-trice8/Movie-Recommender-.git
cd Movie-Recommender-

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the similarity matrix (not included in repo due to size)
python generate_similarity.py
```

## API key

The app fetches posters and overviews from TMDB. You need a free TMDB API key.

Locally, create a file `.streamlit/secrets.toml` with:

```toml
API_KEY = "your_tmdb_api_key_here"
```

This file is gitignored and never committed. For Streamlit Cloud deployment,
paste the same line into the app's **Secrets** box in settings.

## Note on the similarity matrix

`similarity.pkl` is a large precomputed file (the full movie-to-movie
similarity matrix) and is not committed to the repo. Run
`generate_similarity.py` once after cloning to build it locally.

## Run it

```bash
streamlit run app.py
```