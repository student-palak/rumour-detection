import os
import joblib
from extract_text import extract_text_from_url
from claim_extractor import extract_top_claims
from services.factcheck import search_claims

MODEL_PATH = "models/model.joblib"
VECT_PATH = "models/vect.joblib"

model = joblib.load(MODEL_PATH)
vect = joblib.load(VECT_PATH)

def compute_evidence_score(resp):
    claims = resp.get("claims", [])
    score = 0
    for c in claims:
        if c.get("claimReview"):
            score += 1
    return min(score / 5, 1.0)

def analyze_text(text, url=None):
    top_claims = extract_top_claims(text)
    fact_matches = []

    for c in top_claims:
        try:
            fc = search_claims(c)
            evidence = compute_evidence_score(fc)
        except Exception as e:
            fc = {"error": str(e)}
            evidence = 0
        fact_matches.append({
            "claim": c,
            "factchecks": fc.get("claims", []),
            "evidence_score": evidence
        })

    X = vect.transform([text])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X).max()

    if max([f["evidence_score"] for f in fact_matches]) >= 0.75:
        verdict = "likely-misinformation"
    else:
        verdict = "fake" if pred == 0 else "real"

    return {
        "verdict": verdict,
        "model_pred": str(pred),
        "confidence": float(prob),
        "factcheck_matches": fact_matches
    }

def analyze_url(url):
    doc = extract_text_from_url(url)
    return analyze_text(doc["text"], url=url)
