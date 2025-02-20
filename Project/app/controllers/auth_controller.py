from app.models.database_manager import DatabaseManager

class AuthController:
    def __init__(self, db_path):
        """Initializes the authentication controller with a database connection."""
        self.db = DatabaseManager(db_path)

    def validate_user(self, username, password):
        """Validates user credentials and returns role & name."""
        query = """
            SELECT role, name FROM User
            JOIN Login ON User.userID = Login.userID
            WHERE Login.username = ? AND Login.passwordHash = ?
        """
        result = self.db.fetch_results(query, (username, password))
        return result[0] if result else None  # ✅ Returns (role, name)
