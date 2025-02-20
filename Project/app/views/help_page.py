from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QApplication
from PyQt5.QtCore import Qt

class HelpPage(QWidget):
    def __init__(self, navigation_controller, role, name):
        super().__init__()
        self.setWindowTitle("Help & Support")
        self.navigation_controller = navigation_controller
        self.role = role  # ✅ Store the user role

        # ✅ Store the name inside navigation_controller to persist across pages
        self.navigation_controller.current_name = name  

        self.init_ui()

        # ✅ Adjust size dynamically (80% of screen, centered)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.move(int(screen_geometry.width() * 0.1), int(screen_geometry.height() * 0.1))

    def init_ui(self):
        """Initialize the UI layout and elements."""
        # ✅ Title Label
        # self.title_label = QLabel("Help and Support")
        # self.title_label.setAlignment(Qt.AlignCenter)
        # self.title_label.setObjectName("helpTitle")

        # ✅ Scrollable Content Section
        content_layout = QVBoxLayout()

        # ✅ Introduction
        content_layout.addWidget(self.create_section("Welcome!", 
            "Welcome to the Help Page!\nHere you can find guidance on how to use the app."))

        # ✅ FAQ Section
        content_layout.addWidget(self.create_section("Frequently Asked Questions",
            "Q1: How do I add new fields?\nA1: Click the 'Add New Field' button in the Manage Fields page.\n\n"
            "Q2: How do I reset my password?\nA2: Go to the Settings page and select 'Reset Password'.\n\n"
            "Q3: Who can approve reports?\nA3: Only managers can approve or reject reports."))

        # ✅ Navigation Tips
        content_layout.addWidget(self.create_section("Navigation Tips", 
            "Use the top navigation bar to move between Dashboard, Manage Fields, and Settings.\n"
            "Managers have access to Reports and additional controls."))

        # ✅ Scroll Area Setup
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        # ✅ Navigation Buttons
        button_layout = QHBoxLayout()
        
        # ✅ Ensure the correct name is used when navigating home
        button_layout.addWidget(
            self.create_nav_button("Home", lambda: self.navigation_controller.go_to_home(
                self.role, self.navigation_controller.current_name  # ✅ Use stored name
            ))
        )

        if self.role == "manager":
            button_layout.addWidget(self.create_nav_button("Manage Fields", self.navigation_controller.go_to_manage_fields))
            button_layout.addWidget(self.create_nav_button("Reports", self.navigation_controller.go_to_reports))

        elif self.role == "standard":
            button_layout.addWidget(self.create_nav_button("Add Sales", self.navigation_controller.go_to_add_sales))  

        # ✅ Common Buttons for all roles
        button_layout.addWidget(
            self.create_nav_button("Settings", lambda: self.navigation_controller.go_to_settings(self.role))
        )
        button_layout.addWidget(self.create_nav_button("Help", lambda: self.navigation_controller.go_to_help(self.role, self.navigation_controller.current_name)))
        button_layout.addWidget(self.create_nav_button("Log Out", self.navigation_controller.logout))

        # ✅ Main Layout
        main_layout = QVBoxLayout()
        # main_layout.addWidget(self.title_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def create_section(self, title, content):
        """Creates a styled section with a title and content."""
        section_label = QLabel(title)
        section_label.setObjectName("sectionTitle")

        content_label = QLabel(content)
        content_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(section_label)
        layout.addWidget(content_label)

        section_widget = QWidget()
        section_widget.setLayout(layout)
        return section_widget

    def create_nav_button(self, text, callback):
        """Creates a styled navigation button with a click event."""
        button = QPushButton(text)
        button.clicked.connect(callback)
        return button
