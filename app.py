import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from modules.processor import clean_data
from modules.validator import validate_data
from modules.exporter import export_report


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="FlowDesk Automation",
    page_icon="⚙️",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main Layout */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0;
}

.subtitle {
    color: #94a3b8;
    font-size: 1rem;
}

/* KPI Cards */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
}

/* KPI Text */
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] label p,
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #1f2937 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.2);
}

/* Upload Area */
div[data-testid="stFileUploader"] {
    border-radius: 12px;
}

/* Buttons */
.stButton button,
.stDownloadButton button {
    border-radius: 8px;
    font-weight: 600;
}

/* Section Spacing */
h2, h3 {
    font-weight: 650;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">⚙️ FlowDesk Automation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Automated Data Processing & Reporting System</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("⚙️ FlowDesk")

    st.caption("DATA AUTOMATION PLATFORM")

    st.markdown("---")

    st.subheader("Supported Files")

    st.markdown("""
    - CSV
    - Excel (.xlsx)
    """)

    st.markdown("---")

    st.subheader("Processing Features")

    st.markdown("""
    - Data Cleaning
    - Data Validation
    - Duplicate Detection
    - Data Classification
    - Automated Excel Reporting
    """)

    st.markdown("---")

    st.caption("Version 1.0 | MVP")


# ==========================================
# FILE UPLOAD
# ==========================================

st.subheader("📂 Data Import")

st.write(
    "Upload your transaction dataset to start automated processing."
)

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)
# One-Click Demo
st.caption(
    "Don't have a dataset? Try the application using our sample data."
)

if st.button(
    "🚀 Try Demo with Sample Data",
    use_container_width=True
):
    try:
        sample_path = Path(__file__).parent / "sample_data.csv"
        raw_data = pd.read_csv(sample_path)

        st.session_state["demo_data"] = raw_data
        st.session_state["demo_source"] = "Built-in Sample Data"

    except Exception as e:
        st.error(f"Demo failed: {str(e)}")


# Demo Data Preview
if "demo_data" in st.session_state:
    st.success("Sample dataset loaded successfully!")

    with st.expander("👀 Preview Raw Sample Data", expanded=True):
        st.dataframe(
            st.session_state["demo_data"],
            use_container_width=True,
            hide_index=True
        )

    if st.button(
        "🚀 Run Automation on Sample Data",
        type="primary",
        use_container_width=True
    ):
        with st.spinner("Cleaning and validating sample data..."):
            cleaned_data = clean_data(st.session_state["demo_data"])
            result = validate_data(cleaned_data)

            st.session_state["result"] = result
            st.session_state["source_file"] = "Built-in Sample Data"

        st.success("Automation completed successfully!")


# ==========================================
# PROCESSING
# ==========================================

if uploaded_file:

    try:

        if uploaded_file.name.endswith(".csv"):
            raw_data = pd.read_csv(uploaded_file)

        else:
            raw_data = pd.read_excel(uploaded_file)

        st.success(
            f"Successfully uploaded: {uploaded_file.name}"
        )

        with st.expander("Preview Source Data"):

            st.dataframe(
                raw_data.head(10),
                use_container_width=True
            )

        if st.button(
            "🚀 Run Automation",
            type="primary",
            use_container_width=True
        ):

            with st.spinner("Cleaning and validating data..."):

                cleaned_data = clean_data(raw_data)

                result = validate_data(cleaned_data)

                st.session_state["result"] = result
                st.session_state["source_file"] = uploaded_file.name

            st.success("Automation completed successfully!")


    except Exception as e:

        st.error(f"Processing failed: {str(e)}")


# ==========================================
# RESULTS
# ==========================================

if "result" in st.session_state:

    result = st.session_state["result"]

    valid_data = result[
        result["validation_status"] == "VALID"
    ]

    review_data = result[
        result["validation_status"] == "REVIEW"
    ]

    st.markdown("---")

    st.subheader("📊 Processing Overview")

    if "source_file" in st.session_state:
        st.caption(f"Source file: {st.session_state['source_file']}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{len(result):,}"
    )

    col2.metric(
        "Valid Records",
        f"{len(valid_data):,}"
    )

    col3.metric(
        "Needs Review",
        f"{len(review_data):,}"
    )

    col4.metric(
        "Valid Transaction Amount",
        f"Rp {valid_data['amount'].sum():,.0f}".replace(",", ".")
    )
        # ======================================
    # VISUAL ANALYTICS
    # ======================================

    st.markdown("---")
    st.subheader("📈 Visual Analytics")

    chart1, chart2 = st.columns(2)

    # Donut Chart: Validation Results
    with chart1:

        validation_counts = (
            result["validation_status"]
            .value_counts()
            .reindex(["VALID", "REVIEW"], fill_value=0)
            .reset_index()
        )

        validation_counts.columns = ["Status", "Count"]

        fig_donut = px.pie(
            validation_counts,
            names="Status",
            values="Count",
            hole=0.65,
            color="Status",
            color_discrete_map={
                "VALID": "#22c55e",
                "REVIEW": "#f97316"
            },
            title="Data Validation Results"
        )

        fig_donut.update_traces(
            textinfo="percent+value",
            textfont_size=14
        )

        fig_donut.update_layout(
            template="plotly_dark",
            legend_title="Validation Status",
            margin=dict(t=60, b=20, l=20, r=20)
        )

        st.plotly_chart(
            fig_donut,
            use_container_width=True
        )

    # Bar Chart: Transaction Status
    with chart2:

        status_counts = (
            result["status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = ["Status", "Count"]

        fig_bar = px.bar(
            status_counts,
            x="Status",
            y="Count",
            color="Status",
            text="Count",
            title="Transactions by Status",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig_bar.update_traces(
            textposition="outside"
        )

        fig_bar.update_layout(
            template="plotly_dark",
            showlegend=False,
            xaxis_title="Transaction Status",
            yaxis_title="Number of Records",
            margin=dict(t=60, b=20, l=20, r=20)
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    # Data Quality Score
    total_records = len(result)

    valid_percentage = (
        len(valid_data) / total_records * 100
        if total_records > 0 else 0
    )

    st.subheader("🎯 Data Quality Score")

    st.metric(
        "Validation Success Rate",
        f"{valid_percentage:.1f}%"
    )

    st.progress(valid_percentage / 100)

        # ======================================
    # TABLE CONFIGURATION
    # ======================================

    table_config = {
        "order_id": st.column_config.TextColumn(
            "Order ID"
        ),
        "customer_name": st.column_config.TextColumn(
            "Customer Name"
        ),
        "email": st.column_config.TextColumn(
            "Email"
        ),
        "order_date": st.column_config.DateColumn(
            "Order Date",
            format="DD MMM YYYY"
        ),
        "amount": st.column_config.NumberColumn(
            "Amount",
            format="Rp %.0f"
        ),
        "status": st.column_config.TextColumn(
            "Transaction Status"
        ),
        "validation_notes": st.column_config.TextColumn(
            "Validation Notes",
            width="large"
        ),
        "validation_status": st.column_config.TextColumn(
            "Validation Status"
        )
    }

    # ======================================
    # PROCESSED DATA
    # ======================================

    st.markdown("---")

    st.subheader("📋 Processed Data")

    tab1, tab2, tab3 = st.tabs([
        "All Records",
        "🟢 Valid Records",
        "🟠 Needs Review"
    ])

    with tab1:

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True,
            column_config=table_config,
        )
    
    with tab2:

        if valid_data.empty:

            st.info("No valid records found.")

        else:

            st.dataframe(
                valid_data,
                use_container_width=True,
                hide_index=True,
                column_config=table_config,
            )

    with tab3:

        if review_data.empty:

            st.success("No records need review.")

        else:

            st.warning(
                f"{len(review_data)} records require attention."
            )

            st.dataframe(
                review_data,
                use_container_width=True,
                hide_index=True,
                column_config=table_config,
            )

    # ======================================
    # EXPORT REPORT
    # ======================================

    st.markdown("---")

    st.subheader("📥 Export Report")

    st.write(
        "Download the processed results as an Excel workbook."
    )

    excel_file = export_report(result)

    st.download_button(
        label="⬇️ Download Excel Report",
        data=excel_file,
        file_name="FlowDesk_Automation_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "FlowDesk Automation | Built with Python, Pandas & Streamlit"
)