import pandas as pd

def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """
    Convert DataFrame to markdown table string, handling list elements.
    
    Args:
        df: The DataFrame to convert
    Returns:
        Markdown formatted table as string
    """
    if df is None or df.empty:
        return "No data available"

    headers = df.columns.tolist()
    header_row = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    
    rows = []
    for _, row in df.iterrows():
        values = []
        for val in row.values:
            if isinstance(val, list):
                values.append(" and ".join(str(x) for x in val))
            elif pd.notna(val):
                values.append(str(val))
            else:
                values.append("")
        rows.append("| " + " | ".join(values) + " |")
    
    return "\n".join([header_row, separator] + rows)
