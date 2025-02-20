import os
import pandas as pd
import sqlite3
from PyQt5.QtGui import QColor

class ReportsController:
    """Handles report generation, fetching, and exporting data."""

    def __init__(self, db_path, settings_controller):
        self.db_connection = sqlite3.connect(db_path)  # Correctly pass db_path from main.py
        self.settings_controller = settings_controller# Store settings controller reference

    def fetch_report_data(self, start_date, end_date):
        """Fetch sales data and compare with last year."""
        cursor = self.db_connection.cursor()
        query = f"""
            SELECT f.field_name,
                (SELECT SUM(amount_sold) FROM sales WHERE field_id = f.id AND date BETWEEN '{start_date}' AND '{end_date}') AS actual_sales,  
                (SELECT SUM(amount_sold) FROM sales WHERE field_id = f.id AND date BETWEEN date('{start_date}', '-1 year') AND date('{end_date}', '-1 year')) AS actual_sales_last_year
            FROM fields f
            WHERE EXISTS (SELECT 1 FROM sales WHERE field_id = f.id AND date BETWEEN '{start_date}' AND '{end_date}')
        """
        cursor.execute(query)
        data = cursor.fetchall()

        results = []
        for row in data:
            field_name, actual_sales, last_year_sales = row
            actual_sales = actual_sales or 0
            last_year_sales = last_year_sales or 0
            goal = last_year_sales * 1.2
            difference = actual_sales - goal
            percentage = (difference / goal) * 100 if goal != 0 else 0

            results.append({
                "field_name": field_name,
                "actual_sales": round(actual_sales, 2),
                "last_year_sales": round(last_year_sales, 2) if last_year_sales != 0 else "N/A",
                "goal": round(goal, 2),
                "difference": round(difference, 2),
                "percentage": round(percentage, 2),
            })

        return results

    def get_chart_colors(self):
        """Return appropriate colors for the sales chart based on dark mode settings."""
        dark_mode = self.settings_controller.get_dark_mode()  # Check if dark mode is enabled

        if dark_mode:
            return {
                "current_sales": QColor("#00BFFF"),  # Light Blue
                "last_year_sales": QColor("#90EE90"),  # Light Green
                "goals": QColor("#FF4500")  # Orange-Red
            }
        else:
            return {
                "current_sales": QColor("blue"),  # Normal Blue
                "last_year_sales": QColor("green"),  # Normal Green
                "goals": QColor("red")  # Normal Red
            }

    def export_report(self, report_data):
        """Export report based on user preference (CSV or PDF)."""
        if not report_data:
            return False

        # Get export format from settings
        export_format = self.settings_controller.get_export_format()

        df = pd.DataFrame(report_data)

        # Set Output directory
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if export_format == "CSV":
            file_path = os.path.join(output_dir, "sales_report.csv")
            df.to_csv(file_path, index=False)
            return file_path
        elif export_format == "PDF":
            try:
                from fpdf import FPDF  # Import PDF library only when needed
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_font("Arial", style="", size=12)

                pdf.cell(200, 10, "Sales Report", ln=True, align='C')
                pdf.ln(10)

                for entry in report_data:
                    pdf.multi_cell(0, 10, f"{entry['field_name']}: {entry['actual_sales']} sales")
                
                file_path = os.path.join(output_dir, "sales_report.pdf")
                pdf.output(file_path)
                return file_path
            except Exception as e:
                import traceback
                print("Error exporting to PDF:", str(e))
                traceback.print_exc()
                return False


        return False
