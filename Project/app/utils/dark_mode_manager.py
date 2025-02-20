class DarkModeManager:
    """Handles applying dark mode stylesheets dynamically."""
    
    @staticmethod
    def apply_dark_mode(app, enabled):
        """Apply dark mode or reset to default."""
        stylesheet_path = "app/styles/dark_app_styles.qss" if enabled else "app/styles/app_styles.qss"
        try:
            with open(stylesheet_path, "r") as file:
                app.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"⚠️ Stylesheet {stylesheet_path} not found. Using default styling.")
