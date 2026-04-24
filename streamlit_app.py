from __future__ import annotations

from typing import Any
import time
import requests
import streamlit as st

from app.ml.recommender import recommender


API_URL = "https://movie-recommendation-system-v4an.onrender.com"

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
)


def load_movies() -> list[dict[str, Any]]:
    for _ in range(2):
        try:
            response = requests.get(f"{API_URL}/movies", timeout=30)
            response.raise_for_status()
            return response.json()["movies"]
        except requests.RequestException:
            time.sleep(3)
    raise requests.RequestException("API not responding")


def load_recommendations(title: str, top_k: int, industry: str, language: str) -> dict[str, Any]:
    for _ in range(2):
        try:
            response = requests.post(
                f"{API_URL}/recommend",
                json={
                    "title": title,
                    "top_k": top_k,
                    "industry": industry,
                    "language": language,
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            time.sleep(3)
    raise requests.RequestException("API failed")


def load_movies_with_fallback() -> tuple[list[dict[str, Any]], bool]:
    try:
        return load_movies(), True
    except requests.RequestException:
        return recommender.list_movies(), False


def load_recommendations_with_fallback(
    title: str,
    top_k: int,
    industry: str,
    language: str,
) -> tuple[dict[str, Any], bool]:
    try:
        return load_recommendations(
            title=title,
            top_k=top_k,
            industry=industry,
            language=language,
        ), True
    except requests.RequestException:
        st.warning("⚡ API not reachable, using fallback")

        return recommender.recommend(
            title=title,
            top_k=top_k,
            industry=industry,
            language=language,
        ), False


st.title("🎬 CineMatch AI")
st.info("⚡ First request may take 20–30 seconds (server waking up)")

movies, api_available = load_movies_with_fallback()

if not api_available:
    st.warning("⚡ Using local fallback (API temporarily unavailable)")

movie_titles = sorted(movie["title"] for movie in movies)
industries = ["All"] + sorted({movie["industry"] for movie in movies})
languages = ["All"] + sorted({movie["language"] for movie in movies})

with st.sidebar:
    st.header("Controls")
    selected_title = st.selectbox("Movie", movie_titles)
    selected_industry = st.selectbox("Industry", industries)
    selected_language = st.selectbox("Language", languages)
    top_k = st.slider("Recommendations", 3, 8, 5)
    recommend_clicked = st.button("Recommend")


if recommend_clicked:
    payload, from_api = load_recommendations_with_fallback(
        title=selected_title,
        top_k=top_k,
        industry=selected_industry,
        language=selected_language,
    )

    if not from_api:
        st.info("Using fallback recommender")

    st.subheader("Selected Movie")
    st.write(payload["selected_movie"])

    st.subheader("Recommendations")
    for movie in payload["recommendations"]:
        st.write(movie)

else:
    st.subheader("Movie Library")
    for movie in movies[:6]:
        st.write(movie)