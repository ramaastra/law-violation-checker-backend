import pandas as pd
import nltk
import re
from nltk.corpus import stopwords

nltk.download("stopwords")

stop_words = set(stopwords.words("indonesian"))
colloquial_dict = pd.read_csv("./preprocess/colloquial_dict.csv")


def replace_colloquials(text):
    return " ".join(
        [
            colloquial_dict.get(word) if colloquial_dict.get(word) else word
            for word in text.split()
        ]
    )


def remove_stopwords(text):
    return " ".join([word for word in text.split() if word not in stop_words])


def remove_newlines(text):
    return re.sub(r"\\n", " ", text)


def remove_unicodes(text):
    return re.sub(r"\\[\w]+\'?", " ", text)


def remove_non_alphanums(text):
    return re.sub(r"[^a-zA-Z]+", " ", text)


def remove_twitter_placeholders(text):
    return re.sub(r"user|username|url|rt", " ", text)


def remove_extra_spaces(text):
    return re.sub(r"  +", " ", text)
