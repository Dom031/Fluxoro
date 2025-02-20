from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QGroupBox, QApplication
from PyQt5.QtCore import Qt

class UserSettingsPage(QWidget):
    def __init__(self, navigation_controller, settings_controller):
        super().__init__()
        self.setWindowTitle("User Settings")
        self.navigation_controller = navigation_controller
        self.settings_controller = settings_controller
        self.init_ui()
        self.load_settings()

        # ✅ Adjust size dynamically (80% of screen, centered)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.move(int(screen_geometry.width() * 0.1), int(screen_geometry.height() * 0.1))

    def init_ui(self):
        """Initialize UI elements for User Settings."""
        # self.title_label = QLabel("User Settings")
        # self.title_label.setAlignment(Qt.AlignCenter)
        # self.title_label.setObjectName("welcomeLabel")

        # ✅ Navigation Buttons (Including "Settings" Button)
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(lambda: self.navigation_controller.go_to_home("standard"))
        
        self.add_sales_button = QPushButton("Add Sales")
        self.add_sales_button.clicked.connect(lambda: self.navigation_controller.go_to_add_sales())

        self.settings_button = QPushButton("Settings")  # ✅ Add Settings button
        self.settings_button.clicked.connect(lambda: self.navigation_controller.go_to_settings("standard"))

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(lambda: self.navigation_controller.go_to_help("standard"))

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.navigation_controller.logout)

        # ✅ Navigation Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.add_sales_button)
        button_layout.addWidget(self.settings_button) 
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)

        # ✅ Dark Mode Toggle
        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)

        # ✅ Language Selection
        self.language_dropdown = self.create_dropdown(["English", "Portuguese", "Spanish", "French"], self.change_language)

        # ✅ Grouped Sections
        language_group = self.create_group("Language", self.language_dropdown)

        # ✅ Main Layout
        main_layout = QVBoxLayout()
        # main_layout.addWidget(self.title_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.dark_mode_checkbox)
        main_layout.addWidget(language_group)

        self.setLayout(main_layout)

    def create_dropdown(self, options, change_handler):
        """Helper function to create a dropdown."""
        dropdown = QComboBox()
        dropdown.addItems(options)
        dropdown.currentIndexChanged.connect(change_handler)
        return dropdown

    def create_group(self, title, widget):
        """Helper function to create a settings section."""
        group_box = QGroupBox(title)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        group_box.setLayout(layout)
        return group_box

    def load_settings(self):
        """Load saved preferences from the database."""
        self.dark_mode_checkbox.setChecked(self.settings_controller.get_dark_mode())
        self.language_dropdown.setCurrentText(self.settings_controller.get_language())

    def toggle_dark_mode(self, state):
        """Enable or disable dark mode via SettingsController."""
        enabled = state == Qt.Checked
        self.settings_controller.set_dark_mode(enabled)

    def change_language(self):
        """Change the preferred language."""
        language = self.language_dropdown.currentText()
        self.settings_controller.set_language(language)
