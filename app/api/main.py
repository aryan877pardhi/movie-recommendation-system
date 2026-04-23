from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.ml.recommender import recommender


app = FastAPI(
    title="Movie Recommendation API",
    description="Content-based movie recommender for Hollywood, Bollywood, and Tollywood films.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Movie recommendation API is running."}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/movies")
def get_movies(
    industry: str | None = Query(default=None),
    language: str | None = Query(default=None),
) -> dict[str, object]:
    movies = recommender.list_movies(industry=industry, language=language)
    return {"count": len(movies), "movies": movies}


@app.get("/recommend")
def get_recommendations(
    title: str = Query(..., description="Movie title"),
    top_k: int = Query(default=5, ge=1, le=10),
    industry: str | None = Query(default=None),
    language: str | None = Query(default=None),
) -> dict[str, object]:
    try:
        return recommender.recommend(title=title, top_k=top_k, industry=industry, language=language)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
