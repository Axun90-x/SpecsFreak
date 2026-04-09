from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = BASE_DIR / "Dataset"
PRIMARY_DATASET_PATH = DATASET_DIR / "games_of_all_time_cleaned_normalized.csv"
STEAM_TAGS_PATH = DATASET_DIR / "steam_games.csv"
FRONTEND_DIR = BASE_DIR / "frontend"


def clean_text(value: Any) -> str:
    text = str(value if value is not None else "")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_list_string(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            return " ".join(clean_text(item) for item in parsed if item)
    except (ValueError, SyntaxError):
        pass
    return clean_text(text.replace("[", " ").replace("]", " ").replace(",", " "))


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def load_and_prepare() -> tuple[pd.DataFrame, TfidfVectorizer, Any]:
    df = pd.read_csv(PRIMARY_DATASET_PATH)

    df["meta_score"] = pd.to_numeric(df["meta_score"], errors="coerce")
    df["user_score"] = pd.to_numeric(df["user_score"], errors="coerce")

    df["clean_name"] = df["game_name"].apply(clean_text)
    df["clean_genre"] = df["genre"].apply(clean_list_string)
    df["clean_platform"] = df["platform"].apply(clean_list_string)
    df["clean_type"] = df["type"].apply(clean_text)
    df["clean_desc"] = df["description"].apply(clean_text)

    # Optional tag enrichment from provided Steam dataset.
    if STEAM_TAGS_PATH.exists():
        steam_df = pd.read_csv(STEAM_TAGS_PATH, usecols=["title", "popular_tags"])
        steam_df["norm_name"] = steam_df["title"].apply(normalize_name)
        tag_lookup = steam_df.dropna(subset=["popular_tags"]).drop_duplicates(
            subset=["norm_name"]
        ).set_index("norm_name")["popular_tags"]

        df["norm_name"] = df["game_name"].apply(normalize_name)
        df["tags"] = df["norm_name"].map(tag_lookup).fillna("")
    else:
        df["tags"] = ""

    df["clean_tags"] = df["tags"].apply(clean_list_string)

    # Weighted text field inspired by your notebook logic.
    df["combined_features"] = (
        df["clean_name"]
        + " "
        + df["clean_name"]
        + " "
        + df["clean_desc"]
        + " "
        + df["clean_genre"]
        + " "
        + df["clean_genre"]
        + " "
        + df["clean_tags"]
        + " "
        + df["clean_platform"]
        + " "
        + df["clean_type"]
        + " "
        + df["clean_type"]
    )

    tfidf = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=45000,
        min_df=2,
    )
    tfidf_matrix = tfidf.fit_transform(df["combined_features"])
    return df, tfidf, tfidf_matrix


def score_recommendations(
    df: pd.DataFrame,
    tfidf: TfidfVectorizer,
    tfidf_matrix: Any,
    user_prompt: str,
    top_n: int = 30,
    alpha: float = 0.75,
    beta: float = 0.25,
) -> pd.DataFrame:
    prompt_clean = clean_text(user_prompt)
    if len(prompt_clean.split()) < 2:
        return pd.DataFrame()

    user_vector = tfidf.transform([prompt_clean])
    sim_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    sentiment = (
        0.6 * df["meta_score_norm_0_1"].fillna(0).values
        + 0.4 * df["user_score_norm_0_1"].fillna(0).values
    )
    final_scores = (alpha * sim_scores) + (beta * sentiment)

    top_indices = final_scores.argsort()[::-1][:top_n]
    output = df.iloc[top_indices][
        ["game_name", "genre", "platform", "type", "meta_score", "user_score", "rating", "url"]
    ].copy()
    output["similarity"] = sim_scores[top_indices]
    output["final_score"] = final_scores[top_indices]
    output = output.reset_index(drop=True)
    return output


df_store, tfidf_store, tfidf_matrix_store = load_and_prepare()

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
CORS(app)


@app.get("/")
def index():
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.post("/api/recommend")
def recommend():
    body = request.get_json(silent=True) or {}
    prompt = (body.get("prompt") or "").strip()
    top_n = int(body.get("top_n", 30))
    top_n = max(1, min(top_n, 30))

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    results = score_recommendations(
        df_store, tfidf_store, tfidf_matrix_store, prompt, top_n=top_n
    )
    if results.empty:
        return jsonify(
            {
                "prompt": prompt,
                "count": 0,
                "recommendations": [],
                "message": "Please enter at least two descriptive words.",
            }
        )

    return jsonify(
        {
            "prompt": prompt,
            "count": len(results),
            "recommendations": [
                {
                    "rank": idx + 1,
                    "game_name": row["game_name"],
                    "genre": row["genre"],
                    "platform": row["platform"],
                    "type": row["type"],
                    "game_review": None if pd.isna(row["user_score"]) else float(row["user_score"]),
                    "meta_score": None if pd.isna(row["meta_score"]) else float(row["meta_score"]),
                    "user_score": None if pd.isna(row["user_score"]) else float(row["user_score"]),
                    "rating": row["rating"],
                    "url": row["url"],
                    "similarity": round(float(row["similarity"]), 4),
                    "final_score": round(float(row["final_score"]), 4),
                }
                for idx, row in results.iterrows()
            ],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
