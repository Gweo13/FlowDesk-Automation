import pandas as pd

from modules.processor import clean_data
from modules.validator import validate_data
from modules.exporter import export_report


# Load sample data
df = pd.read_csv("sample_data.csv")

# Run automation pipeline
cleaned = clean_data(df)
result = validate_data(cleaned)

# Separate records
valid = result[result["validation_status"] == "VALID"]
review = result[result["validation_status"] == "REVIEW"]

# Display results
print("\n===== FLOWDESK AUTOMATION TEST =====")

print(f"Total Records : {len(result)}")
print(f"Valid Records : {len(valid)}")
print(f"Needs Review  : {len(review)}")

print("\n===== VALIDATION DETAILS =====")

print(
    result[
        ["order_id", "validation_status", "validation_notes"]
    ].to_string(index=False)
)

# Export Excel
excel = export_report(result)

with open("test_report.xlsx", "wb") as file:
    file.write(excel)

print("\nExcel report generated successfully!")