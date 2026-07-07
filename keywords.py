from collections import Counter
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def extract_keywords(text):

    words = text.lower().split()

    stop_words = set(stopwords.words("english"))

    filtered = [w for w in words if w.isalnum() and w not in stop_words]

    freq = Counter(filtered)

    keywords = [word for word, _ in freq.most_common(8)]

    return keywords