from PyQt5.QtWidgets import QApplication
from ui.login_page import LoginPage
from ui.user_dashboard import UserDashboard
from ui.manager_dashboard import ManagerDashboard 
from ui.manage_fields import ManageFieldsPage
from ui.settings_page import SettingsPage
from ui.help_page import HelpPage
import sqlite3  # Import sqlite3 for database integration
import sys
import os


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Initialize database connection
        self.db_connection = sqlite3.connect("Project/Database/SalesApp.db")
        self.cursor = self.db_connection.cursor()

        # Initialize user details
        self.role = None
        self.name = None  

        # Initialize pages
        self.login_page = LoginPage()
        self.user_dashboard = UserDashboard()
        self.manager_dashboard = ManagerDashboard()
        self.manage_fields_page = ManageFieldsPage(self.db_connection, self.cursor)
        self.settings_page = SettingsPage()
        self.help_page = HelpPage()

        # Connect signals
        self.connect_signals()

        # Apply default stylesheet
        self.apply_stylesheet("app_styles.qss")

    def connect_signals(self):
        """Connect all signals for navigation and functionality."""
        # Login Page Signals
        self.login_page.login_successful.connect(self.handle_login)

        # User Dashboard Signals
        self.user_dashboard.logout_signal.connect(self.show_login_page)
        self.user_dashboard.home_signal.connect(self.show_dashboard)

        # Manager Dashboard Signals
        self.manager_dashboard.logout_signal.connect(self.show_login_page)
        self.manager_dashboard.manage_fields_signal.connect(self.show_manage_fields)
        self.manager_dashboard.settings_signal.connect(self.show_settings_page)
        self.manager_dashboard.help_signal.connect(self.show_help_page)

        # Manage Fields Page Signals
        self.manage_fields_page.set_user_details(self.role, self.name)
        self.manage_fields_page.settings_signal.connect(self.show_settings_page)
        self.manage_fields_page.home_signal.connect(self.show_dashboard)
        self.manage_fields_page.logout_signal.connect(self.show_login_page)
        self.manage_fields_page.help_signal.connect(self.show_help_page)

        # Settings Page Signals
        self.settings_page.home_signal.connect(self.show_dashboard)
        self.settings_page.manage_fields_signal.connect(self.show_manage_fields)
        self.settings_page.reports_signal.connect(lambda: print("Reports page placeholder"))  # Placeholder
        self.settings_page.help_signal.connect(self.show_help_page)
        self.settings_page.logout_signal.connect(self.show_login_page)

        # Help Page Signals
        self.help_page.home_signal.connect(self.show_dashboard)
        self.help_page.manage_fields_signal.connect(self.show_manage_fields)
        self.help_page.logout_signal.connect(self.show_login_page)
        self.help_page.settings_signal.connect(self.show_settings_page)

        # Dark Mode Signal
        self.settings_page.dark_mode_signal.connect(self.toggle_dark_mode)

    def apply_stylesheet(self, stylesheet_filename):
        """Load and apply the stylesheet."""
        try:
            base_dir = os.path.dirname(__file__)
            stylesheet_path = os.path.join(base_dir, "styles", stylesheet_filename)
            with open(stylesheet_path, "r") as file:
                self.app.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Stylesheet {stylesheet_filename} not found. Default style will be used.")

    def toggle_dark_mode(self, dark_mode_enabled):
        """Change the stylesheet based on dark mode state."""
        if dark_mode_enabled:
            self.apply_stylesheet("dark_app_styles.qss")
        else:
            self.apply_stylesheet("app_styles.qss")

    def handle_login(self, username, password):
        """Verify login and show the corresponding dashboard."""
        query = """
            SELECT User.name, User.role 
            FROM User 
            JOIN Login ON User.userID = Login.userID 
            WHERE Login.username = ? AND Login.passwordHash = ?
        """
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            self.name, self.role = result  # Store name and role in MainApp
            self.show_dashboard()
        else:
            self.login_page.error_label.setText("Invalid username or password")

    def show_dashboard(self):
        """Switch to the appropriate dashboard screen based on role."""
        self.close_all_pages()

        if self.role == "manager":
            self.manager_dashboard.update_welcome_message(self.name)
            self.manager_dashboard.show()
        elif self.role == "standard":
            self.user_dashboard.update_welcome_message(self.name)
            self.user_dashboard.show()

    def show_login_page(self):
        """Switch back to the Login Page."""
        self.close_all_pages()
        self.login_page.show()

    def show_manage_fields(self):
        """Show the manage fields page."""
        self.close_all_pages()
        self.manage_fields_page.show()

    def show_settings_page(self):
        """Show the settings page."""
        self.close_all_pages()
        self.settings_page.show()

    def show_help_page(self):
        """Show the help page."""
        self.close_all_pages()
        self.help_page.show()

    def close_all_pages(self):
        """Close all active pages."""
        for page in [self.login_page, self.user_dashboard, self.manager_dashboard, self.manage_fields_page, self.settings_page, self.help_page]:
            page.close()

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
