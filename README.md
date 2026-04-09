<<<<<<< HEAD
# Specs Freak - NLP-Based Video Game Recommendation Website

This project includes:
- A **Python backend API** that loads your dataset and performs NLP recommendations.
- A **frontend website** with a warm color palette, animated background, and prompt input.
- A working connection between frontend and backend.

## Run Locally

1. Open terminal in `d:\Specs Freak`
2. Create and activate virtual environment (optional):
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Run the app:
   - `python backend\app.py`
5. Open:
   - `http://localhost:5000`

## API

- **POST** `/api/recommend`
- Body:
  ```json
  {
    "prompt": "dark story rich RPG with open world",
    "top_n": 10
  }
  ```
- Returns ranked game recommendations from your dataset.
=======
# Hybrid-NLP-Based-Video-Game-Recommendation-System-with-Sentiment-Analysis
In this project, we propose a Hybrid NLP-Based Video Game Recommendation System that combines content-based filtering with sentiment analysis to generate personalized recommendations. 
>>>>>>> 62bb53556c40882e7fb4999c50ac47c3ea67a1fa
