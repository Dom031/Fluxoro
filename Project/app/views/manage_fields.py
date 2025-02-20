from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QComboBox, QScrollArea, QLineEdit, QHeaderView, QApplication, QMessageBox
)
from PyQt5.QtCore import Qt
from app.controllers.fields_controller import FieldsController

class ManageFieldsPage(QWidget):
    def __init__(self, navigation_controller, fields_controller):
        super().__init__()
        self.setWindowTitle("Manage Fields")
        self.navigation_controller = navigation_controller
        self.fields_controller = fields_controller
        self.init_ui()

        # Adjust size dynamically (80% of screen, centered)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.move(int(screen_geometry.width() * 0.1), int(screen_geometry.height() * 0.1))

    def init_ui(self):
        """Initialize the UI layout and elements."""
        # Welcome Message
        # self.welcome_label = QLabel("Manage Fields")
        # self.welcome_label.setAlignment(Qt.AlignCenter)

        # Table for displaying fields
        self.fields_table = QTableWidget()
        self.fields_table.setColumnCount(4)  # Field Name, Field Type, Options, Date Created
        self.fields_table.setHorizontalHeaderLabels(["Field Name", "Field Type", "Options", "Date Created"])
        self.fields_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fields_table.horizontalHeader().setStretchLastSection(True)

        # Add spacing and padding to avoid overlapping
        self.fields_table.setStyleSheet("""
            QTableWidget {
                padding: 10px;
                border: 1px solid #3498DB;
            }
            QHeaderView::section {
                padding: 8px;
                border-bottom: 2px solid #3498DB;
            }
        """)

        # Text input for new field
        self.field_name_input = QLineEdit()
        self.field_name_input.setPlaceholderText("Enter field name")

        # Dropdown for field type
        self.field_type_dropdown = QComboBox()
        self.field_type_dropdown.addItems(["Product", "Service"])

        # Button to add a new field
        self.add_field_button = QPushButton("Add New Field")
        self.add_field_button.clicked.connect(self.add_new_field)

        # Layout for adding new fields
        add_field_layout = QHBoxLayout()
        add_field_layout.addWidget(self.field_name_input)
        add_field_layout.addWidget(self.field_type_dropdown)
        add_field_layout.addWidget(self.add_field_button)

        # Scroll Area for Table
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.fields_table)

        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(lambda: self.navigation_controller.go_to_home("manager"))

        self.manage_fields_button = QPushButton("Manage Fields")  # ✅ Keep visible
        self.manage_fields_button.setEnabled(False)  # ✅ Disable since we're already here

        self.reports_button = QPushButton("Reports")
        self.reports_button.clicked.connect(self.navigation_controller.go_to_reports)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(lambda: self.navigation_controller.go_to_settings("manager"))
        
        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(lambda: self.navigation_controller.go_to_help("manager"))

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.navigation_controller.logout)

        # Navigation Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.manage_fields_button)
        button_layout.addWidget(self.reports_button)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)

        # Main Layout
        main_layout = QVBoxLayout()
        # main_layout.addWidget(self.welcome_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(add_field_layout)
        self.setLayout(main_layout)

        # Load fields
        self.load_fields()

    def load_fields(self):
        """Load fields from the database and display them in the table."""
        self.fields_table.setRowCount(0)  # Clear the table first
        fields = self.fields_controller.get_fields()

        for row_index, (field_id, field_name, field_type, date_created) in enumerate(fields):
            self.fields_table.insertRow(row_index)

            self.fields_table.setItem(row_index, 0, QTableWidgetItem(field_name))
            self.fields_table.setItem(row_index, 1, QTableWidgetItem(field_type))

            # Add Delete Button
            delete_button = QPushButton("✖")  # ✅ Use an "X" icon instead of text
            delete_button.setObjectName("deleteButton")  
            delete_button.setFixedSize(40, 25)  # ✅ Smaller width and height
            delete_button.clicked.connect(lambda _, id=field_id: self.delete_field(id))

            self.fields_table.setCellWidget(row_index, 2, delete_button)

            self.fields_table.setItem(row_index, 3, QTableWidgetItem(date_created))


    def add_new_field(self):
        """Handle the addition of a new field."""
        field_name = self.field_name_input.text().strip()
        field_type = self.field_type_dropdown.currentText()

        if self.fields_controller.add_field(field_name, field_type):
            self.load_fields()  # Refresh table
            self.field_name_input.clear()  # Clear input
        else:
            print("Error adding field.")

    def delete_field(self, field_id):
        """Ask for confirmation before deleting a field."""
        confirmation = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            "Are you sure you want to delete this field?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            if self.fields_controller.delete_field(field_id):
                self.load_fields()  # Refresh table after deletion
            else:
                QMessageBox.warning(self, "Error", "Failed to delete the field.")