import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        """Initializes the database connection."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=()):
        """Executes a query that modifies the database."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        return True

    def fetch_results(self, query, params=()):
        """Executes a query and returns the results."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def close_connection(self):
        """Closes the database connection."""
        self.conn.close()
