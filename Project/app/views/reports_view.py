from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QApplication
from PyQt5.QtCore import QDate, Qt
import pyqtgraph as pg # type: ignore

class ReportsPage(QWidget):
    def __init__(self, navigation_controller, reports_controller):
        super().__init__()
        self.setWindowTitle("Reports")
        self.navigation_controller = navigation_controller
        self.reports_controller = reports_controller
        self.init_ui()

        # ✅ Adjust size dynamically (80% of screen, centered)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.move(int(screen_geometry.width() * 0.1), int(screen_geometry.height() * 0.1))

    def init_ui(self):
        """Initialize the UI layout for the Reports Page."""
        
        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(lambda: self.navigation_controller.go_to_home("manager"))

        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.clicked.connect(self.navigation_controller.go_to_manage_fields)

        self.reports_button = QPushButton("Reports")  # No action needed as we're already here

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(lambda: self.navigation_controller.go_to_settings("manager"))

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(lambda: self.navigation_controller.go_to_help("manager"))

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.navigation_controller.logout)

        # ✅ NAVIGATION LAYOUT
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.manage_fields_button)
        nav_layout.addWidget(self.reports_button)
        nav_layout.addWidget(self.settings_button)
        nav_layout.addWidget(self.help_button)
        nav_layout.addWidget(self.logout_button)

        # ✅ TAB WIDGET (Day, Week, Month)
        self.tabs = QTabWidget(self)
        self.day_tab = QWidget()
        self.week_tab = QWidget()
        self.month_tab = QWidget()

        self.tabs.addTab(self.day_tab, "Day")
        self.tabs.addTab(self.week_tab, "Week")
        self.tabs.addTab(self.month_tab, "Month")

        self.day_tab.setLayout(QVBoxLayout())
        self.week_tab.setLayout(QVBoxLayout())
        self.month_tab.setLayout(QVBoxLayout())

        # ✅ BAR CHART - EXPANDED FULLY TO TOP
        self.bar_chart_widget = pg.GraphicsLayoutWidget()
        self.bar_chart_widget.setMinimumHeight(400)  # Adjust as needed
        self.bar_plot = self.bar_chart_widget.addPlot(title="Sales Comparison")
        self.bar_plot.showGrid(x=True, y=True)

        # ✅ REPORT TABLE - FIXED HEIGHT SO GRAPH EXPANDS
        self.report_table = QTableWidget(self)
        self.report_table.setRowCount(0)
        self.report_table.setColumnCount(6)
        self.report_table.setHorizontalHeaderLabels(["Field Name", "Sales", "Last Year Sales", "Goal", "Difference", "Percentage"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.report_table.setFixedHeight(250)  # Reduce table height to give more space to graph

        # ✅ BUTTONS LAYOUT
        self.generate_report_button = QPushButton("Generate Report")
        self.generate_report_button.clicked.connect(self.generate_report)

        self.export_button = QPushButton("Export Report")
        self.export_button.clicked.connect(self.export_report)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_report_button)
        button_layout.addWidget(self.export_button)

        # ✅ MAIN LAYOUT - MAKING CHART TAKE TOP SPACE
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(nav_layout)  # Navigation
        main_layout.addWidget(self.tabs)  # Tabs
        main_layout.addWidget(self.bar_chart_widget, 1)  # CHART EXPANDS FULLY
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.report_table)

        self.setLayout(main_layout)

    def generate_report(self):
        start_date = QDate.currentDate().toString('yyyy-MM-dd')
        end_date = QDate.currentDate().toString('yyyy-MM-dd')

        if self.tabs.currentIndex() == 1:
            start_date = QDate.currentDate().addDays(-QDate.currentDate().dayOfWeek() + 1).toString('yyyy-MM-dd')
            end_date = QDate.currentDate().addDays(7 - QDate.currentDate().dayOfWeek()).toString('yyyy-MM-dd')
        elif self.tabs.currentIndex() == 2:
            start_date = QDate.currentDate().toString('yyyy-MM') + "-01"
            end_date = QDate.currentDate().toString('yyyy-MM-dd')

        data = self.reports_controller.fetch_report_data(start_date, end_date)
        self.populate_table(data)
        self.generate_bar_chart(data)

    def populate_table(self, data):
        """Populate the table with report data while applying color coding."""
        self.report_table.setRowCount(len(data))

        for row, entry in enumerate(data):
            for col, key in enumerate(["field_name", "actual_sales", "last_year_sales", "goal", "difference", "percentage"]):
                if key == "percentage":
                    percentage_value = round(entry[key])  # ✅ Round to whole number
                    item = QTableWidgetItem(f"{percentage_value}%")  # ✅ Append %
                else:
                    item = QTableWidgetItem(str(entry[key]))

                # Apply color coding for "Difference" and "Percentage"
                if key == "difference" and entry[key] < 0:
                    item.setForeground(Qt.red)
                elif key == "difference" and entry[key] > 0:
                    item.setForeground(Qt.green)
                elif key == "percentage" and entry[key] < 0:
                    item.setForeground(Qt.red)
                elif key == "percentage" and entry[key] > 0:
                    item.setForeground(Qt.green)

                self.report_table.setItem(row, col, item)

    def export_report(self):
        """Export the report in the preferred format."""
        report_data = []
        for row in range(self.report_table.rowCount()):
            entry = {
                "field_name": self.report_table.item(row, 0).text(),
                "actual_sales": self.report_table.item(row, 1).text(),
                "last_year_sales": self.report_table.item(row, 2).text(),
                "goal": self.report_table.item(row, 3).text(),
                "difference": self.report_table.item(row, 4).text(),
                "percentage": self.report_table.item(row, 5).text(),
            }
            report_data.append(entry)

        file_path = self.reports_controller.export_report(report_data)
        if file_path:
            QMessageBox.information(self, "Success", f"Report exported successfully!\nSaved to: {file_path}")
        else:
            QMessageBox.warning(self, "Error", "Failed to export report.")

    def generate_bar_chart(self, data):
        """Generate a bar chart using the report data, considering color blind settings."""
        self.bar_plot.clear()

        # Fetch color blind mode from settings
        color_blind_mode = self.reports_controller.settings_controller.get_color_blind_mode()

        # Adjust colors based on mode
        if color_blind_mode == "Protanopia":
            current_sales_color = "yellow"
            last_year_sales_color = "blue"
            goals_color = "gray"
        elif color_blind_mode == "Tritanopia":
            current_sales_color = "purple"
            last_year_sales_color = "orange"
            goals_color = "gray"
        elif color_blind_mode == "Grayscale":
            current_sales_color = "gray"
            last_year_sales_color = "darkgray"
            goals_color = "lightgray"
        else:
            current_sales_color = "cyan"
            last_year_sales_color = "orange"
            goals_color = "red"

        field_names = [entry["field_name"] for entry in data]
        current_sales = [float(entry["actual_sales"]) for entry in data]
        last_year_sales = [float(entry["last_year_sales"]) if entry["last_year_sales"] != "N/A" else 0 for entry in data]
        goals = [float(entry["goal"]) for entry in data]

        x_positions = list(range(len(field_names)))
        bar_width = 0.2

        current_sales_bars = pg.BarGraphItem(x=[x - bar_width for x in x_positions], height=current_sales, width=bar_width, brush=current_sales_color)
        last_year_sales_bars = pg.BarGraphItem(x=[x for x in x_positions], height=last_year_sales, width=bar_width, brush=last_year_sales_color)
        goals_bars = pg.BarGraphItem(x=[x + bar_width for x in x_positions], height=goals, width=bar_width, brush=goals_color)

        self.bar_plot.addItem(current_sales_bars)
        self.bar_plot.addItem(last_year_sales_bars)
        self.bar_plot.addItem(goals_bars)

        x_axis_labels = [(i, field) for i, field in enumerate(field_names)]
        self.bar_plot.getAxis('bottom').setTicks([x_axis_labels])

        if not hasattr(self, 'legend'):
            self.legend = pg.LegendItem((80, 60), offset=(30, 30))
            self.legend.setParentItem(self.bar_plot.graphicsItem())
        self.legend.clear()
        self.legend.addItem(current_sales_bars, "Current Sales")
        self.legend.addItem(last_year_sales_bars, "Last Year Sales")
        self.legend.addItem(goals_bars, "Goals")
