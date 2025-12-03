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
