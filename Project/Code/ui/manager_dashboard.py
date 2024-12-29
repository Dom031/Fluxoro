from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class ManagerDashboard(QWidget):
    
    logout_signal = pyqtSignal()  # Signal for logout
    home_signal = pyqtSignal(str)  # Signal for home (manager role)
    manage_fields_signal = pyqtSignal()  # Signal for manage fields
    settings_signal = pyqtSignal() # Signal for settings
    help_signal = pyqtSignal()  # Signal for help
    report_signal = pyqtSignal()  # Signal for reports
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manager Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

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
        
        
        # Layout for Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.manage_fields_button)
        button_layout.addWidget(self.reports_button)
        button_layout.addWidget(self.settings_button )
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)
        
        #Layout for Sales
        sales_layout = QHBoxLayout()
        sales_layout.addWidget(self.weekly_sale_label)
        sales_layout.addWidget(self.monthly_sales_label)
        sales_layout.addWidget(self.pending_reports_label)
                
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.welcome_label)
        main_layout.addLayout(sales_layout)
        main_layout.addWidget(self.welcome_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    
    def update_welcome_message(self, name):
        """Update the welcome message with the manager's name."""
        self.welcome_label.setText(f"Welcome back, {name}!")
        
    def handle_logout(self):
        """Emit the logout signal when the button is clicked."""
        self.close()
        self.logout_signal.emit()
            
    def handle_home(self):
        """Emit a signal to return to the Home page."""
        self.home_signal.emit("manager")  # Emit manager role signal

    def handle_manage_fields(self):
        """Handle navigation to the Manage Fields page."""
        self.manage_fields_signal.emit()

    def handle_reports(self):
        """Placeholder for reports navigation."""
        self.report_signal.emit()
    def handle_settings(self):
        """Emit the signal to show the settings page."""
        self.settings_signal.emit()

    def handle_help(self):
        """Placeholder for help navigation."""
        self.help_signal.emit()