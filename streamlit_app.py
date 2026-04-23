from __future__ import annotations

from typing import Any

import requests
import streamlit as st

from app.ml.recommender import recommender


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
)


def load_movies() -> list[dict[str, Any]]:
    response = requests.get(f"{API_URL}/movies", timeout=20)
    response.raise_for_status()
    return response.json()["movies"]


def load_recommendations(title: str, top_k: int, industry: str, language: str) -> dict[str, Any]:
    response = requests.get(
        f"{API_URL}/recommend",
        params={
            "title": title,
            "top_k": top_k,
            "industry": industry,
            "language": language,
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


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
        return load_recommendations(title=title, top_k=top_k, industry=industry, language=language), True
    except requests.RequestException:
        return recommender.recommend(title=title, top_k=top_k, industry=industry, language=language), False


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Manrope:wght@400;500;700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Manrope', sans-serif;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(251, 191, 36, 0.18), transparent 28%),
                    radial-gradient(circle at top right, rgba(239, 68, 68, 0.16), transparent 24%),
                    linear-gradient(135deg, #020617 0%, #0f172a 52%, #111827 100%);
                color: #e2e8f0;
            }

            .hero-card {
                padding: 2rem;
                border: 1px solid rgba(148, 163, 184, 0.25);
                border-radius: 28px;
                background: linear-gradient(145deg, rgba(15, 23, 42, 0.82), rgba(30, 41, 59, 0.72));
                box-shadow: 0 24px 60px rgba(15, 23, 42, 0.45);
                backdrop-filter: blur(12px);
            }

            .hero-title {
                font-family: 'Space Grotesk', sans-serif;
                font-size: 3rem;
                font-weight: 700;
                line-height: 1.05;
                margin-bottom: 0.5rem;
                color: #f8fafc;
            }

            .hero-subtitle {
                font-size: 1.05rem;
                color: #cbd5e1;
                max-width: 760px;
            }

            .pill-row {
                display: flex;
                gap: 0.75rem;
                flex-wrap: wrap;
                margin-top: 1.25rem;
            }

            .pill {
                padding: 0.55rem 0.95rem;
                border-radius: 999px;
                background: rgba(59, 130, 246, 0.14);
                border: 1px solid rgba(96, 165, 250, 0.32);
                color: #dbeafe;
                font-size: 0.92rem;
            }

            .section-title {
                font-family: 'Space Grotesk', sans-serif;
                font-size: 1.5rem;
                font-weight: 700;
                color: #f8fafc;
                margin-top: 0.5rem;
                margin-bottom: 0.8rem;
            }

            .poster-card {
                border-radius: 24px;
                overflow: hidden;
                background: rgba(15, 23, 42, 0.82);
                border: 1px solid rgba(148, 163, 184, 0.2);
                box-shadow: 0 16px 40px rgba(2, 6, 23, 0.28);
                transition: transform 0.25s ease, box-shadow 0.25s ease;
                min-height: 100%;
            }

            .poster-card:hover {
                transform: translateY(-6px);
                box-shadow: 0 22px 50px rgba(14, 165, 233, 0.18);
            }

            .poster-card img {
                width: 100%;
                height: 320px;
                object-fit: cover;
                display: block;
            }

            .poster-content {
                padding: 1rem 1rem 1.2rem;
            }

            .movie-title {
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 700;
                color: #f8fafc;
                font-size: 1.08rem;
                margin-bottom: 0.4rem;
            }

            .movie-meta, .movie-overview {
                color: #cbd5e1;
                font-size: 0.92rem;
            }

            .movie-overview {
                margin-top: 0.8rem;
                line-height: 1.5;
            }

            .score-chip {
                display: inline-block;
                margin-top: 0.85rem;
                padding: 0.45rem 0.75rem;
                border-radius: 999px;
                background: rgba(34, 197, 94, 0.14);
                color: #bbf7d0;
                border: 1px solid rgba(74, 222, 128, 0.22);
                font-size: 0.86rem;
            }

            [data-testid="stSidebar"] {
                background: rgba(15, 23, 42, 0.9);
                border-right: 1px solid rgba(148, 163, 184, 0.16);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_movie_card(movie: dict[str, Any], show_similarity: bool = False) -> None:
    similarity_html = ""
    if show_similarity and "similarity" in movie:
        similarity_html = f"<div class='score-chip'>Similarity score: {movie['similarity']}</div>"

    st.markdown(
        f"""
        <div class="poster-card">
            <img src="{movie['poster_url']}" onerror="this.onerror=null;this.src='{movie['backup_poster_url']}';" alt="{movie['title']} poster" />
            <div class="poster-content">
                <div class="movie-title">{movie['title']}</div>
                <div class="movie-meta">{movie['industry']} • {movie['language']} • {movie['year']} • Rating {movie['rating']}</div>
                <div class="movie-meta">Genres: {', '.join(movie['genres'])}</div>
                <div class="movie-meta">Director: {movie['director']}</div>
                <div class="movie-overview">{movie['overview']}</div>
                {similarity_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_styles()

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">CineMatch AI</div>
        <div class="hero-subtitle">
            A movie recommendation system built with FastAPI, Streamlit, and a simple ML pipeline.
            It recommends similar movies across Hollywood, Bollywood, and Tollywood using content-based filtering.
        </div>
        <div class="pill-row">
            <div class="pill">FastAPI backend</div>
            <div class="pill">Streamlit frontend</div>
            <div class="pill">TF-IDF vectorization</div>
            <div class="pill">Cosine similarity</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

movies, api_available = load_movies_with_fallback()

if not api_available:
    st.warning(
        "FastAPI server is not running, so Streamlit is using the local ML recommender directly. "
        "You can still use the app, or start the API with: uvicorn app.api.main:app --reload"
    )

movie_titles = sorted(movie["title"] for movie in movies)
industries = ["All"] + sorted({movie["industry"] for movie in movies})
languages = ["All"] + sorted({movie["language"] for movie in movies})

with st.sidebar:
    st.markdown("### Recommendation Controls")
    selected_title = st.selectbox("Choose a movie", movie_titles)
    selected_industry = st.selectbox("Filter by industry", industries)
    selected_language = st.selectbox("Filter by language", languages)
    top_k = st.slider("Number of recommendations", min_value=3, max_value=8, value=5)
    recommend_clicked = st.button("Recommend Movies", use_container_width=True)


if recommend_clicked:
    try:
        payload, recommendation_from_api = load_recommendations_with_fallback(
            title=selected_title,
            top_k=top_k,
            industry=selected_industry,
            language=selected_language,
        )
    except ValueError as error:
        st.error(str(error))
        st.stop()

    if not recommendation_from_api:
        st.info("Recommendations are currently coming from the local Python recommender because the API is unavailable.")

    st.markdown("<div class='section-title'>Selected Movie</div>", unsafe_allow_html=True)
    render_movie_card(payload["selected_movie"])

    st.markdown("<div class='section-title'>Recommended For You</div>", unsafe_allow_html=True)
    columns = st.columns(3)
    for index, movie in enumerate(payload["recommendations"]):
        with columns[index % 3]:
            render_movie_card(movie, show_similarity=True)
else:
    st.markdown("<div class='section-title'>Movie Library</div>", unsafe_allow_html=True)
    preview_columns = st.columns(3)
    for index, movie in enumerate(movies[:6]):
        with preview_columns[index % 3]:
            render_movie_card(movie)
