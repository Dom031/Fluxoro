from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QTabWidget
from PyQt5.QtCore import Qt, pyqtSignal

class UserSettingsPage(QWidget):
    # Signals for navigation
    home_signal = pyqtSignal()  
    add_sales_signal = pyqtSignal()  
    user_help_signal = pyqtSignal()  # Renamed for clarity
    logout_signal = pyqtSignal()
    dark_mode_signal = pyqtSignal(bool)  
    user_settings_signal = pyqtSignal()  # Renamed for clarity

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Worker Settings")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.title_label = QLabel("Settings")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title_label")

        # Tab Widget
        self.tabs = QTabWidget(self)
        self.general_tab = QWidget()
        self.personalization_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.personalization_tab, "Personalization")

        # General Settings (Dark Mode)
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setObjectName("darkModeCheckbox")
        self.dark_mode_checkbox.stateChanged.connect(self.handle_dark_mode)

        general_layout = QVBoxLayout()
        general_layout.addWidget(self.dark_mode_checkbox)
        self.general_tab.setLayout(general_layout)

        # Personalization Tab (Future Features)
        personalization_label = QLabel("Personalization options coming soon...")
        personalization_label.setAlignment(Qt.AlignCenter)

        personalization_layout = QVBoxLayout()
        personalization_layout.addWidget(personalization_label)
        self.personalization_tab.setLayout(personalization_layout)

        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.home_signal.emit)

        self.add_sales_button = QPushButton("Add Sales")
        self.add_sales_button.clicked.connect(self.add_sales_signal.emit)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.user_help_signal.emit)  # Updated signal

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.logout_signal.emit)

        # Navigation Buttons Layout
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.add_sales_button)
        nav_layout.addWidget(self.help_button)
        nav_layout.addWidget(self.logout_button)

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)

    def handle_dark_mode(self, state):
        """Emit signal to toggle dark mode."""
        dark_mode_enabled = (state == Qt.Checked)
        self.dark_mode_signal.emit(dark_mode_enabled)
