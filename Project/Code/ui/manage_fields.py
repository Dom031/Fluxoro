from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QScrollArea, QLineEdit, QHeaderView
from PyQt5.QtCore import Qt, pyqtSignal

class ManageFieldsPage(QWidget):

    logout_signal = pyqtSignal()  # Signal for logout
    home_signal = pyqtSignal(str, str)  # Signal for home (manager role)
    manage_fields_signal = pyqtSignal()  # Signal for manage fields
    settings_signal = pyqtSignal() # Signal for settings
    help_signal = pyqtSignal()  # Signal for help

    
    
    def __init__(self, db_connection, db_cursor):
        super().__init__()
        self.db_connection = db_connection
        self.db_cursor = db_cursor
        self.setWindowTitle("Manage Fields")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.role = None
        self.name = None

    def init_ui(self):
        # Welcome Message
        self.welcome_label = QLabel("Welcome back, Manager!")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setObjectName("welcomeLabel")

        # Sales Overview Placeholder
        self.weekly_sale_label = QLabel("Weekly Sales: £0.00")
        self.weekly_sale_label.setObjectName("weeklySalesLabel")

        self.monthly_sales_label = QLabel("Monthly Sales: £0.00")
        self.monthly_sales_label.setObjectName("monthlySalesLabel")

        self.pending_reports_label = QLabel("Pending Reports: 0")
        self.pending_reports_label.setObjectName("pendingReportsLabel")

        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.setObjectName("homeButton")
        self.home_button.clicked.connect(self.handle_home)

        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.setObjectName("manageFieldsButton")
        self.manage_fields_button.clicked.connect(self.handle_manage_fields)

        self.reports_button = QPushButton("Reports")
        self.reports_button.setObjectName("reportsButton")
        self.reports_button.clicked.connect(self.handle_reports)  # Placeholder for reports

        self.settings_button = QPushButton("Settings")
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.clicked.connect(self.handle_settings) 

        self.help_button = QPushButton("Help")
        self.help_button.setObjectName("helpButton")
        self.help_button.clicked.connect(self.handle_help)

        self.logout_button = QPushButton("Log Out")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.handle_logout)

        # --- Manage Fields Section ---
        # Table for displaying fields
        self.fields_table = QTableWidget()
        self.fields_table.setColumnCount(4)  # Field Name, Field Type, Options, Date Created
        self.fields_table.setHorizontalHeaderLabels(["Field Name", "Field Type", "Options", "Date Created"])
        self.fields_table.setObjectName("fieldsTable")
        self.fields_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fields_table.horizontalHeader().setStretchLastSection(True)

        # Text input for field name
        self.field_name_input = QLineEdit()  # Initialize here
        self.field_name_input.setPlaceholderText("Enter field name")
        self.field_name_input.setObjectName("fieldNameInput")

        # Add New Field Section
        self.field_type_dropdown = QComboBox()
        self.field_type_dropdown.addItems(["Product", "Service"])

        self.add_field_button = QPushButton("Add New Field")
        self.add_field_button.setObjectName("addFieldButton")
        self.add_field_button.clicked.connect(self.add_new_field)

        # Add New Field Section Layout
        add_field_layout = QHBoxLayout()  # Define layout only once
        add_field_layout.addWidget(self.field_name_input)  # Add the input field
        add_field_layout.addWidget(self.field_type_dropdown)
        add_field_layout.addWidget(self.add_field_button)

        # Scroll Area for Table (optional for large data)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.fields_table)

        # Layout for Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.manage_fields_button)
        button_layout.addWidget(self.reports_button)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)

        # Layout for Sales
        sales_layout = QHBoxLayout()
        sales_layout.addWidget(self.weekly_sale_label)
        sales_layout.addWidget(self.monthly_sales_label)
        sales_layout.addWidget(self.pending_reports_label)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.welcome_label)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(sales_layout)
        main_layout.addWidget(scroll_area)  # Add table inside a scroll area
        main_layout.addLayout(add_field_layout)  # Add new field section
        self.setLayout(main_layout)

        # Load initial fields
        self.load_fields()

    def populate_table(self):
        """Populate the table with placeholder data."""
        sample_data = [
            {"Field Name": "Product 1", "Field Type": "Service", "Options": "[Edit] [x]", "Date Created": "01/01/2001"},
            {"Field Name": "Product 2", "Field Type": "Product", "Options": "[Edit] [x]", "Date Created": "02/02/2003"}
        ]
        self.fields_table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            self.fields_table.setItem(row, 0, QTableWidgetItem(data["Field Name"]))
            self.fields_table.setItem(row, 1, QTableWidgetItem(data["Field Type"]))
            self.fields_table.setItem(row, 2, QTableWidgetItem(data["Options"]))
            self.fields_table.setItem(row, 3, QTableWidgetItem(data["Date Created"]))
            
            
    def handle_logout(self):
        """Emit the logout signal when the button is clicked."""
        self.logout_signal.emit()
            
    def handle_home(self):
        """Emit a signal to return to the Home page."""
        self.home_signal.emit(self.role, self.name)  # Emit role and name signal

    def handle_manage_fields(self):
        """Handle navigation to the Manage Fields page."""
        self.manage_fields_signal.emit()
    
    def set_user_details(self, role, name):
        self.role = role
        self.name = name

    def handle_reports(self):
        """Placeholder for reports navigation."""
        print("Reports button clicked!")  # Placeholder functionality

    def handle_settings(self):
        """Emit the signal to show the settings page."""
        self.settings_signal.emit()

    def handle_help(self): 
        """Emit the signal for help ."""
        self.help_signal.emit()

    def add_new_field(self):
        """Handle the addition of a new field."""
        field_type = self.field_type_dropdown.currentText()
        field_name = self.field_name_input.text().strip()  # Get text from input field

        if not field_name:
            print("Field name cannot be empty!")
            return

        try:
            query = "INSERT INTO Fields (field_name, field_type, date_created) VALUES (?, ?, date('now'))"
            self.db_cursor.execute(query, (field_name, field_type))
            self.db_connection.commit()

            self.load_fields()  # Refresh table
            print("Field added successfully!")
            self.field_name_input.clear()  # Clear the input field after adding
        except Exception as e:
            print("Error adding field:", e)
            
    def load_fields(self):
        """Load fields from the database and display them in the table."""
        try:
            query = "SELECT id, field_name, field_type, date_created FROM Fields"
            self.db_cursor.execute(query)
            rows = self.db_cursor.fetchall()

            self.fields_table.setRowCount(len(rows))
            for row_index, row_data in enumerate(rows):
                # Extract the id and other field data
                field_id, field_name, field_type, date_created = row_data

                # Set Field Name (Column 0)
                field_name_item = QTableWidgetItem(field_name)
                field_name_item.setTextAlignment(Qt.AlignCenter)
                self.fields_table.setItem(row_index, 0, field_name_item)

                # Set Field Type (Column 1)
                field_type_item = QTableWidgetItem(field_type)
                field_type_item.setTextAlignment(Qt.AlignCenter)
                self.fields_table.setItem(row_index, 1, field_type_item)

                # Add delete button in the Options column (Column 2)
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, id=field_id: self.delete_field(id))
                self.fields_table.setCellWidget(row_index, 2, delete_button)

                # Set Date Created (Column 3)
                date_item = QTableWidgetItem(date_created)  # Already formatted as YYYY-MM-DD in the database
                date_item.setTextAlignment(Qt.AlignCenter)
                self.fields_table.setItem(row_index, 3, date_item)
        except Exception as e:
            print(f"Error loading fields: {e}")
            
    def delete_field(self, field_id):
        """Delete a field from the database."""
        try:
            query = "DELETE FROM Fields WHERE id = ?"
            self.db_cursor.execute(query, (field_id,))
            self.db_connection.commit()
            self.load_fields()  # Refresh table
            print("Field deleted successfully!")
        except Exception as e:
            print(f"Error deleting field: {e}")