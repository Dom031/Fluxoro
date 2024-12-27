from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt, pyqtSignal

class SettingsPage(QWidget):
    # Signals for navigation
    home_signal = pyqtSignal()  # Signal for home (manager role)
    manage_fields_signal = pyqtSignal()
    reports_signal = pyqtSignal()
    help_signal = pyqtSignal()
    logout_signal = pyqtSignal()
    dark_mode_signal = pyqtSignal(bool)  # Add a signal for dark mode toggle

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        
    def init_ui(self):
        # Title Label
        self.title_label = QLabel("Settings")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        
        # Dark Mode Toggle
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setObjectName("darkModeCheckbox")
        self.dark_mode_checkbox.stateChanged.connect(self.handle_dark_mode)

        # Dark Mode Section (grouped and aligned)
        self.dark_mode_layout = QHBoxLayout()
        self.dark_mode_layout.addWidget(self.dark_mode_checkbox)
        
        # Graph Options Section
        self.graph_type_label = QLabel("Graph Options")
        self.graph_type_dropdown = QComboBox()
        self.graph_type_dropdown.addItem("Bar Graph")
        self.graph_type_dropdown.addItem("Pie Chart")
        self.graph_type_dropdown.addItem("Line Graph")
        
        # Data Format Section
        self.data_format_label = QLabel("Data Format")
        self.data_format_dropdown = QComboBox()
        self.data_format_dropdown.addItem("Value (£)")
        self.data_format_dropdown.addItem("Percentage (%)")
        
        # Language Options Section
        self.language_label = QLabel("Language Options")
        self.language_dropdown = QComboBox()
        self.language_dropdown.addItem("English")
        self.language_dropdown.addItem("Portuguese")
        self.language_dropdown.addItem("Spanish")
        self.language_dropdown.addItem("French")

        # Group sections into groups using QGroupBox
        graph_group_box = QGroupBox("Graph Options")
        graph_group_layout = QVBoxLayout()
        graph_group_layout.addWidget(self.graph_type_label)
        graph_group_layout.addWidget(self.graph_type_dropdown)
        graph_group_box.setLayout(graph_group_layout)

        data_format_group_box = QGroupBox("Data Format")
        data_format_group_layout = QVBoxLayout()
        data_format_group_layout.addWidget(self.data_format_label)
        data_format_group_layout.addWidget(self.data_format_dropdown)
        data_format_group_box.setLayout(data_format_group_layout)

        language_group_box = QGroupBox("Language Options")
        language_group_layout = QVBoxLayout()
        language_group_layout.addWidget(self.language_label)
        language_group_layout.addWidget(self.language_dropdown)
        language_group_box.setLayout(language_group_layout)

        # Buttons Layout
        self.home_button = QPushButton("Home")
        self.home_button.setObjectName("homeButton")
        self.home_button.clicked.connect(self.home_signal.emit)
        
        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.setObjectName("manageFieldsButton")
        self.manage_fields_button.clicked.connect(self.manage_fields_signal.emit)

        self.reports_button = QPushButton("Reports")
        self.reports_button.setObjectName("reportsButton")
        self.reports_button.clicked.connect(self.reports_signal.emit)

        self.help_button = QPushButton("Help")
        self.help_button.setObjectName("helpButton")
        self.help_button.clicked.connect(self.help_signal.emit)

        self.logout_button = QPushButton("Log Out")
        self.logout_button.setObjectName("logoutButton")        
        self.logout_button.clicked.connect(self.logout_signal.emit)

        # Navigation Buttons Layout
        self.nav_buttons_layout = QHBoxLayout()
        self.nav_buttons_layout.addWidget(self.home_button)
        self.nav_buttons_layout.addWidget(self.manage_fields_button)
        self.nav_buttons_layout.addWidget(self.reports_button)
        self.nav_buttons_layout.addWidget(self.help_button)
        self.nav_buttons_layout.addWidget(self.logout_button)

        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)
        
        # Dark Mode Section
        self.layout.addLayout(self.dark_mode_layout)
        
        # Grouped Sections
        self.layout.addWidget(graph_group_box)
        self.layout.addWidget(data_format_group_box)
        self.layout.addWidget(language_group_box)
        
        # Navigation Buttons at the bottom
        self.layout.addLayout(self.nav_buttons_layout)
        
        self.setLayout(self.layout)

    def handle_dark_mode(self, state):
        """Emit signal to MainApp to apply the correct stylesheet."""
        dark_mode_enabled = (state == Qt.Checked)
        self.dark_mode_signal.emit(dark_mode_enabled)
