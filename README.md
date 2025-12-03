

# Rumour Detection

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Status](https://img.shields.io/badge/Status-Prototype-green.svg)

A simple end-to-end **Rumour Detection** pipeline (TF-IDF + Logistic Regression baseline) with:
- data preparation and preprocessing,
- training and evaluation,
- a Streamlit web demo.

---

## 🚀 Demo — Run locally

```bash
# create & activate venv (Windows)
python -m venv venv
venv\Scripts\activate

# install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# prepare dataset (combine Fake.csv + True.csv -> rumour_raw.csv)
python src/prepare_dataset.py

# preprocess and create cleaned CSV
python src/preprocess.py data/rumour_raw.csv data/cleaned_rumour.csv

# train baseline model (saves models/*)
python src/train_baseline.py data/cleaned_rumour.csv models/model.joblib models/vect.joblib

# run app
streamlit run app.py

streamlit run app.py
```

## 📸 Screenshots

### Streamlit App
![Streamlit App](docs/images/streamlit_app.png)

### Prediction Example
![Prediction Example](docs/images/prediction_example.png)


