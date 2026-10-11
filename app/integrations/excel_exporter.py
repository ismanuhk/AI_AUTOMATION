import os
import pandas as pd

from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter

from app.models.test_case import TestCase


def export_to_excel(
    test_cases: list[TestCase],
    output_file: str
):
    rows = []

    for test_case in test_cases:
        rows.append({
            "Test Case ID": test_case.test_case_id,
            "Requirement ID": test_case.requirement_id,
            "Title": test_case.title,
            "Preconditions": "\n".join(test_case.preconditions),
            "Test Steps": "\n".join(
                f"{i}. {step}"
                for i, step in enumerate(test_case.test_steps, 1)
            ),
            "Test Data": "\n".join(test_case.test_data),
            "Expected Result": test_case.expected_result,
            "Priority": test_case.priority,
            "Severity": test_case.severity,
            "Test Type": test_case.test_type,
            "Positive/Negative": test_case.positive_negative,
            "Automation Candidate": test_case.automation_candidate,
        })

    df = pd.DataFrame(rows)

    output_directory = os.path.dirname(output_file)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            sheet_name="Test Cases",
            index=False
        )

        worksheet = writer.sheets["Test Cases"]

        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        header_fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78"
        )

        header_font = Font(
            bold=True,
            color="FFFFFF",
            size=11
        )

        thin_side = Side(
            style="thin",
            color="D9E2F3"
        )

        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True
            )
            cell.border = Border(
                bottom=Side(
                    style="medium",
                    color="17365D"
                )
            )

        worksheet.row_dimensions[1].height = 32

        preferred_widths = {
            "A": 15,
            "B": 17,
            "C": 34,
            "D": 30,
            "E": 42,
            "F": 30,
            "G": 38,
            "H": 13,
            "I": 13,
            "J": 18,
            "K": 20,
            "L": 22,
        }

        for column_letter, width in preferred_widths.items():
            worksheet.column_dimensions[column_letter].width = width

        for row in worksheet.iter_rows(
            min_row=2,
            max_row=worksheet.max_row
        ):
            for cell in row:
                cell.alignment = Alignment(
                    vertical="top",
                    wrap_text=True
                )
                cell.border = Border(
                    bottom=thin_side
                )

            worksheet.row_dimensions[row[0].row].height = 42

        for column_letter in ["A", "B", "H", "I", "J", "K", "L"]:
            for cell in worksheet[column_letter][1:]:
                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                    wrap_text=True
                )

        # Create the Summary worksheet.
        summary = writer.book.create_sheet("Summary")

        summary["A1"] = "AI TEST CASE GENERATOR DASHBOARD"
        summary["A1"].font = Font(
            bold=True,
            size=16,
            color="FFFFFF"
        )
        summary["A1"].fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78"
        )
        summary.merge_cells("A1:B1")
        summary.row_dimensions[1].height = 30

        summary_data = [
            ["Metric", "Count"],
            ["Total Test Cases", len(test_cases)],
            [
                "High Priority",
                sum(tc.priority == "High" for tc in test_cases)
            ],
            [
                "Medium Priority",
                sum(tc.priority == "Medium" for tc in test_cases)
            ],
            [
                "Low Priority",
                sum(tc.priority == "Low" for tc in test_cases)
            ],
            [
                "Positive Tests",
                sum(tc.positive_negative == "Positive" for tc in test_cases)
            ],
            [
                "Negative Tests",
                sum(tc.positive_negative == "Negative" for tc in test_cases)
            ],
            [
                "Automation Candidates",
                sum(tc.automation_candidate for tc in test_cases)
            ],
        ]

        for row in summary_data:
            summary.append(row)

        for cell in summary[2]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="4472C4"
            )
            cell.alignment = Alignment(horizontal="center")

        for row in summary.iter_rows(min_row=3, max_row=summary.max_row):
            for cell in row:
                cell.alignment = Alignment(
                    horizontal="left" if cell.column == 1 else "center",
                    vertical="center"
                )
                cell.border = Border(bottom=thin_side)

        summary.column_dimensions["A"].width = 28
        summary.column_dimensions["B"].width = 16
        summary.freeze_panes = "A3"

        # Create a priority distribution chart.
        chart = BarChart()
        chart.type = "col"
        chart.style = 10
        chart.title = "Test Cases by Priority"
        chart.y_axis.title = "Number of Test Cases"
        chart.x_axis.title = "Priority"

        chart_data = Reference(
            summary,
            min_col=2,
            min_row=3,
            max_row=5
        )

        categories = Reference(
            summary,
            min_col=1,
            min_row=3,
            max_row=5
        )

        chart.add_data(chart_data, titles_from_data=False)
        chart.set_categories(categories)
        chart.height = 7
        chart.width = 13

        summary.add_chart(chart, "D2")

    print(f"\nExcel file created: {output_file}")
    print("Worksheets created: Test Cases, Summary")


