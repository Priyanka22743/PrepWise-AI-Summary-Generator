from transformers import pipeline

simplifier = pipeline("text2text-generation", model="google/flan-t5-base")

def simplify_text(text):

    prompt = "Explain this in simple language: " + text

    result = simplifier(prompt, max_length=120)

    return result[0]["generated_text"]