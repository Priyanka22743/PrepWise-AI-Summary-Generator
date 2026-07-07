import re

def generate_summary(text):

    # Clean text
    text = text.replace("\n", " ")

    # Split sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    # Agar text chhota hai
    if len(sentences) <= 4:
        return text

    # Smart summary (first + important middle + last)
    summary = []

    summary.append(sentences[0])
    summary.append(sentences[len(sentences)//2])
    summary.append(sentences[-1])

    return " ".join(summary)