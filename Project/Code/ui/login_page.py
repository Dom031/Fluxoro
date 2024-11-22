from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox
)
from PyQt5.QtCore import (
    pyqtSignal, QTimer, Qt
)


class LoginPage(QWidget):
    login_successful = pyqtSignal()  # Signal to notify successful login

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 400, 300)  # Window dimensions
        self.init_ui()

    def init_ui(self):
        # --- Layout ---
        form_layout = QVBoxLayout()

        # --- Logo and Welcome ---
        self.logo_label = QLabel("LOGO")  # Placeholder for a logo
        self.logo_label.setObjectName("logoLabel")

        self.welcome_label = QLabel("Welcome to Fluxoro\nPlease log in to continue.")
        self.welcome_label.setObjectName("welcomeLabel")
        self.welcome_label.setAlignment(Qt.AlignCenter)

        form_layout.addWidget(self.logo_label)
        form_layout.addWidget(self.welcome_label)

        # --- Username ---
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setObjectName("usernameInput")
        self.username_input.setEchoMode(QLineEdit.Password)

        self.show_username_checkbox = QCheckBox("Show Username")
        self.show_username_checkbox.setObjectName("showUsernameCheckbox")
        self.show_username_checkbox.stateChanged.connect(self.toggle_username_visibility)

        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.show_username_checkbox)

        # --- Password ---
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setObjectName("passwordInput")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setObjectName("showPasswordCheckbox")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.show_password_checkbox)

        # --- Buttons ---
        self.error_label = QLabel("")  # Placeholder for error messages
        self.error_label.setObjectName("errorLabel")

        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.handle_login)

        self.forgot_password_button = QPushButton("Forgot Password")
        self.forgot_password_button.setObjectName("forgotPasswordButton")
        self.forgot_password_button.setVisible(False)
        self.forgot_password_button.clicked.connect(self.handle_forgot_password)

        form_layout.addWidget(self.error_label)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.forgot_password_button)

        # --- Finalize Layout ---
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
        """Handle login logic."""
        username = self.username_input.text()
        password = self.password_input.text()

        # Placeholder: Replace with actual validation
        if username == "admin" and password == "1234":
            self.error_label.setText("")
            self.login_successful.emit()  # Emit signal for successful login
        else:
            self.error_label.setText("Invalid username or password!")
            QTimer.singleShot(3000, lambda: self.error_label.setText(""))  # Clears message after 3 seconds
            self.forgot_password_button.setVisible(True)  # Display forgot password button

    def handle_forgot_password(self):
        """Handle 'Forgot Password' logic."""
        print("Forgot Password button clicked. Implement the functionality here.")
