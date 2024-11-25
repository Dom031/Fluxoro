from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class UserDashboard(QWidget):
    logout_signal = pyqtSignal()  # Signal for logout
    home_signal = pyqtSignal(str) #signal for home
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Dashboard")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        # Welcome Message
        self.welcome_label = QLabel("Welcome back, User!")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setObjectName("welcomeLabel")

        # Sales Overview Placeholder
        self.daily_goal_label = QLabel("Today's Goal: £0.00")
        self.daily_goal_label.setObjectName("dailyGoalLabel")
        
        self.weekly_goal_label = QLabel("Weekly Goal £0.00")
        self.weekly_goal_label.setObjectName("weeklyGoalLabel")
        
        self.pending_reports_label = QLabel("Pending Reports: £0.00")
        self.pending_reports_label.setObjectName("pendingReportsLabel")
        
        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.setObjectName("homeButton")
        
        self.add_sales_button = QPushButton("Add Sales")
        self.add_sales_button.setObjectName("addSalesButton")
    
        self.settings_button = QPushButton("Settings")
        self.settings_button.setObjectName("settingsButton")
        
        self.help_button = QPushButton("Help")
        self.help_button.setObjectName("helpButton")         

        self.logout_button = QPushButton("Log Out")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.handle_logout)    


    

        # Layout for Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.add_sales_button)
        button_layout.addWidget(self.settings_button )
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.logout_button)
        #Layout for Goals
        goal_layout = QHBoxLayout()
        goal_layout.addWidget(self.daily_goal_label)
        goal_layout.addWidget(self.weekly_goal_label)
        goal_layout.addWidget(self.pending_reports_label)
                
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.welcome_label)
        main_layout.addLayout(goal_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def handle_logout(self):
        """Emit the logout signal when the button is clicked."""
        self.logout_signal.emit()
        
    def handle_home_button(self):
        """Emit a signal to return to the Home page."""
        self.home_signal.emit("user")