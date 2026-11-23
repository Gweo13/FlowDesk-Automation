# ⚙️ FlowDesk Automation
### Automated Data Processing & Reporting System

FlowDesk Automation is a Python-based data automation application designed to simplify transaction data processing, validation, and reporting.

The system automatically cleans uploaded datasets, detects invalid and duplicate records, classifies transaction data, and generates interactive dashboards and formatted Excel reports.

## 🚀 Key Features

- **Data Import** — Upload CSV and Excel (.xlsx) files.
- **Data Cleaning** — Normalize column names and clean text values.
- **Data Validation** — Validate required fields, email formats, dates, amounts, and transaction statuses.
- **Duplicate Detection** — Identify duplicated Order IDs.
- **Data Classification** — Separate valid records from records requiring review.
- **Interactive Dashboard** — Display processing KPIs and visual analytics.
- **Excel Reporting** — Generate formatted Excel reports with multiple worksheets and automated charts.

## 📊 Dashboard Preview

The application provides:
- Total Records
- Valid Records
- Records Needing Review
- Valid Transaction Amount
- Data Validation Results
- Transactions by Status
- Data Quality Score

## 📁 Excel Report

The generated Excel workbook contains four worksheets:

| Worksheet | Description |
|---|---|
| Summary | Processing summary and dashboard charts |
| All Data | Complete processed dataset |
| Valid Data | Records that passed validation |
| Needs Review | Records requiring further attention |

## 🛠️ Technology Stack

- Python 3.12
- Streamlit
- Pandas
- OpenPyXL
- Plotly
- Git & GitHub

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FlowDesk-Automation
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

## 🧪 Sample Dataset

A sample transaction dataset (`sample_data.csv`) is included to demonstrate the automated processing pipeline.

The sample contains valid records, duplicate Order IDs, invalid email formats, and invalid transaction amounts.

## 🎯 Project Objective

This project demonstrates practical skills in Python automation, data processing, data quality validation, dashboard development, and automated reporting.

**Project Type:** Personal Portfolio Project  
**Version:** 1.0 MVP  
**Developer:** Aryansyah Dewanata