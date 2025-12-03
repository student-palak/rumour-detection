# src/train_baseline.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import sys

def main(clean_csv, model_path, vect_path):
    df = pd.read_csv(clean_csv)
    X = df['text_clean'].astype(str)
    y = df['label'].astype(str)

    strat = y if len(set(y)) > 1 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=strat)

    vect = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
    Xtr = vect.fit_transform(X_train)
    Xte = vect.transform(X_test)

    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(Xtr, y_train)

    preds = model.predict(Xte)

    print(classification_report(y_test, preds))

    joblib.dump(vect, vect_path)
    joblib.dump(model, model_path)

    print("Saved model to", model_path)
    print("Saved vectorizer to", vect_path)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python train_baseline.py data/cleaned.csv models/model.joblib models/vect.joblib")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
