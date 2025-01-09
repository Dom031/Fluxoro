import random
import sqlite3
from datetime import datetime, timedelta

# Setup database connection
db_connection = sqlite3.connect("Project/Database/SalesApp.db")
cursor = db_connection.cursor()

# Define the field names for your sales categories
fields = [
    ("Passport Photos", 1),  # Field Name, ID (1)
    ("Albums", 2),            # Field Name, ID (2)
    ("Frames", 3),            # Field Name, ID (3)
    ("Instant Prints", 4),    # Field Name, ID (4)
    ("Film", 5)               # Field Name, ID (5)
]

# Function to generate random sales data
def generate_data():
    # Get today's date
    today = datetime.today()
    
    # Define the date range (last 3 years)
    start_date = today - timedelta(days=3 * 365)  # Start 3 years ago

    # Generate sales data for each field for the last 3 years
    for field_name, field_id in fields:
        for i in range(1, 13):  # Generate data for each month for 3 years
            for year in range(today.year - 3, today.year + 1):
                for month in range(1, 13):  # Loop through each month
                    for day in range(1, 29):  # We keep it simple for all months, you can customize it
                        # Generate a random sales value for the day (between 1 and 500)
                        amount_sold = random.randint(1, 500)
                        
                        # Insert sales data into the 'sales' table
                        sales_date = datetime(year, month, day).strftime('%Y-%m-%d')  # Format date
                        
                        # Here, all sales are paid by "Card" (as per your original request)
                        cursor.execute("INSERT INTO sales (field_id, amount_sold, date, payment_type) VALUES (?, ?, ?, ?)", 
                                       (field_id, amount_sold, sales_date, 'Card'))
                        
    # Commit the changes to the database
    db_connection.commit()

# Run the function to generate data
generate_data()
