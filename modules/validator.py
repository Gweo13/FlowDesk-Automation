import pandas as pd

REQUIRED_COLUMNS = [
    "order_id",
    "customer_name",
    "email",
    "order_date",
    "amount",
    "status"
]

VALID_STATUSES = [
    "pending",
    "paid",
    "cancelled",
    "completed"
]


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )

    df["email"] = df["email"].str.lower()
    df["status"] = df["status"].str.lower()

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", dayfirst=False)

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["validation_notes"] = ""

    checks = {
        "order_id": df["order_id"].isna(),
        "customer_name": df["customer_name"].isna(),
        "email": ~df["email"].str.contains(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            regex=True,
            na=False
        ),
        "order_date": df["order_date"].isna(),
        "amount": df["amount"].isna() | (df["amount"] <= 0),
        "status": ~df["status"].isin(VALID_STATUSES)
    }

    messages = {
        "order_id": "Order ID kosong",
        "customer_name": "Nama pelanggan kosong",
        "email": "Format email tidak valid",
        "order_date": "Tanggal tidak valid",
        "amount": "Nominal harus lebih dari 0",
        "status": "Status tidak dikenal"
    }

    for column, invalid in checks.items():
        df.loc[invalid, "validation_notes"] += (
            messages[column] + "; "
        )

    duplicate = df["order_id"].duplicated(keep=False)

    df.loc[duplicate, "validation_notes"] += (
        "Order ID duplikat; "
    )

    df["validation_status"] = (
        df["validation_notes"]
        .eq("")
        .map({True: "VALID", False: "REVIEW"})
    )

    return df