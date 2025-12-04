# src/predict.py
import joblib
import sys
from src.preprocess import clean_text

def predict(text, model_path="models/model.joblib", vect_path="models/vect.joblib"):
    # Load vectorizer and model
    vect = joblib.load(vect_path)
    model = joblib.load(model_path)

    # Clean input text
    clean = clean_text(text)

    # Transform and predict
    x = vect.transform([clean])
    pred = model.predict(x)[0]

    # Confidence score (if available)
    if hasattr(model, "predict_proba"):
        conf = model.predict_proba(x)[0].max()
    else:
        conf = None

    return pred, conf

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py \"Your text here\"")
    else:
        text = " ".join(sys.argv[1:])
        prediction, confidence = predict(text)
        print("Prediction:", prediction)
        print("Confidence:", confidence)
