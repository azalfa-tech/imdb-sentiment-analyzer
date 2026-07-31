import re

CONTRACTIONS = {
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "can't": "can not",
    "cannot": "can not",
    "couldn't": "could not",
    "won't": "will not",
    "wouldn't": "would not",
    "shouldn't": "should not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "mustn't": "must not",
    "needn't": "need not",
    "i'm": "i am",
    "it's": "it is",
    "that's": "that is",
    "there's": "there is"
}

def clean_text(text):

    text = text.lower()

    for contraction, expanded in CONTRACTIONS.items():
        text = text.replace(contraction, expanded)

    text = re.sub(r"<.*?>", " ", text)

    text = re.sub(r"http\S+|www\S+", "", text)

    text = re.sub(r"[^a-zA-Z\s]", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text