# Rumour Detection

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Status](https://img.shields.io/badge/Status-Prototype-green.svg)

A simple end-to-end **Rumour Detection** project using TF-IDF and Logistic Regression.  
Includes preprocessing, training, prediction, and a Streamlit UI.

---

## 🚀 Demo

### Run locally

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python src/preprocess.py data/sample.csv data/cleaned_sample.csv
python src/train_baseline.py data/cleaned_sample.csv models/model.joblib models/vect.joblib

streamlit run app.py
