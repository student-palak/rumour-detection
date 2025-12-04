# src/prepare_dataset.py
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
fake_path = DATA_DIR / "Fake.csv"
true_path = DATA_DIR / "True.csv"
out_path = DATA_DIR / "rumour_raw.csv"

def load_csv(path):
    print("Loading", path)
    df = pd.read_csv(path, low_memory=False)
    print("Columns:", list(df.columns)[:10])
    return df

def pick_text_column(df):
    # prefer 'text', else 'title', else first string-like column
    if "text" in df.columns:
        return df["text"].astype(str)
    if "title" in df.columns:
        return df["title"].astype(str)
    for col in df.columns:
        if df[col].dtype == object:
            return df[col].astype(str)
    raise ValueError("No text-like column found")

def main():
    fake = load_csv(fake_path)
    true = load_csv(true_path)

    fake_text = pick_text_column(fake)
    true_text = pick_text_column(true)

    df_fake = pd.DataFrame({"text": fake_text})
    df_fake["label"] = "rumour"

    df_true = pd.DataFrame({"text": true_text})
    df_true["label"] = "not_rumour"

    df = pd.concat([df_fake, df_true], ignore_index=True)
    df = df.dropna(subset=["text"]).reset_index(drop=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved combined dataset to: {out_path}")
    print("Dataset shape:", df.shape)
    print(df["label"].value_counts())

if __name__ == "__main__":
    main()

