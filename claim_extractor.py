import re
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag

nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

def score_sentence(sent):
    score = 0
    if re.search(r"\b\d+\b", sent): score += 1
    if re.search(r"(killed|died|cases|infected|percent|%)", sent, re.I): score += 2
    toks = word_tokenize(sent)
    pos = pos_tag(toks)
    score += sum(1 for _, t in pos if t in ("NNP","NNPS"))
    return score

def extract_top_claims(text, top_n=3):
    sentences = sent_tokenize(text)
    ranked = sorted(sentences, key=score_sentence, reverse=True)
    return ranked[:top_n]
