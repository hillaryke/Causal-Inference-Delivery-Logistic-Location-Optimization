# Display df in markdown
def display_df(df, n_rows=5, head_or_tail="head"):
    """Displays DataFrame in markdown format."""
    
    if head_or_tail == "head":
        print(df.head(n_rows).to_markdown(index=False, numalign="left", stralign="left"))
    elif head_or_tail == "tail":
        print(df.tail(n_rows).to_markdown(index=False, numalign="left", stralign="left"))