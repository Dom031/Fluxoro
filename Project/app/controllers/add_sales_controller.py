from app.models.sales_model import SalesModel

class AddSalesController:
    def __init__(self, db_manager):
        """Initializes the controller with the database manager."""
        self.sales_model = SalesModel(db_manager)

    def get_fields(self):
        """Fetch available fields for sales entry."""
        return self.sales_model.get_available_fields()

    def save_sale(self, field_id, amount_sold, date, payment_type):
        """Validate and save sales data."""
        if amount_sold <= 0:
            return False, "Amount must be greater than 0."
        if not payment_type:
            return False, "Please select a payment type."
        
        success = self.sales_model.save_sales(field_id, amount_sold, date, payment_type)
        if success:
            return True, "Sale saved successfully!"
        return False, "Failed to save sale."
