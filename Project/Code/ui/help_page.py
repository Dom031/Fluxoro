from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal

class HelpPage(QWidget):
    # Signals for navigation
    home_signal = pyqtSignal()  # Signal for home (manager role)
    manage_fields_signal = pyqtSignal()
    reports_signal = pyqtSignal()
    help_signal = pyqtSignal()
    logout_signal = pyqtSignal()
    dark_mode_signal = pyqtSignal(bool)  # Add a signal for dark mode toggle

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        
    def init_ui(self):
        # Title Label
        self.title_label = QLabel("Help and Support")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("helpTitle")

        # Content Section
        self.content_layout = QVBoxLayout()
        
        # Introduction section
        self.intro_label = QLabel("Welcome to the Help Page!\n\nHere you can find guidance on how to use the app.")
        self.content_layout.addWidget(self.intro_label)
        
        # FAQ Section
        self.faq_title = QLabel("Frequently Asked Questions")
        self.content_layout.addWidget(self.faq_title)
        
        self.faq_content = QLabel("Q1: How do I add new fields?\nA1: Click the 'Add New Field' button in the Manage Fields page.")
        self.content_layout.addWidget(self.faq_content)

        # Navigation Tips
        self.nav_tips_title = QLabel("Navigation Tips")
        self.content_layout.addWidget(self.nav_tips_title)
        
        self.nav_tips_content = QLabel("Use the top navigation bar to go between the Dashboard, Manage Fields, and Settings.")
        self.content_layout.addWidget(self.nav_tips_content)

        # Create a QWidget to hold the layout and set it in the scroll area
        content_widget = QWidget()
        content_widget.setLayout(self.content_layout)

        # Scroll Area for Content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)  # Set the QWidget as the widget for the scroll area

        # Navigation Buttons
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

        # Adding layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(self.nav_buttons_layout)
        main_layout.addWidget(scroll_area)  # Add the scroll area with content to the main layout

        self.setLayout(main_layout)
