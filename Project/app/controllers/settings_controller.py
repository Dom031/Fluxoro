import sqlite3
from app.utils.dark_mode_manager import DarkModeManager


class SettingsController:
    """Handles retrieving and updating user settings from the database."""

    def __init__(self, db_path, app):
        self.db_path = db_path
        self.app = app  # Store application reference
        self.create_settings_table()  # Ensure settings table exists

    def create_settings_table(self):
        """Create the settings table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.commit()

    def set_setting(self, key, value, role=None):
        """
        Set a specific setting value in the database.
        
        - **role**: Ensures only managers modify **restricted settings** (e.g., export format).
        """
        if role == "user" and key in ["export_format", "graph_type", "data_format"]:
            print(f"⚠️ Users cannot modify {key}.")
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO settings (key, value) 
                VALUES (?, ?) 
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """, (key, value))
            conn.commit()

    def get_setting(self, key, default=None):
        """Retrieve a specific setting value from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
            result = cursor.fetchone()
            return result[0] if result else default

    # **Export Format (CSV / PDF) [Managers Only]**
    def set_export_format(self, format, role):
        self.set_setting("export_format", format, role)

    def get_export_format(self):
        return self.get_setting("export_format", "CSV")  # Default: CSV

    # **Dark Mode Toggle**
    def set_dark_mode(self, enabled):
        """Save dark mode setting and apply the stylesheet."""
        value = "1" if enabled else "0"
        self.set_setting("dark_mode", value)
        DarkModeManager.apply_dark_mode(self.app, enabled)  # ✅ Apply immediately

    def get_dark_mode(self):
        """Retrieve dark mode setting."""
        return self.get_setting("dark_mode", "0") == "1"  # Default to False

    # **Graph Type (Bar, Pie, Line) [Managers Only]**
    def set_graph_type(self, graph_type, role):
        self.set_setting("graph_type", graph_type, role)

    def get_graph_type(self):
        return self.get_setting("graph_type", "Bar Graph")

    # **Data Format (Currency / Percentage) [Managers Only]**
    def set_data_format(self, format_type, role):
        self.set_setting("data_format", format_type, role)

    def get_data_format(self):
        return self.get_setting("data_format", "Value (£)")

    # **Language Selection [Users & Managers]**
    def set_language(self, language):
        self.set_setting("language", language)

    def get_language(self):
        return self.get_setting("language", "English")

    def set_color_blind_mode(self, mode):
        """Enable or disable color blind mode with a specific setting."""
        self.set_setting("color_blind_mode", mode)

    def get_color_blind_mode(self):
        """Retrieve color blind mode setting."""
        return self.get_setting("color_blind_mode", "None")  # Default: Off
