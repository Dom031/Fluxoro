from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QGroupBox, QApplication
from PyQt5.QtCore import Qt

class ManagerSettingsPage(QWidget):
    def __init__(self, navigation_controller, settings_controller):
        super().__init__()
        self.setWindowTitle("Manager Settings")
        self.navigation_controller = navigation_controller
        self.settings_controller = settings_controller
        self.init_ui()
        self.load_settings()

        # ✅ Adjust size dynamically (80% of screen, centered)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.move(int(screen_geometry.width() * 0.1), int(screen_geometry.height() * 0.1))

    def init_ui(self):
        """Initialize UI elements for Manager Settings."""
        # self.title_label = QLabel("Manager Settings")
        # self.title_label.setAlignment(Qt.AlignCenter)
        # self.title_label.setObjectName("welcomeLabel")

        # ✅ Navigation Buttons (Including "Settings" Button)
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(lambda: self.navigation_controller.go_to_home("manager"))

        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.clicked.connect(self.navigation_controller.go_to_manage_fields)

        self.reports_button = QPushButton("Reports")
        self.reports_button.clicked.connect(self.navigation_controller.go_to_reports)

        self.settings_button = QPushButton("Settings")  # ✅ Add Settings button
        self.settings_button.clicked.connect(lambda: self.navigation_controller.go_to_settings("manager"))

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(lambda: self.navigation_controller.go_to_help("manager"))

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.navigation_controller.logout)

        # ✅ Navigation Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.manage_fields_button)
        button_layout.addWidget(self.reports_button)
        button_layout.addWidget(self.settings_button)  # ✅ Ensure settings button is included
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)

        # ✅ Export Format Selection (Managers Only)
        self.export_format_dropdown = self.create_dropdown(["CSV", "PDF"], self.change_export_format)

        # ✅ Graph Type Selection
        self.graph_type_dropdown = self.create_dropdown(["Bar Graph", "Pie Chart", "Line Graph"], self.change_graph_type)

        # ✅ Data Format Selection (Currency / Percentage)
        self.data_format_dropdown = self.create_dropdown(["Value (£)", "Percentage (%)"], self.change_data_format)
        
        # ✅ Color Blind Mode Selection
        self.color_blind_dropdown = self.create_dropdown(
            ["None", "Protanopia", "Tritanopia", "Grayscale"],
            self.change_color_blind_mode
        )

        # ✅ Group Section for Color Blind Mode
        color_blind_group = self.create_group("Color Blind Mode", self.color_blind_dropdown)

        # ✅ Dark Mode Toggle
        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)

        # ✅ Grouped Sections
        export_group = self.create_group("Export Format", self.export_format_dropdown)
        graph_group = self.create_group("Graph Type", self.graph_type_dropdown)
        data_format_group = self.create_group("Data Format", self.data_format_dropdown)

        # ✅ Main Layout
        main_layout = QVBoxLayout()
        # main_layout.addWidget(self.title_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.dark_mode_checkbox)
        main_layout.addWidget(color_blind_group)
        main_layout.addWidget(export_group)
        main_layout.addWidget(graph_group)
        main_layout.addWidget(data_format_group)

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
        self.color_blind_dropdown.setCurrentText(self.settings_controller.get_color_blind_mode())
        self.export_format_dropdown.setCurrentText(self.settings_controller.get_export_format())
        self.graph_type_dropdown.setCurrentText(self.settings_controller.get_graph_type())
        self.data_format_dropdown.setCurrentText(self.settings_controller.get_data_format())

    def toggle_dark_mode(self, state):
        """Enable or disable dark mode via SettingsController."""
        enabled = state == Qt.Checked
        self.settings_controller.set_dark_mode(enabled)
        
    def change_export_format(self):
        format = self.export_format_dropdown.currentText()
        self.settings_controller.set_export_format(format, "manager")  # ✅ Correct order

    def change_graph_type(self):
        graph_type = self.graph_type_dropdown.currentText()
        self.settings_controller.set_graph_type(graph_type, "manager")  # ✅ Correct order

    def change_data_format(self):
        data_format = self.data_format_dropdown.currentText()
        self.settings_controller.set_data_format(data_format, "manager")  # ✅ Correct order

    def change_color_blind_mode(self):
        """Update the color blind mode setting and refresh reports page."""
        mode = self.color_blind_dropdown.currentText()
        self.settings_controller.set_color_blind_mode(mode)

        # ✅ Correct way to refresh the Reports Page
        self.navigation_controller.go_to_reports()  # ✅ This will reload the page
