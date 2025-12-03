# src/preprocess.py
import pandas as pd
import re
import sys

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+', ' ', text)     # remove urls
    text = re.sub(r'@\w+', ' ', text)        # remove mentions
    text = re.sub(r'#', ' ', text)           # remove hashtags symbol only
    text = re.sub(r'[^a-z0-9\s]', ' ', text) # remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['text_clean'] = df['text'].apply(clean_text)
    df.to_csv(output_csv, index=False)
    print("Saved cleaned data to", output_csv)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python preprocess.py data/input.csv data/output.csv")
    else:
        main(sys.argv[1], sys.argv[2])
