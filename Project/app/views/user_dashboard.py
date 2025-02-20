from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt

class UserDashboard(QWidget):
    def __init__(self, navigation_controller, sales_controller):
        super().__init__()
        self.setWindowTitle("Standard Dashboard")

        self.navigation_controller = navigation_controller
        self.sales_controller = sales_controller  # ✅ Store reference for sales data

        self.init_ui()
        self.update_goals()  # ✅ Fetch and update the goals when loading

        # ✅ Adjust size dynamically (80% of screen, centered)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.move(int(screen_geometry.width() * 0.1), int(screen_geometry.height() * 0.1))

    def init_ui(self):
        """Initialize the UI layout and elements."""
        self.welcome_label = QLabel("")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setObjectName("welcomeLabel")

        # ✅ Sales Overview Labels (Simple QLabel, No More QFrame)
        self.daily_goal_label = QLabel("Today's Goal: Loading...")
        self.daily_goal_label.setObjectName("dailyGoalLabel")

        self.weekly_goal_label = QLabel("Weekly Goal: Loading...")
        self.weekly_goal_label.setObjectName("weeklyGoalLabel")

        self.pending_reports_label = QLabel("Pending Reports: 0")
        self.pending_reports_label.setObjectName("pendingReportsLabel")

        # ✅ Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(lambda: self.navigation_controller.go_to_home("standard"))

        self.add_sales_button = QPushButton("Add Sales")
        self.add_sales_button.clicked.connect(self.navigation_controller.go_to_add_sales)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(lambda: self.navigation_controller.go_to_settings("standard"))

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(lambda: self.navigation_controller.go_to_help(
            "standard", self.navigation_controller.current_name  # ✅ Always pass the stored name
        ))

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.navigation_controller.logout)

        # ✅ Layout for Sales Overview
        sales_layout = QHBoxLayout()
        sales_layout.addWidget(self.daily_goal_label)
        sales_layout.addWidget(self.weekly_goal_label)
        sales_layout.addWidget(self.pending_reports_label)

        # ✅ Layout for Buttons (Horizontally Aligned)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.add_sales_button)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)

        # ✅ Main Layout (Vertically Stacked)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.welcome_label)
        main_layout.addLayout(sales_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def update_welcome_message(self, name):
        """Update the welcome message with the user's name."""
        self.welcome_label.setText(f"Welcome back, {name}!")

    def update_goals(self):
        """Fetch and update the daily and weekly sales goals dynamically."""
        daily_goal = self.sales_controller.get_daily_goal()
        weekly_goal = self.sales_controller.get_weekly_goal()

        # ✅ Update QLabel values directly
        self.daily_goal_label.setText(f"Today's Goal: £{daily_goal:.2f}")
        self.weekly_goal_label.setText(f"Weekly Goal: £{weekly_goal:.2f}")
