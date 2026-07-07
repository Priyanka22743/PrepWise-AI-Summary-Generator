import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def extract_keypoints(text):

    sentences = sent_tokenize(text)

    keypoints = sentences[:5]

    return keypoints