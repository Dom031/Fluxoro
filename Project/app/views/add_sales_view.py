from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QDateEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QDate

class AddSalesPage(QWidget):
    def __init__(self, navigation_controller, sales_controller):
        super().__init__()
        self.setWindowTitle("Add Sales")
        self.navigation_controller = navigation_controller
        self.sales_controller = sales_controller
        self.fields = self.sales_controller.get_fields()
        self.init_ui()

        # ✅ Adjust size dynamically (80% of screen, centered)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.move(int(screen_geometry.width() * 0.1), int(screen_geometry.height() * 0.1))

    def init_ui(self):
        """Initialize UI elements for Add Sales Page."""
        # self.title_label = QLabel("Add Sales")
        # self.title_label.setAlignment(Qt.AlignCenter)

        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(lambda: self.navigation_controller.go_to_home("standard"))

        self.add_sales_button = QPushButton("Add Sales")
        self.add_sales_button.clicked.connect(lambda: self.navigation_controller.go_to_add_sales())

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(lambda: self.navigation_controller.go_to_settings("standard"))

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(lambda: self.navigation_controller.go_to_help("standard"))

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.navigation_controller.logout)

        # Navigation Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.add_sales_button) 
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)

        # Date Selection
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        # Sales Table
        self.sales_table = QTableWidget(self)
        self.sales_table.setRowCount(len(self.fields))
        self.sales_table.setColumnCount(3)
        self.sales_table.setHorizontalHeaderLabels(["Field Name", "Amount Sold", "Payment Type"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, (field_id, field_name) in enumerate(self.fields):
            field_item = QTableWidgetItem(field_name)
            field_item.setFlags(Qt.ItemIsEnabled)  # Make the field name non-editable
            self.sales_table.setItem(row, 0, field_item)

            amount_item = QTableWidgetItem()
            self.sales_table.setItem(row, 1, amount_item)

            payment_dropdown = QComboBox()
            payment_dropdown.addItems(["Cash", "Card", "Online"])
            self.sales_table.setCellWidget(row, 2, payment_dropdown)

        # Save Button
        self.save_button = QPushButton("Save Sales")
        self.save_button.clicked.connect(self.save_sales)

        # Layout
        main_layout = QVBoxLayout()
        # main_layout.addWidget(self.title_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.date_input)
        main_layout.addWidget(self.sales_table)
        main_layout.addWidget(self.save_button)

        self.setLayout(main_layout)

    def save_sales(self):
        """Collects and saves sales data."""
        date = self.date_input.date().toString("yyyy-MM-dd")
        for row, (field_id, _) in enumerate(self.fields):
            amount_item = self.sales_table.item(row, 1)
            payment_widget = self.sales_table.cellWidget(row, 2)
            payment_type = payment_widget.currentText() if payment_widget else None

            if amount_item and amount_item.text().strip():
                try:
                    amount_sold = float(amount_item.text())
                    success, message = self.sales_controller.save_sale(field_id, amount_sold, date, payment_type)
                    if not success:
                        QMessageBox.warning(self, "Error", message)
                        return
                except ValueError:
                    QMessageBox.warning(self, "Error", "Amount must be a valid number.")
                    return

        QMessageBox.information(self, "Success", "Sales saved successfully!")
