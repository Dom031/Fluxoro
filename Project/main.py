import sys
from PyQt5.QtWidgets import QApplication
from app.controllers.navigation_controller import NavigationController
from app.controllers.sales_controller import SalesController
from app.controllers.auth_controller import AuthController
from app.controllers.fields_controller import FieldsController
from app.controllers.reports_controller import ReportsController
from app.controllers.settings_controller import SettingsController
from app.controllers.add_sales_controller import AddSalesController
from app.views.add_sales_view import AddSalesPage
from app.views.login_view import LoginView
from app.views.manager_dashboard import ManagerDashboard
from app.views.user_dashboard import UserDashboard
from app.views.reports_view import ReportsPage
from app.views.manager_settings_view import ManagerSettingsPage
from app.views.user_settings_view import UserSettingsPage
from app.utils.dark_mode_manager import DarkModeManager
from app.models.database_manager import DatabaseManager 

def apply_stylesheet(app, stylesheet_path):
    """Loads and applies the QSS stylesheet globally."""
    try:
        with open(stylesheet_path, "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print(f"⚠️ Stylesheet {stylesheet_path} not found. Using default styling.")


def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)

    db_manager = DatabaseManager("database/SalesApp.db")


    # Initialize controllers
    navigation_controller = NavigationController()
    sales_controller = SalesController("database/SalesApp.db")
    auth_controller = AuthController("database/SalesApp.db")
    fields_controller = FieldsController("database/SalesApp.db")
    settings_controller = SettingsController("database/SalesApp.db", app) 
    reports_controller = ReportsController("database/SalesApp.db", settings_controller)
    add_sales_controller = AddSalesController(db_manager)

    # Apply stored Dark Mode setting
    DarkModeManager.apply_dark_mode(app, settings_controller.get_dark_mode())

    # Apply QSS
    apply_stylesheet(app, "app/styles/app_styles.qss")

    # Initialize views
    login_view = LoginView(auth_controller, navigation_controller)
    manager_dashboard = ManagerDashboard(navigation_controller, sales_controller)
    user_dashboard = UserDashboard(navigation_controller, sales_controller)
    reports_page = ReportsPage(navigation_controller, reports_controller)
    add_sales_page = AddSalesPage(navigation_controller, add_sales_controller)

    # Initialize different settings pages based on role
    manager_settings_page = ManagerSettingsPage(navigation_controller, settings_controller)
    user_settings_page = UserSettingsPage(navigation_controller, settings_controller)

    # Assign views to navigation controller
    navigation_controller.set_views(manager_dashboard, user_dashboard, login_view)
    navigation_controller.set_fields_controller(fields_controller)
    navigation_controller.set_reports_page(reports_page)
    navigation_controller.set_settings_pages(manager_settings_page, user_settings_page)  # ✅ Set both settings pages

    # Ensure navigation to the correct dashboard
    navigation_controller.navigate_to_home.connect(lambda role, name: navigation_controller.go_to_home(role, name))
    navigation_controller.navigate_to_help.connect(lambda role, name: navigation_controller.go_to_help(role, name))
    navigation_controller.navigate_to_settings.connect(lambda role: navigation_controller.go_to_settings(role))
    navigation_controller.navigate_to_reports.connect(navigation_controller.go_to_reports)
    navigation_controller.set_add_sales_page(add_sales_page)

    login_view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
