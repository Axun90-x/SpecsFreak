# 🎮 Hybrid NLP-Based Video Game Recommendation System

This project is an advanced **Video Game Recommendation System** that combines:
- 🧠 **Natural Language Processing (NLP)**
- ⭐ **Sentiment Analysis**
- 🔍 **Content-Based Filtering**

It allows users to input natural language prompts (e.g., *"dark story-rich RPG with open world"*) and receive **personalized game recommendations** based on game descriptions and user sentiment.

---

## 🚀 Features

- 🎯 NLP-based recommendation engine
- 😊 Sentiment analysis for better personalization
- 🔗 Hybrid filtering approach (content + sentiment)
- 🌐 Interactive frontend with modern UI
- ⚡ Fast API response using Python backend
- 🎨 Animated UI with warm color palette

---

## 🛠️ Tech Stack

**Frontend:**
- HTML, CSS, JavaScript
- Animated UI / Responsive Design

**Backend:**
- Python (Flask / FastAPI)
- NLP Libraries (NLTK / Scikit-learn)

**Other Tools:**
- Pandas, NumPy
- Dataset-based recommendation system

---

## 📂 Project Structure
Hybrid-Game-Recommender/
│
├── colab_notebooks/             # 📊 Main development done here
│   ├── Game_Recommender.ipynb   # NLP + recommendation system
│   ├── Sentiment_Analysis.ipynb # Sentiment model
│   └── EDA.ipynb                # Data analysis
│
├── backend/                     # 🔧 Converted API from Colab
│   ├── app.py                   # Flask/FastAPI server
│   ├── recommender.py           # Logic extracted from notebook
│   ├── sentiment.py             # Sentiment logic
│   └── model/                   # Saved models from Colab
│       ├── tfidf.pkl
│       └── similarity.pkl
│
├── dataset/                     # 📁 Dataset used in Colab
│   └── games.csv
│
├── frontend/                    # 🌐 Website UI
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── outputs/                     # 📈 Results / screenshots
│   └── sample_results.png
│
├── requirements.txt
├── README.md
└── .gitignore
