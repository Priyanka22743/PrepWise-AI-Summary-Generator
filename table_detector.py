import camelot

def detect_tables(pdf_path):

    tables = camelot.read_pdf(pdf_path, pages='all')

    table_summaries = []

    for i, table in enumerate(tables):

        df = table.df

        rows, cols = df.shape

        summary = f"Table {i+1} detected with {rows} rows and {cols} columns."

        table_summaries.append(summary)

    return table_summaries