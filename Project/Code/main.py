from PyQt5.QtWidgets import QApplication
from ui.login_page import LoginPage
from ui.user_dashboard import UserDashboard
from ui.manager_dashboard import ManagerDashboard  # Import Manager Dashboard
from ui.manage_fields import ManageFieldsPage
from ui.settings_page import SettingsPage
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
        
        # Initialize screens
        self.login_page = LoginPage()
        self.user_dashboard = UserDashboard()
        self.manager_dashboard = ManagerDashboard()
        self.manage_fields_page = ManageFieldsPage(self.db_connection, self.cursor)
        self.settings_page = SettingsPage()
        
        # Connect dark mode signal from SettingsPage to the toggle_dark_mode method
        self.settings_page.dark_mode_signal.connect(self.toggle_dark_mode)
        self.apply_stylesheet("app_styles.qss")

        # Connect signals
        self.login_page.login_successful.connect(self.handle_login)
        self.user_dashboard.logout_signal.connect(self.show_login_page)
        self.user_dashboard.home_signal.connect(self.show_dashboard)
        self.manager_dashboard.logout_signal.connect(self.show_login_page)
        self.manager_dashboard.manage_fields_signal.connect(self.show_manage_fields)
        self.manage_fields_page.set_user_details(self.role, self.name)
        self.manager_dashboard.settings_signal.connect(self.show_settings_page)
        self.manage_fields_page.settings_signal.connect(self.show_settings_page)


        # Add navigation back from Manage Fields to Manager Dashboard
        self.manage_fields_page.home_signal.connect(self.show_dashboard)
        self.manage_fields_page.logout_signal.connect(self.show_login_page)
        
        # Add navigation signals
        self.settings_page.home_signal.connect(self.show_dashboard)
        self.settings_page.manage_fields_signal.connect(self.show_manage_fields)
        self.settings_page.reports_signal.connect(lambda: print("Reports page placeholder"))
        self.settings_page.help_signal.connect(lambda: print("Help page placeholder"))
        self.settings_page.logout_signal.connect(self.show_login_page)
        
    def apply_stylesheet(self, stylesheet_filename):
        """Load and apply the stylesheet."""
        try:
            base_dir = os.path.dirname(__file__)
            stylesheet_path = os.path.join(base_dir, "styles", stylesheet_filename)
            print(f"Applying stylesheet: {stylesheet_path}")  # Debugging line
            with open(stylesheet_path, "r") as file:
                self.app.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Stylesheet {stylesheet_filename} not found. Default style will be used.")

    def toggle_dark_mode(self, dark_mode_enabled):
        """Change the stylesheet based on dark mode state."""
        print(f"Dark Mode yes or no : {dark_mode_enabled}")  # Debugging line
        if dark_mode_enabled:
            self.apply_stylesheet("dark_app_styles.qss")
        else:
            self.apply_stylesheet("app_styles.qss")

                
            
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
            self.show_dashboard(self.role, self.name)
        else:
            self.login_page.error_label.setText("Invalid username or password")


    def show_dashboard(self, role=None, name=None):
        """Switch to the appropriate dashboard screen based on role."""
        #stored name and role from handle_login
        role = role or self.role
        name = name or self.name
        # Close all pages
        self.login_page.close()
        self.manager_dashboard.close()
        self.user_dashboard.close()
        self.manage_fields_page.close()
        self.settings_page.close()  

        # Show the relevant dashboard
        if role == "manager":
            self.manager_dashboard.update_welcome_message(name)
            self.manager_dashboard.show()
        elif role == "standard":
            self.user_dashboard.update_welcome_message(name)
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


    def close_connection(self):
        """Close the database connection."""
        self.db_connection.close()

    def run(self):
        """Run the application."""
        self.login_page.show()
        sys.exit(self.app.exec_())


    def close_all_pages(self):
        """Close all active pages."""
        for page in [self.login_page, self.user_dashboard, self.manager_dashboard, self.manage_fields_page, self.settings_page]:
            page.close()

    def show_manage_fields(self):
        """Switch to the Manage Fields Page."""
        self.close_all_pages()  # Close the Manager Dashboard
        self.manage_fields_page.show()
        
    def show_settings_page(self):
        """Show the settings page."""
        self.close_all_pages()
        self.settings_page.show()
        
if __name__ == "__main__":
    app = MainApp()
    app.run()
