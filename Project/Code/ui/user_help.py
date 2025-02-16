from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal

class UserHelpPage(QWidget):
    # Signals for navigation
    home_signal = pyqtSignal()
    add_sales_signal = pyqtSignal()
    user_settings_signal = pyqtSignal()  # Renamed for clarity
    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Worker Help")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.title_label = QLabel("Help and Support")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("helpTitle")

        # Tab Widget
        self.tabs = QTabWidget(self)
        self.faq_tab = QWidget()
        self.troubleshooting_tab = QWidget()
        self.contact_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.faq_tab, "FAQ")
        self.tabs.addTab(self.troubleshooting_tab, "Troubleshooting")
        self.tabs.addTab(self.contact_tab, "Contact")

        # FAQ Tab
        faq_layout = QVBoxLayout()
        faq_content = QLabel(
            "Q1: How do I add sales?\nA1: Click 'Add Sales' from the dashboard.\n\n"
            "Q2: Can I view my sales history?\nA2: Yes, go to the Reports section to see sales data.\n\n"
            "Q3: What do I do if I make a mistake?\nA3: Contact a manager to correct the entry."
        )
        faq_content.setWordWrap(True)
        faq_layout.addWidget(faq_content)
        self.faq_tab.setLayout(faq_layout)

        # Troubleshooting Tab
        troubleshooting_layout = QVBoxLayout()
        troubleshooting_content = QLabel(
            "Issue: The app is not responding.\nSolution: Restart the application.\n\n"
            "Issue: I can't add sales.\nSolution: Ensure your account has the correct permissions."
        )
        troubleshooting_content.setWordWrap(True)
        troubleshooting_layout.addWidget(troubleshooting_content)
        self.troubleshooting_tab.setLayout(troubleshooting_layout)

        # Contact Tab
        contact_layout = QVBoxLayout()
        contact_content = QLabel(
            "For support, please contact:\n\n"
            "📧 Email: support@company.com\n"
            "📞 Phone: +44 123 456 789\n"
            "📍 Office: 123 Business Street, London"
        )
        contact_content.setAlignment(Qt.AlignCenter)
        contact_layout.addWidget(contact_content)
        self.contact_tab.setLayout(contact_layout)

        # Scroll Area for Help Content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.tabs)

        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.home_signal.emit)

        self.add_sales_button = QPushButton("Add Sales")
        self.add_sales_button.clicked.connect(self.add_sales_signal.emit)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.user_settings_signal.emit)  # Updated signal

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.logout_signal.emit)

        # Navigation Layout
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.add_sales_button)
        nav_layout.addWidget(self.settings_button)
        nav_layout.addWidget(self.logout_button)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)
