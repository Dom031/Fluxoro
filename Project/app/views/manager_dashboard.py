from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt

class ManagerDashboard(QWidget):
    def __init__(self, navigation_controller, sales_controller):
        super().__init__()
        self.setWindowTitle("Manager Dashboard")

        self.navigation_controller = navigation_controller
        self.sales_controller = sales_controller  

        self.init_ui()
        self.update_sales()  # ✅ Update weekly/monthly sales when the page loads

        # ✅ Adjust size dynamically (80% of screen, centered)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.move(int(screen_geometry.width() * 0.1), int(screen_geometry.height() * 0.1))

    def init_ui(self):
        """Initialize the UI layout and elements."""
        self.welcome_label = QLabel("")  # ✅ Empty initially, updated later
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setObjectName("welcomeLabel")

        # ✅ Sales Overview Labels (Not Using QFrame Anymore)
        self.weekly_sale_label = QLabel("Weekly Sales: £0.00")
        self.weekly_sale_label.setObjectName("weeklySalesLabel")

        self.monthly_sales_label = QLabel("Monthly Sales: £0.00")
        self.monthly_sales_label.setObjectName("monthlySalesLabel")

        self.pending_reports_label = QLabel("Pending Reports: 0")
        self.pending_reports_label.setObjectName("pendingReportsLabel")

        # ✅ Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(lambda: self.navigation_controller.go_to_home("manager"))

        self.manage_fields_button = QPushButton("Manage Fields")
        self.manage_fields_button.clicked.connect(self.navigation_controller.go_to_manage_fields)

        self.reports_button = QPushButton("Reports")
        self.reports_button.clicked.connect(self.navigation_controller.go_to_reports)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(lambda: self.navigation_controller.go_to_settings("manager"))

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(lambda: self.navigation_controller.go_to_help(
            "manager", self.navigation_controller.current_name  # ✅ Always pass the stored name
        ))

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.navigation_controller.logout)

        # ✅ Layout for Sales
        sales_layout = QHBoxLayout()
        sales_layout.addWidget(self.weekly_sale_label)
        sales_layout.addWidget(self.monthly_sales_label)
        sales_layout.addWidget(self.pending_reports_label)

        # ✅ Layout for Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.manage_fields_button)
        button_layout.addWidget(self.reports_button)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)

        # ✅ Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.welcome_label) 
        main_layout.addLayout(sales_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def update_welcome_message(self, name):
        """Update the welcome message with the manager's name."""
        self.welcome_label.setText(f"Welcome back, {name}!")

    def update_sales(self):
        """Fetch and update the weekly and monthly sales dynamically."""
        weekly_sales = self.sales_controller.get_weekly_sales()
        monthly_sales = self.sales_controller.get_monthly_sales()

        # ✅ Update labels instead of QFrame widgets
        self.weekly_sale_label.setText(f"Weekly Sales: £{weekly_sales:.2f}")
        self.monthly_sales_label.setText(f"Monthly Sales: £{monthly_sales:.2f}")
