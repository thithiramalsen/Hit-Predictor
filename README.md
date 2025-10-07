# 🎵 Machine Learning-Based Hit Song Prediction  

---

## 📖 Project Overview

This project, **Machine Learning-Based Hit Song Prediction**, aims to predict a song's **popularity score (0–100)** on Spotify based on its **audio features** such as danceability, energy, loudness, tempo, and valence.

The system uses **machine learning regression models** to analyze numerical patterns and forecast the potential success of a track before its release.  
It includes a backend built with **FastAPI** and **Flask**, and an OCR-integrated interface to read song features from screenshots (Chosic.com).

---

## 🚀 Key Features

- Predicts a song’s **Spotify popularity score** before release.  
- Supports both **Regression** and **Classification** models.  
- Uses **Tesseract OCR** to extract features directly from screenshots.  
- Interactive backend API built using **FastAPI**.  
- Frontend built with **React.js** for easy interaction.  
- Model trained on the **Spotify Songs Dataset (174,000+ tracks)**.  

---

## 🧠 Machine Learning Models Used

### 🔹 Regression Models:
- Linear Regression  
- Random Forest Regression  
- XGBoost Regression ✅ *(Best performer)*  
- Neural Network Regression ✅ *(Second-best)*  

### 🔹 Classification Models:
- Logistic Regression  
- Random Forest Classification  
- XGBoost Classification  
- Neural Network Classification  

---

## 🧪 Dataset

- Source: [Kaggle – Spotify Tracks Dataset (1921–2020)](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db)
- Size: 174,389 records
- Key columns: `danceability`, `energy`, `valence`, `tempo`, `loudness`, `acousticness`, `instrumentalness`, `speechiness`, `popularity`.

---

## ⚙️ Tech Stack

**Languages:** Python, JavaScript  
**Frontend:** React.js, Tailwind CSS  
**Backend:** FastAPI, Flask  
**Machine Learning:** Scikit-learn, XGBoost, TensorFlow/Keras  
**Data Handling:** Pandas, NumPy  
**Visualization:** Matplotlib, Seaborn  
**OCR:** Tesseract OCR  
**Database:** Local CSV (Spotify dataset)  

---

## 🎥 Project Demo Video
👉 [Watch Full Demonstration](https://drive.google.com/file/d/1aGJWYLTag4wHy5K8-E2J02s6uMjOb-JJ/view?usp=sharing)

> The video includes a full walkthrough of the project: preprocessing, model training, app demonstration, and predictions.

---


---

## 🧰 Installation & Setup

Follow these steps to run the project locally.

### 🔹 Step 1: Clone the Repository

```bash
git clone https://github.com/YourUsername/Hit-Predictor.git
cd Hit-Predictor

```
###  Step 2: Backend Setup

###  Navigate to the backend directory:
```bash
cd backend
```
###  Install all required dependencies:
```bash
pip install -r requirements.txt
```

### Run the backend server:
```bash
$env:PYTHONPATH="D:\VSCode\GitHub\Hit-Predictor\backend\src"; uvicorn src.api:app --reload --port 5000
```

⚠️ For macOS/Linux users:
```bash
export PYTHONPATH="~/Hit-Predictor/backend/src" && uvicorn src.api:app --reload --port 5000
```
### 🔹 Step 3: Frontend Setup

Open a new terminal and navigate to the frontend folder:
```bash
cd frontend
```

Install frontend dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```

Open your browser and go to:
👉 http://localhost:5173



### 🌟 Future Improvements

🔗 Integrate with Spotify API for real-time data fetching

🎧 Add support for raw audio file uploads (Librosa feature extraction)

☁️ Deploy on cloud platforms (AWS / Render) for live predictions

💬 Add lyrics sentiment analysis for advanced feature inputs

🎨 Improve frontend UI/UX for smoother user experience


👨‍💻 Contributors

Team Gold Rush – FDM_02 (SLIIT)

🎤 Malsen N.G.T.

🧠 Waidyarathne D.A.V.P.

💻 Senadheera G.D.B.L.R.

🌸 Sathsarani W.T.T.S.


### This project bridges machine learning and music analytics, enabling prediction of a song’s potential popularity using measurable features.
By leveraging XGBoost Regression and Neural Networks, the system provides valuable insights for artists, producers, and record labels to make data-driven decisions about song releases.

✅ Final Model: XGBoost Regression (best accuracy and generalization)

