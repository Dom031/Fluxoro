from app.models.database_manager import DatabaseManager

class SalesModel:
    def __init__(self, db_manager: DatabaseManager):
        """Initializes the SalesModel with a database connection."""
        self.db = db_manager

    def save_sales(self, field_id, amount_sold, date, payment_type):
        """Saves a sale record in the database."""
        query = "INSERT INTO sales (field_id, amount_sold, date, payment_type) VALUES (?, ?, ?, ?)"
        return self.db.execute_query(query, (field_id, amount_sold, date, payment_type))

    def get_sales_report(self, date):
        """Retrieves sales data for a given date."""
        query = "SELECT * FROM sales WHERE date = ?"
        return self.db.fetch_results(query, (date,))

    def compare_sales_yearly(self, date):
        """Compares current sales to last year's data for the same date."""
        query = "SELECT * FROM sales WHERE date = DATE(?, '-1 year')"
        return self.db.fetch_results(query, (date,))

    def get_available_fields(self):
        """Fetch all fields (id, field_name) for sales input."""
        query = "SELECT id, field_name FROM fields"
        return self.db.fetch_results(query)