import pandas as pd
from io import BytesIO

from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.chart import DoughnutChart, BarChart, Reference
from openpyxl.chart.label import DataLabelList


def export_report(df: pd.DataFrame) -> bytes:
    valid = df[df["validation_status"] == "VALID"]
    review = df[df["validation_status"] == "REVIEW"]

    summary = pd.DataFrame({
        "Metric": [
            "Total Records",
            "Valid Records",
            "Records Needing Review",
            "Total Valid Amount",
            "Validation Success Rate"
        ],
        "Value": [
            len(df),
            len(valid),
            len(review),
            valid["amount"].sum(),
            len(valid) / len(df) if len(df) > 0 else 0
        ]
    })

    validation_counts = (
        df["validation_status"]
        .value_counts()
        .reindex(["VALID", "REVIEW"], fill_value=0)
    )

    status_counts = df["status"].value_counts().sort_index()

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        df.to_excel(writer, sheet_name="All Data", index=False)
        valid.to_excel(writer, sheet_name="Valid Data", index=False)
        review.to_excel(writer, sheet_name="Needs Review", index=False)

        workbook = writer.book
        ws_summary = writer.sheets["Summary"]

        # Styling
        header_fill = PatternFill(fill_type="solid", fgColor="1E3A5F")
        header_font = Font(bold=True, color="FFFFFF", size=11)

        valid_fill = PatternFill(fill_type="solid", fgColor="DCFCE7")
        review_fill = PatternFill(fill_type="solid", fgColor="FFEDD5")

        thin_border = Border(
            bottom=Side(style="thin", color="E2E8F0")
        )

        for ws in workbook.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions

            for cell in ws[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center"
                )

            ws.row_dimensions[1].height = 25

            for column_cells in ws.columns:
                max_length = 0
                column_letter = get_column_letter(
                    column_cells[0].column
                )

                for cell in column_cells:
                    if cell.value is not None:
                        max_length = max(
                            max_length,
                            len(str(cell.value))
                        )

                ws.column_dimensions[column_letter].width = min(
                    max(max_length + 4, 14),
                    40
                )

            for row in ws.iter_rows(min_row=2):
                for cell in row:
                    cell.border = thin_border
                    cell.alignment = Alignment(vertical="center")

            headers = {
                cell.value: cell.column
                for cell in ws[1]
            }

            if "amount" in headers:
                amount_col = headers["amount"]

                for row in range(2, ws.max_row + 1):
                    ws.cell(
                        row=row,
                        column=amount_col
                    ).number_format = '"Rp" #,##0'

            if "order_date" in headers:
                date_col = headers["order_date"]

                for row in range(2, ws.max_row + 1):
                    ws.cell(
                        row=row,
                        column=date_col
                    ).number_format = "DD MMM YYYY"

            if "validation_status" in headers:
                status_col = headers["validation_status"]

                for row in range(2, ws.max_row + 1):
                    status = ws.cell(
                        row=row,
                        column=status_col
                    ).value

                    if status == "VALID":
                        for col in range(1, ws.max_column + 1):
                            ws.cell(
                                row=row,
                                column=col
                            ).fill = valid_fill

                    elif status == "REVIEW":
                        for col in range(1, ws.max_column + 1):
                            ws.cell(
                                row=row,
                                column=col
                            ).fill = review_fill

        # Summary formatting
        for row in range(2, ws_summary.max_row + 1):
            metric = ws_summary.cell(row=row, column=1).value
            value_cell = ws_summary.cell(row=row, column=2)

            if metric == "Total Valid Amount":
                value_cell.number_format = '"Rp" #,##0'

            elif metric == "Validation Success Rate":
                value_cell.number_format = "0.0%"

        # Supporting data for charts
        ws_summary["D2"] = "Validation Status"
        ws_summary["E2"] = "Count"

        for cell in ws_summary[2][3:5]:
            cell.fill = header_fill
            cell.font = header_font

        ws_summary["D3"] = "VALID"
        ws_summary["E3"] = int(validation_counts["VALID"])

        ws_summary["D4"] = "REVIEW"
        ws_summary["E4"] = int(validation_counts["REVIEW"])

        ws_summary["G2"] = "Transaction Status"
        ws_summary["H2"] = "Count"

        for cell in ws_summary[2][6:8]:
            cell.fill = header_fill
            cell.font = header_font

        for row_num, (status, count) in enumerate(
            status_counts.items(), start=3
        ):
            ws_summary.cell(row=row_num, column=7, value=status)
            ws_summary.cell(row=row_num, column=8, value=int(count))

        # Doughnut Chart
        donut = DoughnutChart()

        donut_data = Reference(
            ws_summary,
            min_col=5,
            min_row=2,
            max_row=4
        )

        donut_categories = Reference(
            ws_summary,
            min_col=4,
            min_row=3,
            max_row=4
        )

        donut.add_data(donut_data, titles_from_data=True)
        donut.set_categories(donut_categories)

        donut.title = "Data Validation Results"
        donut.style = 10
        donut.holeSize = 65
        donut.height = 8
        donut.width = 13

        donut.dataLabels = DataLabelList()
        donut.dataLabels.showPercent = True
        donut.dataLabels.showVal = True

        ws_summary.add_chart(donut, "D9")

        # Bar Chart
        bar = BarChart()

        bar_data = Reference(
            ws_summary,
            min_col=8,
            min_row=2,
            max_row=2 + len(status_counts)
        )

        bar_categories = Reference(
            ws_summary,
            min_col=7,
            min_row=3,
            max_row=2 + len(status_counts)
        )

        bar.add_data(bar_data, titles_from_data=True)
        bar.set_categories(bar_categories)

        bar.title = "Transactions by Status"
        bar.y_axis.title = "Number of Records"
        bar.x_axis.title = "Transaction Status"
        bar.style = 10
        bar.height = 8
        bar.width = 13
        bar.legend = None

        bar.dataLabels = DataLabelList()
        bar.dataLabels.showVal = True

        ws_summary.add_chart(bar, "L9")

        ws_summary.column_dimensions["D"].width = 22
        ws_summary.column_dimensions["E"].width = 14
        ws_summary.column_dimensions["G"].width = 22
        ws_summary.column_dimensions["H"].width = 14

    return output.getvalue()