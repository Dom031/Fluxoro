from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class BasePage(QWidget):
    # Common signals for navigation
    home_signal = pyqtSignal()
    manage_fields_signal = pyqtSignal()
    reports_signal = pyqtSignal()
    settings_signal = pyqtSignal()
    help_signal = pyqtSignal()
    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_navigation()

    def init_navigation(self):
        """Initialize the navigation buttons and layout."""
        self.home_button = QPushButton("Home")
        self.home_button.setObjectName("homeButton")
        self.home_button.clicked.connect(self.home_signal.emit)

        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.setObjectName("manageFieldsButton")
        self.manage_fields_button.clicked.connect(self.manage_fields_signal.emit)

        self.reports_button = QPushButton("Reports")
        self.reports_button.setObjectName("reportsButton")
        self.reports_button.clicked.connect(self.reports_signal.emit)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.clicked.connect(self.settings_signal.emit)

        self.help_button = QPushButton("Help")
        self.help_button.setObjectName("helpButton")
        self.help_button.clicked.connect(self.help_signal.emit)

        self.logout_button = QPushButton("Log Out")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.logout_signal.emit)

        # Navigation layout
        self.nav_buttons_layout = QHBoxLayout()
        self.nav_buttons_layout.addWidget(self.home_button)
        self.nav_buttons_layout.addWidget(self.manage_fields_button)
        self.nav_buttons_layout.addWidget(self.reports_button)
        self.nav_buttons_layout.addWidget(self.settings_button)
        self.nav_buttons_layout.addWidget(self.help_button)
        self.nav_buttons_layout.addWidget(self.logout_button)
