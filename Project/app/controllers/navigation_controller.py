from PyQt5.QtCore import QObject, pyqtSignal

class NavigationController(QObject):
    """Handles navigation between different pages in the application."""

    # Define global signals
    navigate_to_home = pyqtSignal(str)  # Emits role for home
    navigate_to_manage_fields = pyqtSignal()
    navigate_to_reports = pyqtSignal()
    navigate_to_settings = pyqtSignal(str)  # Emits role
    navigate_to_help = pyqtSignal(str)  # Emits role
    logout_signal = pyqtSignal()
    navigate_to_add_sales = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.manager_dashboard = None
        self.user_dashboard = None
        self.help_pages = {}
        self.settings_pages = {"manager": None, "user": None}  # ✅ Store both settings pages
        self.current_name = None  
        self.login_view = None  
        self.reports_page = None
        self.manage_fields_page = None

    def set_views(self, manager_dashboard, user_dashboard, login_view):
        """Assigns dashboard views and login view to the controller."""
        self.manager_dashboard = manager_dashboard
        self.user_dashboard = user_dashboard
        self.login_view = login_view  

    def set_settings_pages(self, manager_settings_page, user_settings_page):
        """Assigns both Manager and User Settings pages to the controller."""
        self.settings_pages["manager"] = manager_settings_page
        self.settings_pages["standard"] = user_settings_page

        

    def set_reports_page(self, reports_page):
        """Assign the ReportsPage to navigation controller."""
        self.reports_page = reports_page

    def go_to_settings(self, role):
        """Navigate to the correct Settings page based on user role."""
        if role not in self.settings_pages or self.settings_pages[role] is None:
            print(f"⚠️ ERROR: No settings page found for role: {role}")  # Debugging
            return
        self.show_page(self.settings_pages[role])



    def go_to_home(self, role, name=None):
        """Navigate to the home dashboard based on user role."""
        if name:
            self.current_name = name  # Store name persistently
        
        if role == "manager":
            self.manager_dashboard.update_welcome_message(self.current_name)
            self.show_page(self.manager_dashboard)
        else:
            self.user_dashboard.update_welcome_message(self.current_name)
            self.show_page(self.user_dashboard)

    def go_to_manage_fields(self):
        """Navigate to the Manage Fields page."""
        from app.views.manage_fields import ManageFieldsPage  # Lazy import

        if not self.manage_fields_page:
            self.manage_fields_page = ManageFieldsPage(self, self.fields_controller)

        self.show_page(self.manage_fields_page)

    def go_to_reports(self):
        """Navigate to the Reports page."""
        if self.reports_page:
            self.show_page(self.reports_page)

    def go_to_help(self, role, name=None):
        """Navigate to the Help page while preserving name."""
        from app.views.help_page import HelpPage  # Lazy import

        if name:
            self.current_name = name  

        if role not in self.help_pages:
            self.help_pages[role] = HelpPage(self, role, self.current_name)  

        self.show_page(self.help_pages[role])

    def set_add_sales_page(self, add_sales_page):
        """Assign the Add Sales page to the navigation controller."""
        self.add_sales_page = add_sales_page

    def go_to_add_sales(self):
        """Navigate to the Add Sales page."""
        if self.add_sales_page:
            self.show_page(self.add_sales_page)


    def logout(self):
        """Handle user logout, close all pages, and return to login."""
        self.current_name = None  

        # Close all open views
        if self.manager_dashboard:
            self.manager_dashboard.close()
        if self.user_dashboard:
            self.user_dashboard.close()
        if self.settings_pages["manager"]:
            self.settings_pages["manager"].close()
        if self.settings_pages["standard"]:
            self.settings_pages["standard"].close()
        if self.reports_page:
            self.reports_page.close()
        if self.manage_fields_page:
            self.manage_fields_page.close()
        if self.add_sales_page:
            self.add_sales_page.close()
        for help_page in self.help_pages.values():
            help_page.close()
        
        self.login_view.clear_fields()  
        self.show_page(self.login_view)  

    def show_page(self, page):
        """Close all other pages before showing the new one."""
        if self.manager_dashboard:
            self.manager_dashboard.close()
        if self.user_dashboard:
            self.user_dashboard.close()
        if self.reports_page:
            self.reports_page.close()
        if self.manage_fields_page:
            self.manage_fields_page.close()
        if self.add_sales_page:
            self.add_sales_page.close()
        if self.settings_pages["manager"]:
            self.settings_pages["manager"].close()
        if self.settings_pages["standard"]:
            self.settings_pages["standard"].close()
        for help_page in self.help_pages.values():
            help_page.close()

        page.show()

    def set_fields_controller(self, fields_controller):
        """Assign the fields controller to navigation controller."""
        self.fields_controller = fields_controller
