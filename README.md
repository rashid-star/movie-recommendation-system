# 🎬 Movie Recommendation System

🔗 **Live App:** [https://movie-recommendation-system-by-rashid07.streamlit.app/](https://movie-recommendation-system-by-rashid07.streamlit.app/)

---

## 📌 Project Overview

This project is an **end‑to‑end Movie Recommendation System** built using **Machine Learning, NLP, FastAPI, and Streamlit**.

The goal of this project is to recommend similar movies to users based on the movie they select. The system uses **text‑based similarity (TF‑IDF + Cosine Similarity)** to find related movies.

This project covers the **complete ML lifecycle**:

* Data preprocessing
* Feature engineering (NLP)
* Model building
* Backend API (FastAPI)
* Frontend UI (Streamlit)
* Deployment

---

## 🧠 How Recommendation Works (Core Logic)

### 1️⃣ Data

* Movie metadata (title, overview, genres)
* Stored and processed using **Pandas**

### 2️⃣ NLP Processing

* Movie overviews are cleaned and vectorized
* **TF‑IDF (Term Frequency – Inverse Document Frequency)** is used to convert text into numerical vectors

### 3️⃣ Similarity Calculation

* **Cosine Similarity** is applied on TF‑IDF vectors
* Movies with the highest similarity scores are recommended

### 4️⃣ Model Persistence

* Trained components are saved as:

  * `df.pkl`
  * `tfidf.pkl`
  * `tfidf_matrix.pkl`

---

## ⚙️ Tech Stack Used

### 🧩 Machine Learning & NLP

* Python
* Pandas
* NumPy
* Scikit‑learn
* TF‑IDF Vectorizer
* Cosine Similarity

### 🌐 Backend (API)

* **FastAPI**
* Handles recommendation logic and API endpoints

### 🎨 Frontend (UI)

* **Streamlit**
* User‑friendly interface
* Dropdown to select movie
* Displays recommended movies instantly

### ☁️ Deployment

* **Streamlit Cloud**
* App deployed and accessible publicly

---

## 📂 Project Structure

```text
movie-rec/
│
├── app.py                # Streamlit frontend
├── main.py               # FastAPI backend
├── df.pkl                # Movie dataframe
├── tfidf.pkl             # TF‑IDF vectorizer
├── tfidf_matrix.pkl      # TF‑IDF matrix
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## 🚀 How to Run Locally

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Streamlit App

```bash
streamlit run app.py
```

### 4️⃣ (Optional) Run FastAPI Backend

```bash
uvicorn main:app --reload
```

Open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🎯 Features

* Content‑based movie recommendation
* NLP‑driven similarity matching
* Clean and simple UI
* Real‑time recommendations
* Deployed and production‑ready

---

## 🧪 Challenges Faced & Learnings

* Dependency conflicts (NumPy, Streamlit)
* Environment setup issues
* Deployment debugging
* API & frontend integration

💡 **This project helped me gain real‑world experience in ML engineering and deployment.**

---

## 👨‍💻 Author

**Rashid Chaudhary**
Aspiring Data Scientist / ML Engineer

---

## ⭐ Acknowledgements

* Scikit‑learn documentation
* Streamlit documentation
* TMDB dataset

