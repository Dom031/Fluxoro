import sqlite3

class FieldsController:
    """Handles all database interactions related to fields."""
    
    def __init__(self, db_path):
        """Initialize database connection."""
        self.db_path = db_path

    def _connect(self):
        """Create a new database connection."""
        return sqlite3.connect(self.db_path)

    def get_fields(self):
        """Fetch all fields from the database."""
        query = "SELECT id, field_name, field_type, date_created FROM Fields"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching fields: {e}")
            return []

    def add_field(self, field_name, field_type):
        """Insert a new field into the database."""
        if not field_name:
            return False  # Prevent empty names

        query = "INSERT INTO Fields (field_name, field_type, date_created) VALUES (?, ?, date('now'))"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (field_name, field_type))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding field: {e}")
            return False

    def delete_field(self, field_id):
        """Delete a field by its ID."""
        query = "DELETE FROM Fields WHERE id = ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (field_id,))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting field: {e}")
            return False
