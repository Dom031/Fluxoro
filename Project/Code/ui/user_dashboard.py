from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class UserDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Dashboard")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        # Welcome Message
        self.welcome_label = QLabel("Welcome back, User!")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setObjectName("welcomeLabel")

        # Sales Overview Placeholder
        self.sales_label = QLabel("Today's Sales: £0.00")
        self.sales_label.setAlignment(Qt.AlignCenter)
        self.sales_label.setObjectName("salesLabel")

        # Navigation Buttons
        self.view_reports_button = QPushButton("View Reports")
        self.view_reports_button.setObjectName("viewReportsButton")

        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.setObjectName("manageFieldsButton")

        self.logout_button = QPushButton("Log Out")
        self.logout_button.setObjectName("logoutButton")

        # Layout for Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.view_reports_button)
        button_layout.addWidget(self.manage_fields_button)
        button_layout.addWidget(self.logout_button)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.welcome_label)
        main_layout.addWidget(self.sales_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
