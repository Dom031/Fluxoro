from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox
)
from PyQt5.QtCore import (
    pyqtSignal, QTimer, Qt
)


class LoginPage(QWidget):
    login_successful = pyqtSignal(str, str)


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluxoro Login")
        self.setGeometry(100, 100, 800, 600)  # Window dimensions
        self.init_ui()

    def init_ui(self):
        # Main Layout
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignTop)

        # Logo Section
        self.logo_label = QLabel("LOGO")  # Placeholder for logo
        self.logo_label.setObjectName("logoLabel")

        # Welcome Message
        self.welcome_label = QLabel("Welcome to Fluxoro\nPlease log in to continue.")
        self.welcome_label.setObjectName("welcomeLabel")
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Username Input
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setObjectName("usernameInput")
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setEchoMode(QLineEdit.Password)

        self.show_username_checkbox = QCheckBox("Show Username")
        self.show_username_checkbox.setObjectName("showUsernameCheckbox")
        self.show_username_checkbox.stateChanged.connect(self.toggle_username_visibility)

        # Password Input
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setObjectName("passwordInput")
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setObjectName("showPasswordCheckbox")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Error Message
        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.handle_login)

        self.forgot_password_button = QPushButton("Forgot Password")
        self.forgot_password_button.setObjectName("forgotPasswordButton")
        self.forgot_password_button.setVisible(False)
        self.forgot_password_button.clicked.connect(self.handle_forgot_password)

        # Add Widgets to Layout
        form_layout.addWidget(self.logo_label)
        form_layout.addWidget(self.welcome_label)
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.show_username_checkbox)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.show_password_checkbox)
        form_layout.addWidget(self.error_label)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.forgot_password_button)

        # Apply Layout
        self.setLayout(form_layout)

    def toggle_username_visibility(self):
        """Toggle visibility of the username field."""
        if self.show_username_checkbox.isChecked():
            self.username_input.setEchoMode(QLineEdit.Normal)
        else:
            self.username_input.setEchoMode(QLineEdit.Password)

    def toggle_password_visibility(self):
        """Toggle visibility of the password field."""
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def handle_login(self):
        """Emit the login signal with username and password."""
        username = self.username_input.text()
        password = self.password_input.text()

        # Emit the signal to MainApp
        self.login_successful.emit(username, password)

    def handle_forgot_password(self):
        """Handle forgot password logic."""
        print("Forgot Password button clicked.")
