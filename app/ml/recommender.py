from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "movies.json"


class MovieRecommender:
    def __init__(self, data_path: Path = DATA_PATH) -> None:
        self.data_path = data_path
        self.movies = self._load_movies()
        self.movies["feature_text"] = self.movies.apply(self._build_feature_text, axis=1)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.feature_matrix = self.vectorizer.fit_transform(self.movies["feature_text"])
        self.similarity_matrix = cosine_similarity(self.feature_matrix)

    def _load_movies(self) -> pd.DataFrame:
        with self.data_path.open(encoding="utf-8") as file:
            records = json.load(file)

        movies = pd.DataFrame(records)
        movies["search_title"] = movies["title"].str.lower()
        movies["backup_poster_url"] = movies["title"].apply(
            lambda title: f"https://placehold.co/600x900/0f172a/e2e8f0?text={title.replace(' ', '+')}"
        )
        return movies

    @staticmethod
    def _build_feature_text(row: pd.Series) -> str:
        parts = [
            row["title"],
            row["industry"],
            row["language"],
            row["director"],
            row["overview"],
            " ".join(row["genres"]),
            " ".join(row["mood"]),
            " ".join(row["cast"]),
        ]
        return " ".join(parts).lower()

    def list_movies(self, industry: str | None = None, language: str | None = None) -> list[dict[str, Any]]:
        filtered = self.movies.copy()

        if industry and industry != "All":
            filtered = filtered[filtered["industry"].str.lower() == industry.lower()]

        if language and language != "All":
            filtered = filtered[filtered["language"].str.lower() == language.lower()]

        return filtered.sort_values(["industry", "title"]).to_dict(orient="records")

    def recommend(
        self,
        title: str,
        top_k: int = 5,
        industry: str | None = None,
        language: str | None = None,
    ) -> dict[str, Any]:
        matches = self.movies[self.movies["search_title"] == title.lower()]
        if matches.empty:
            suggestions = self.movies["title"].sort_values().tolist()
            raise ValueError(f"Movie '{title}' was not found. Try one of these: {', '.join(suggestions[:8])}")

        movie_index = matches.index[0]
        similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))
        similarity_scores.sort(key=lambda item: item[1], reverse=True)

        recommendations: list[dict[str, Any]] = []
        for index, score in similarity_scores:
            if index == movie_index:
                continue

            movie = self.movies.iloc[index]
            if industry and industry != "All" and movie["industry"].lower() != industry.lower():
                continue
            if language and language != "All" and movie["language"].lower() != language.lower():
                continue

            result = movie.to_dict()
            result["similarity"] = round(float(score), 3)
            recommendations.append(result)

            if len(recommendations) == top_k:
                break

        return {
            "selected_movie": self.movies.iloc[movie_index].to_dict(),
            "recommendations": recommendations,
            "available_industries": sorted(self.movies["industry"].unique().tolist()),
            "available_languages": sorted(self.movies["language"].unique().tolist()),
        }


recommender = MovieRecommender()
