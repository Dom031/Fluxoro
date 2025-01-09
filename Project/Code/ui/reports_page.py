from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QDate, Qt, pyqtSignal
import pandas as pd
import os

class ReportsPage(QWidget):
    # Define signals for navigation
    home_signal = pyqtSignal()
    settings_signal = pyqtSignal()
    manage_fields_signal = pyqtSignal()
    logout_signal = pyqtSignal()
    reports_signal = pyqtSignal()
    help_signal = pyqtSignal()

    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.setWindowTitle("Reports")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        # Title Label
        self.title_label = QLabel("Sales Report")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Tab Widget for Day, Week, Month
        self.tabs = QTabWidget(self)
        self.day_tab = QWidget()
        self.week_tab = QWidget()
        self.month_tab = QWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(self.day_tab, "Day")
        self.tabs.addTab(self.week_tab, "Week")
        self.tabs.addTab(self.month_tab, "Month")

        # Layout for the tab pages
        self.day_layout = QVBoxLayout()
        self.week_layout = QVBoxLayout()
        self.month_layout = QVBoxLayout()

        self.day_tab.setLayout(self.day_layout)
        self.week_tab.setLayout(self.week_layout)
        self.month_tab.setLayout(self.month_layout)

        # Generate Report Button
        self.generate_report_button = QPushButton("Generate Report")
        self.generate_report_button.clicked.connect(self.generate_report)

        # Export Report Button
        self.export_button = QPushButton("Export Report")
        self.export_button.clicked.connect(self.export_report)

        # Report Table
        self.report_table = QTableWidget(self)
        self.report_table.setRowCount(0)
        self.report_table.setColumnCount(6)
        self.report_table.setHorizontalHeaderLabels(["Field Name", "Sales", "Last Year Sales", "Goal", "Difference", "Percentage"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.report_table.horizontalHeader().setStretchLastSection(True)

        # Layout for buttons and table
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.generate_report_button)
        self.button_layout.addWidget(self.export_button)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.tabs)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.report_table)

        self.setLayout(self.main_layout)

    def fetch_report_data(self, start_date, end_date):
        # Calculate dates for the same period last year
        last_year_start_date = (QDate.fromString(start_date, 'yyyy-MM-dd').addYears(-1)).toString('yyyy-MM-dd')
        last_year_end_date = (QDate.fromString(end_date, 'yyyy-MM-dd').addYears(-1)).toString('yyyy-MM-dd')

        # Query to fetch sales data
        query = f"""
            SELECT 
                f.field_name,
                (SELECT SUM(amount_sold) FROM sales WHERE field_id = f.id AND date BETWEEN '{start_date}' AND '{end_date}') AS actual_sales,  
                (SELECT SUM(amount_sold) FROM sales WHERE field_id = f.id AND date BETWEEN '{last_year_start_date}' AND '{last_year_end_date}') AS actual_sales_last_year
            FROM fields f
            WHERE EXISTS (SELECT 1 FROM sales WHERE field_id = f.id AND date BETWEEN '{start_date}' AND '{end_date}')
        """

        query += f" AND EXISTS (SELECT 1 FROM sales WHERE field_id = f.id AND date BETWEEN '{last_year_start_date}' AND '{last_year_end_date}')"

        print("Generated Query:", query)  # Debugging query

        # Execute query and fetch results
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # Initialize totals
        total_sales = 0
        total_last_year_sales = 0
        total_goal = 0
        total_difference = 0

        # Populate the table with the fetched data
        self.report_table.setRowCount(len(data) + 1)  # Add an extra row for totals
        for row, row_data in enumerate(data):
            # Extract fields
            field_name = row_data[0]
            actual_sales = row_data[1] or 0  # Sales from the current range
            last_year_sales = row_data[2] or 0  # Sales from last year

            # Calculate Goal as 20% more than last year's sales
            goal = last_year_sales * 1.2
            difference = actual_sales - goal
            percentage = (difference / goal) * 100 if goal != 0 else 0

            # Add to totals
            total_sales += actual_sales
            total_last_year_sales += last_year_sales
            total_goal += goal
            total_difference += difference

            # Prepare the row data to display
            display_data = [
                field_name,
                round(actual_sales, 2),
                round(last_year_sales, 2) if last_year_sales != 0 else "N/A",
                round(goal, 2),
                round(difference, 2),
                round(percentage, 2)
            ]

            # Populate the table row by row
            for col, value in enumerate(display_data):
                item = QTableWidgetItem(str(value))
                if col == 4 or col == 5:  # Apply color coding for Difference and Percentage
                    if col == 4:  # Difference column
                        if difference < 0:
                            item.setForeground(Qt.red)
                        elif difference > 0:
                            item.setForeground(Qt.green)
                    if col == 5:  # Percentage column
                        if percentage < 0:
                            item.setForeground(Qt.red)
                        elif percentage > 0:
                            item.setForeground(Qt.green)

                self.report_table.setItem(row, col, item)

        # Add the totals row
        total_percentage = (total_difference / total_goal) * 100 if total_goal != 0 else 0
        totals_row = [
            "Total",
            round(total_sales, 2),
            round(total_last_year_sales, 2),
            round(total_goal, 2),
            round(total_difference, 2),
            round(total_percentage, 2)
        ]

        for col, value in enumerate(totals_row):
            item = QTableWidgetItem(str(value))
            item.setBackground(Qt.gray)  # Highlight the totals row
            item.setForeground(Qt.black)  # Set the text color to black for better readability
            self.report_table.setItem(len(data), col, item)

    def generate_report(self):
        start_date = QDate.currentDate().toString('yyyy-MM-dd')
        end_date = QDate.currentDate().toString('yyyy-MM-dd')

        # Handle Day, Week, Month
        if self.tabs.currentIndex() == 0:  # Day Tab
            start_date = QDate.currentDate().toString('yyyy-MM-dd')
            end_date = QDate.currentDate().toString('yyyy-MM-dd')
        elif self.tabs.currentIndex() == 1:  # Week Tab
            start_date = QDate.currentDate().addDays(-QDate.currentDate().dayOfWeek() + 1).toString('yyyy-MM-dd')  # Start of the week (Monday)
            end_date = QDate.currentDate().addDays(7 - QDate.currentDate().dayOfWeek()).toString('yyyy-MM-dd')  # End of the week (Sunday)
        elif self.tabs.currentIndex() == 2:  # Month Tab
            start_date = QDate.currentDate().toString('yyyy-MM') + "-01"  # First day of the current month
            end_date = QDate.currentDate().toString('yyyy-MM-dd')  # Today's date

        # Fetch and display the report data
        self.fetch_report_data(start_date, end_date)

    def export_report(self):
        print("Exporting report...")

        rows = []
        for row in range(self.report_table.rowCount()):
            row_data = []
            for col in range(self.report_table.columnCount()):
                item = self.report_table.item(row, col)
                if item is not None:
                    row_data.append(item.text())
            rows.append(row_data)

        if rows:
            df = pd.DataFrame(rows, columns=["Field Name", "Sales", "Last Year Sales", "Goal", "Difference", "Percentage"])

            # Set the output directory to Project/Output (going two levels up from the current script)
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Output")

            # Ensure the output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Define the full file path for CSV and Excel files in the Output folder
            csv_file_path = os.path.join(output_dir, "sales_report.csv")
            df.to_csv(csv_file_path, index=False)
            print(f"Report exported as CSV to {csv_file_path}.")

            try:
                excel_file_path = os.path.join(output_dir, "sales_report.xlsx")
                df.to_excel(excel_file_path, index=False)
                print(f"Report exported as Excel to {excel_file_path}.")
            except Exception as e:
                print("Error exporting to Excel:", e)
        else:
            print("No data to export.")
