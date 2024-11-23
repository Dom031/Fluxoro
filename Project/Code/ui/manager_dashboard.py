from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class ManagerDashboard(QWidget):
    
    logout_signal = pyqtSignal()  # Signal for logout

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manager Dashboard")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        # Welcome Message
        self.welcome_label = QLabel("Welcome back, Manager!")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setObjectName("welcomeLabel")

        # Sales Overview Placeholder
        self.sales_label = QLabel("Today's Sales: £0.00")
        self.sales_label.setAlignment(Qt.AlignCenter)
        self.sales_label.setObjectName("salesLabel")

        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.setObjectName("homeButton")
        
        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.setObjectName("manageFieldsButton")
        
        self.view_reports_button = QPushButton("Reports")
        self.view_reports_button.setObjectName("viewReportsButton")
    
        self.settings_button = QPushButton("Settings")
        self.settings_button.setObjectName("settingsButton")
        
        self.help_button = QPushButton("Help")
        self.help_button.setObjectName("helpButton")         
        
        self.logout_button = QPushButton("Log Out")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.handle_logout)    

        # Layout for Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.manage_fields_button)
        button_layout.addWidget(self.view_reports_button)
        button_layout.addWidget(self.settings_button )
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.welcome_label)
        main_layout.addWidget(self.sales_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def handle_logout(self):
        """Emit the logout signal when the button is clicked."""
        self.logout_signal.emit()