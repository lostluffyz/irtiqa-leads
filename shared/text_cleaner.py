import re


JUNK_PHRASES = [

    "podcast",
    "youtube",
    "latest blog posts",
    "featured video",
    "featured episode",
    "listen now",
    "watch video",
    "book reviews",
    "open job opportunities",
    "careers",
    "press media",
    "skip content",
    "cookie",
    "privacy policy",
    "terms conditions",
    "sign up",
    "subscribe",
    "bonus episodes"
]


def clean_text(text):

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Remove weird symbols
    text = re.sub(r"[^a-zA-Z0-9\s.,&-]", " ", text)

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove junk phrases
    for phrase in JUNK_PHRASES:

        text = text.replace(phrase, " ")

    # Remove repeated spaces again
    text = re.sub(r"\s+", " ", text)

    # Split words
    words = text.split()

    filtered_words = []

    for word in words:

        # Remove tiny junk words
        if len(word) > 2:
            filtered_words.append(word)

    cleaned_text = " ".join(filtered_words)

    return cleaned_text.strip()