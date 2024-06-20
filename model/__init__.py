import preprocess


def preprocess_data(text):
    clean_text = str.lower(text)
    clean_text = preprocess.remove_newlines(clean_text)
    clean_text = preprocess.remove_unicodes(clean_text)
    clean_text = preprocess.replace_colloquials(clean_text)
    clean_text = preprocess.remove_stopwords(clean_text)
    clean_text = preprocess.remove_non_alphanums(clean_text)
    clean_text = preprocess.remove_twitter_placeholders(clean_text)
    clean_text = preprocess.remove_extra_spaces(clean_text)

    return clean_text.strip()
