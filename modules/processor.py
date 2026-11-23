import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names and clean text values.
    """

    df = df.copy()

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Clean text values
    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df