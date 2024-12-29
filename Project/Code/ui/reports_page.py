from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QDate, Qt, pyqtSignal
import pandas as pd  # Import pandas for export functionality


class ReportsPage(QWidget):
    # Define signals for navigation
    home_signal = pyqtSignal()  # Signal to go to the home page
    settings_signal = pyqtSignal()  # Signal to go to the settings page
    manage_fields_signal = pyqtSignal()  # Signal to go to the manage fields page
    logout_signal = pyqtSignal()  # Signal for logout

    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection  # Store the database connection for queries
        self.setWindowTitle("Reports")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        # Title Label
        self.title_label = QLabel("Sales Report")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Date Pickers for start and end date
        self.start_date_picker = QDateEdit(self)
        self.end_date_picker = QDateEdit(self)
        self.start_date_picker.setDate(QDate.currentDate())  # Default to current date
        self.end_date_picker.setDate(QDate.currentDate())  # Default to current date

        # Button to generate report
        self.generate_report_button = QPushButton("Generate Report")
        self.generate_report_button.clicked.connect(self.generate_report)

        # Button to export report
        self.export_button = QPushButton("Export Report")
        self.export_button.clicked.connect(self.export_report)

        # Table to display the report
        self.report_table = QTableWidget(self)
        self.report_table.setRowCount(0)  # Initially no rows
        self.report_table.setColumnCount(5)  # Adjust based on your report columns
        self.report_table.setHorizontalHeaderLabels(["Field Name", "Actual Sales", "Goal", "Difference", "Percentage"])

        # Navigation Buttons (for Home, Settings, etc.)
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.home_signal.emit)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.settings_signal.emit)

        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.clicked.connect(self.manage_fields_signal.emit)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout_signal.emit)

        # Horizontal Layout for the navigation bar
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.settings_button)
        nav_layout.addWidget(self.manage_fields_button)
        nav_layout.addWidget(self.logout_button)

        # Layout setup
        layout = QVBoxLayout(self)
        layout.addLayout(nav_layout)
        layout.addWidget(self.title_label)
        layout.addWidget(self.start_date_picker)
        layout.addWidget(self.end_date_picker)
        layout.addWidget(self.generate_report_button)
        layout.addWidget(self.report_table)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

    def generate_report(self):
        start_date = self.start_date_picker.date().toString('yyyy-MM-dd')
        end_date = self.end_date_picker.date().toString('yyyy-MM-dd')
        print(f"Generating report from {start_date} to {end_date}")

        # Fetch report data from the database
        self.fetch_report_data(start_date, end_date)

    def fetch_report_data(self, start_date, end_date):
        # Query to fetch the sales report data from the database
        query = f"""
            SELECT 
                f.field_name, 
                SUM(s.amount_sold) AS actual_sales,
                SUM(s.amount_sold) * 1.2 AS goal,  -- Assuming 20% more than last year's sales as the goal
                (SUM(s.amount_sold) - (SUM(s.amount_sold) * 1.2)) AS difference, 
                ((SUM(s.amount_sold) - (SUM(s.amount_sold) * 1.2)) / (SUM(s.amount_sold) * 1.2)) * 100 AS percentage_diff
            FROM sales s
            JOIN fields f ON s.field_id = f.id
            WHERE s.date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY s.field_id, f.field_name;
        """

        cursor = self.db_connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # Print the data to verify it's being fetched
        print("Fetched Data:", data)

        # Populate the table with the fetched data
        self.report_table.setRowCount(len(data))  # Adjust row count based on data
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.report_table.setItem(row, col, QTableWidgetItem(str(value)))

    def export_report(self):
        print("Exporting report...")

        # Get the data from the table to export
        rows = []
        for row in range(self.report_table.rowCount()):
            row_data = []
            for col in range(self.report_table.columnCount()):
                item = self.report_table.item(row, col)
                if item is not None:  # Check for None before appending
                    row_data.append(item.text())
            rows.append(row_data)

        # Check the collected rows data
        print("Rows for export:", rows)

        if rows:
            # Convert the data to a pandas DataFrame
            df = pd.DataFrame(rows, columns=["Field Name", "Actual Sales", "Goal", "Difference", "Percentage"])        
            df.to_csv("sales_report.csv", index=False)
            print("Report exported as CSV.")

            # Export to Excel
            try:
                df.to_excel("sales_report.xlsx", index=False)
                print("Report exported as Excel.")
            except Exception as e:
                print("Error exporting to Excel:", e)
        else:
            print("No data to export.")
