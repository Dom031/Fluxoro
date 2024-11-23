from PyQt5.QtWidgets import QApplication
from ui.login_page import LoginPage
from ui.user_dashboard import UserDashboard
from ui.manager_dashboard import ManagerDashboard  # Import Manager Dashboard
import sys
import os

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Apply the stylesheet
        self.apply_stylesheet()

        # Initialize screens
        self.login_page = LoginPage()
        self.user_dashboard = UserDashboard()
        self.manager_dashboard = ManagerDashboard() 
       

        # Connect signals
        self.login_page.login_successful.connect(self.show_dashboard)
        self.user_dashboard.logout_signal.connect(self.show_login_page)
        self.manager_dashboard.logout_signal.connect(self.show_login_page)


    def apply_stylesheet(self):
        """Load and apply the stylesheet."""
        try:
            stylesheet_path = os.path.join("styles", "app_styles.qss")
            with open(stylesheet_path, "r") as file:
                self.app.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Stylesheet not found. Default style will be used.")


    def show_dashboard(self, role):
        """Switch to the appropriate dashboard screen based on role."""
        self.login_page.close()
        if role == "manager":
            self.manager_dashboard.show()
        else:
            self.user_dashboard.show()

    def show_login_page(self):
        """Switch back to the Login Page."""
        self.user_dashboard.close()
        self.manager_dashboard.close()
        # Clear login inputs
        self.login_page.username_input.clear()
        self.login_page.password_input.clear()
        # Clear error label
        self.login_page.error_label.clear()
        # Reset Checkboxes
        self.login_page.show_username_checkbox.setChecked(False)
        self.login_page.show_password_checkbox.setChecked(False)
        # Show Login Page
        self.login_page.show()

    def run(self):
        """Run the application."""
        self.login_page.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = MainApp()
    app.run()
