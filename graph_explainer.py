import re

def explain_graphs(text):

    numbers = re.findall(r'\d+', text)

    if len(numbers) > 5:

        return "The document contains numerical data which may represent charts or graphs showing trends or comparisons."

    return "No clear graph or chart detected in this page."