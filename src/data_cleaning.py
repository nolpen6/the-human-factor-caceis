import pandas as pd
import re


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names:
    - lowercase
    - remove leading/trailing spaces
    - replace special characters with underscores
    """
    df = df.copy()
    df.columns = [
        re.sub(r"[^a-zA-Z0-9]+", "_", str(col).strip().lower()).strip("_")
        for col in df.columns
    ]
    return df


def remove_empty_rows_and_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows and columns that are fully empty.
    """
    df = df.copy()
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove exact duplicate rows.
    """
    return df.drop_duplicates().copy()


def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert columns containing 'date' into datetime format.
    """
    df = df.copy()

    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def standardize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip spaces from text columns.
    """
    df = df.copy()

    text_cols = df.select_dtypes(include="object").columns

    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": None, "None": None, "": None})

    return df


def standardize_employee_id(
    df: pd.DataFrame,
    possible_id_columns=None
) -> pd.DataFrame:
    """
    Standardize employee ID column if detected.

    Creates a common column called 'employee_id' when possible.
    """

    df = df.copy()

    if possible_id_columns is None:
        possible_id_columns = [
            "employee_id",
            "id_collaborateur",
            "id_salarie",
            "matricule",
            "matricule_salarie",
            "numero_collaborateur",
            "num_collaborateur",
            "id",
        ]

    existing_cols = df.columns.tolist()

    for col in possible_id_columns:
        if col in existing_cols:
            df["employee_id"] = df[col].astype(str).str.strip()
            return df

    return df


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply standard cleaning steps to one raw dataset.
    """

    df = df.copy()

    df = remove_empty_rows_and_columns(df)
    df = clean_column_names(df)
    df = remove_duplicates(df)
    df = standardize_text_columns(df)
    df = standardize_employee_id(df)
    df = convert_date_columns(df)

    return df


def inspect_dataset(df: pd.DataFrame, name: str = "Dataset") -> None:
    """
    Print a quick overview of a dataframe.
    """

    print(f"\n===== {name} =====")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).head(15))
    print("\nPreview:")
    display(df.head())
