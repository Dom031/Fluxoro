from PyQt5.QtWidgets import QApplication
from ui.login_page import LoginPage
from ui.user_dashboard import UserDashboard
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

        # Connect signals
        self.login_page.login_successful.connect(self.show_user_dashboard)

    def apply_stylesheet(self):
        """Load and apply the stylesheet."""
        try:
            stylesheet_path = os.path.join("styles", "app_styles.qss")
            with open(stylesheet_path, "r") as file:
                self.app.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Stylesheet not found. Default style will be used.")

    def show_user_dashboard(self):
        """Switch to the User Dashboard screen."""
        self.login_page.close()
        self.user_dashboard.show()

    def run(self):
        """Run the application."""
        self.login_page.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = MainApp()
    app.run()
