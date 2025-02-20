from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal

class LoginView(QWidget):
    login_successful = pyqtSignal(str, str)  # Emit role and name on login

    def __init__(self, auth_controller, navigation_controller):
        super().__init__()
        self.auth_controller = auth_controller  
        self.navigation_controller = navigation_controller  

        self.setWindowTitle("Fluxoro Login")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignTop)

        # Logo Section
        self.logo_label = QLabel("LOGO")
        self.logo_label.setObjectName("logoLabel")

        # Welcome Message
        self.welcome_label = QLabel("Welcome to Fluxoro\nPlease log in to continue.")
        self.welcome_label.setObjectName("welcomeLabel")
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setObjectName("usernameInput")
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setText("")  # Ensure field starts empty

        self.show_username_checkbox = QCheckBox("Show Username")
        self.show_username_checkbox.setChecked(True)
        self.show_username_checkbox.stateChanged.connect(self.toggle_username_visibility)

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setObjectName("passwordInput")
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Error Message
        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)

        # Sign In Button
        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.handle_login)  

        # Add Widgets to Layout
        form_layout.addWidget(self.logo_label)
        form_layout.addWidget(self.welcome_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.show_username_checkbox)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.show_password_checkbox)
        form_layout.addWidget(self.error_label)
        form_layout.addWidget(self.login_button)

        self.setLayout(form_layout)

    def toggle_username_visibility(self):
        """Toggle visibility of the username field."""
        if self.show_username_checkbox.isChecked():
            self.username_input.setEchoMode(QLineEdit.Normal)
        else:
            self.username_input.setEchoMode(QLineEdit.Password)  # Ensures it's hidden when unticked

    def toggle_password_visibility(self):
        """Toggle visibility of the password field."""
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def clear_fields(self):
        """Clears the username and password fields."""
        self.username_input.clear()
        self.password_input.clear()
        self.error_label.clear()
        self.show_username_checkbox.setChecked(True)  # Reset checkbox state
        self.show_password_checkbox.setChecked(False)

    def handle_login(self):
        """Handle login logic and navigate to the appropriate page."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.error_label.setText("Please enter both username and password.")
            return  

        user_data = self.auth_controller.validate_user(username, password)  

        if user_data:
            role, name = user_data  
            self.clear_fields()  # Clear fields on successful login
            self.close()  
            self.navigation_controller.go_to_home(role, name)  
        else:
            self.error_label.setText("Invalid username or password")
