import pandas as pd

def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """
    Convert any DataFrame to a markdown table string.
    
    Args:
        df: The DataFrame to convert
    Returns:
        Markdown formatted table as string
    """
    headers = df.columns.tolist()
    header_row = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    
    rows = []
    for _, row in df.iterrows():
        # Convert any non-string values to strings and handle None/NaN
        values = [str(val) if pd.notna(val) else "" for val in row.values]
        rows.append("| " + " | ".join(values) + " |")
    
    return "\n".join([header_row, separator] + rows)
