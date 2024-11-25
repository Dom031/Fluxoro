from PyQt5.QtWidgets import QApplication
from ui.login_page import LoginPage
from ui.user_dashboard import UserDashboard
from ui.manager_dashboard import ManagerDashboard  # Import Manager Dashboard
from ui.manage_fields import ManageFieldsPage
import sqlite3  # Import sqlite3 for database integration
import sys
import os

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Apply the stylesheet
        self.apply_stylesheet()

        # Initialize database connection
        self.db_connection = sqlite3.connect("../Database/SalesApp.db")
        self.cursor = self.db_connection.cursor()

        # Initialize screens
        self.login_page = LoginPage()
        self.user_dashboard = UserDashboard()
        self.manager_dashboard = ManagerDashboard()
        self.manage_fields_page = ManageFieldsPage()

        # Connect signals
        self.login_page.login_successful.connect(self.handle_login)
        self.user_dashboard.logout_signal.connect(self.show_login_page)
        self.user_dashboard.home_signal.connect(self.show_dashboard)
        self.manager_dashboard.logout_signal.connect(self.show_login_page)
        self.manager_dashboard.manage_fields_signal.connect(self.show_manage_fields)

        # Add navigation back from Manage Fields to Manager Dashboard
        self.manage_fields_page.home_signal.connect(self.show_dashboard)
        self.manage_fields_page.logout_signal.connect(self.show_login_page)

    def apply_stylesheet(self):
        """Load and apply the stylesheet."""
        try:
            stylesheet_path = os.path.join("styles", "app_styles.qss")
            with open(stylesheet_path, "r") as file:
                self.app.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Stylesheet not found. Default style will be used.")

    def handle_login(self, username, password):
        """Verify login and navigate to the appropriate dashboard."""
        role = self.verify_login(username, password)
        if role:
            self.show_dashboard(role)
        else:
            # Display an error message if login fails
            self.login_page.error_label.setText("Invalid username or password")

    def verify_login(self, username, password):
        """Check the login credentials in the database."""
        query = """
            SELECT role 
            FROM User 
            WHERE userID = (SELECT userID FROM Login WHERE username = ? AND passwordHash = ?)
        """
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def handle_login(self, username, password):
        """Verify login and navigate to the appropriate dashboard."""
        role = self.verify_login(username, password)  # Check the database
        if role:
            self.show_dashboard(role)  # Navigate to the appropriate dashboard
        else:
            self.login_page.error_label.setText("Invalid username or password")


    def show_dashboard(self, role):
        """Switch to the appropriate dashboard screen based on role."""
        # Close all pages
        self.login_page.close()
        self.manager_dashboard.close()
        self.user_dashboard.close()
        self.manage_fields_page.close()

        # Show the relevant dashboard
        if role == "manager":
            self.manager_dashboard.show()
        elif role == "standard":
            self.user_dashboard.show()
        else:
            print("Invalid role")

    def show_login_page(self):
        """Switch back to the Login Page."""
        self.user_dashboard.close()
        self.manager_dashboard.close()
        self.manage_fields_page.close()
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

    def show_manage_fields(self):
        """Switch to the Manage Fields Page."""
        self.manager_dashboard.close()  # Close the Manager Dashboard
        self.manage_fields_page.show()

    def close_connection(self):
        """Close the database connection."""
        self.db_connection.close()

    def run(self):
        """Run the application."""
        self.login_page.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = MainApp()
    app.run()
