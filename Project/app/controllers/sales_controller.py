from app.models.sales_model import SalesModel
from app.models.database_manager import DatabaseManager
import sqlite3

class SalesController:
    def __init__(self, db_path):
        """Initializes the SalesController with a database connection."""
        self.db = DatabaseManager(db_path)
        self.sales_model = SalesModel(self.db)

    def add_sale(self, user_id, amount, date):
        """Adds a sale record to the database."""
        return self.sales_model.save_sales(user_id, amount, date)

    def generate_report(self, date):
        """Generates a sales report for the given date."""
        return self.sales_model.get_sales_report(date)

    def compare_to_last_year(self, date):
        """Compares current sales to last year's data for the same date."""
        return self.sales_model.compare_sales_yearly(date)

    def get_daily_goal(self):
        """Fetch last year's sales for today's date and increase by 20%."""
        query = """
            SELECT COALESCE(SUM(amount_sold) * 1.2, 0) AS daily_goal
            FROM sales
            WHERE date = DATE('now', '-1 year');
        """
        return self._fetch_single_value(query)

    def get_weekly_goal(self):
        """Fetch last year's sales for the same week and increase by 20%."""
        query = """
            SELECT COALESCE(SUM(amount_sold) * 1.2, 0) AS weekly_goal
            FROM sales
            WHERE date BETWEEN DATE('now', '-1 year', 'weekday 0', '-6 days') 
            AND DATE('now', '-1 year', 'weekday 0');
        """
        return self._fetch_single_value(query)

    def get_weekly_sales(self):
        """Fetch total sales for the current week."""
        query = """
            SELECT COALESCE(SUM(amount_sold), 0) AS weekly_sales
            FROM sales
            WHERE date BETWEEN DATE('now', 'weekday 0', '-6 days')
            AND DATE('now');
        """
        result = self._fetch_single_value(query)
        return result

    def get_monthly_sales(self):
        """Fetch total sales for the current month."""
        query = """
            SELECT COALESCE(SUM(amount_sold), 0) AS monthly_sales
            FROM sales
            WHERE date BETWEEN DATE('now', 'start of month')
            AND DATE('now');
        """
        result = self._fetch_single_value(query)
        return result


    def _fetch_single_value(self, query):
        """Helper function to execute a query and return a single value."""
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()[0]  # Get the first column
            conn.close()
            return round(result, 2)  # Round for display
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0.0
