# Movie Recommendation System

This is a mini ML project that recommends movies from Hollywood, Bollywood, and Tollywood using:

- `FastAPI` for the backend API
- `Streamlit` for the frontend UI
- `TF-IDF Vectorizer` for converting movie text data into numbers
- `Cosine Similarity` for finding similar movies

## Project Structure

```text
project_3/
|-- app/
|   |-- api/
|   |   `-- main.py
|   |-- data/
|   |   `-- movies.json
|   `-- ml/
|       `-- recommender.py
|-- streamlit_app.py
|-- requirements.txt
`-- README.md
```

## How The Recommendation System Works

This is a **content-based recommendation system**.

Instead of using user ratings, it compares movie content:

- title
- industry
- language
- director
- genres
- mood
- cast
- overview

### Step 1: Dataset

The dataset is stored in `app/data/movies.json`.

Each movie has:

- title
- language
- industry
- genres
- mood
- cast
- director
- overview
- rating
- poster URL

### Step 2: Feature Engineering

In `app/ml/recommender.py`, all important text fields are merged into one single text string called `feature_text`.

Example idea:

```python
feature_text = title + industry + language + director + overview + genres + mood + cast
```

This helps the ML model understand that movies with similar story style, genre, cast, or mood should be close to each other.

### Step 3: TF-IDF Vectorization

`TfidfVectorizer` converts text into numeric vectors.

Why we use it:

- It gives importance to meaningful words
- It reduces the weight of very common words
- It helps represent every movie as a machine-readable vector

### Step 4: Cosine Similarity

After converting all movies into vectors, cosine similarity is used.

This calculates how close two movie vectors are.

- score near `1` = very similar
- score near `0` = not very similar

So if you choose `Inception`, the system finds other movies with similar story, mood, genre, or style.

## FastAPI Backend Explanation

File: `app/api/main.py`

### Main parts

1. `FastAPI()` creates the API application.
2. `CORSMiddleware` allows Streamlit to call the API.
3. `/movies` endpoint returns all movie records.
4. `/recommend` endpoint returns recommendations for a selected movie.

### Important API routes

- `GET /`
  - Checks if API is running
- `GET /health`
  - Health check endpoint
- `GET /movies`
  - Returns movie list
- `GET /recommend?title=Inception&top_k=5`
  - Returns similar movies

## Recommender Code Explanation

File: `app/ml/recommender.py`

### `MovieRecommender` class

This class handles the ML logic.

#### `__init__()`

- loads dataset
- creates a dataframe
- builds combined feature text
- applies TF-IDF
- calculates cosine similarity matrix

#### `_load_movies()`

- reads JSON file
- creates a pandas dataframe
- creates lowercase titles for easy searching
- creates backup poster image URLs

#### `_build_feature_text()`

- combines all useful movie fields into one text sentence
- this becomes the input to the vectorizer

#### `list_movies()`

- returns all movies
- can filter by industry or language

#### `recommend()`

- finds the selected movie
- checks similarity scores with all other movies
- sorts from highest to lowest similarity
- filters by industry/language if needed
- returns top recommendations

## Streamlit UI Explanation

File: `streamlit_app.py`

### What this file does

- connects to FastAPI using the `requests` library
- loads all movies from backend
- shows a modern dashboard UI
- lets user choose:
  - movie title
  - industry
  - language
  - number of recommendations
- displays selected movie and recommended movie cards

### UI features

- dark cinematic gradient background
- custom fonts
- poster cards
- similarity score chip
- sidebar controls
- poster fallback if image link fails

## How To Run

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Start FastAPI server

```bash
uvicorn app.api.main:app --reload
```

Open API docs:

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 3. Start Streamlit app

Open a second terminal and run:

```bash
streamlit run streamlit_app.py
```

Streamlit usually opens here:

- [http://localhost:8501](http://localhost:8501)

## Example Output Flow

1. Select `3 Idiots`
2. Click `Recommend Movies`
3. Backend computes similarity scores
4. UI shows similar films like feel-good, friendship, drama, and inspirational movies

## Why This Is Good For An ML Project

- shows ML concept clearly
- uses feature engineering
- uses vectorization
- uses similarity-based recommendation
- has backend + frontend
- has explainable logic
- easy to demo in college/project viva

## Future Improvements

- add larger CSV dataset
- use TMDb API for live posters and descriptions
- add collaborative filtering
- add user login and watchlist
- add sentiment analysis on reviews
- deploy on Render, Railway, or Hugging Face Spaces
