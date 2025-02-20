import random
import sqlite3
from datetime import datetime

# Setup database connection
db_connection = sqlite3.connect("database/SalesApp.db")
cursor = db_connection.cursor()

# Fetch all field IDs dynamically from the database
cursor.execute("SELECT id, field_name FROM fields")
fields = cursor.fetchall()  # List of (id, field_name)

# Payment types to randomly alternate
payment_types = ["Card", "Cash"]

# Function to generate random sales data for 2024-2025
def generate_data():
    start_year = 2024
    end_year = 2025  # ✅ Covers full 2024 and 2025

    for field_id, field_name in fields:
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):  # ✅ January - December
                for day in range(1, 29):  # ✅ Avoids Feb 30/31 issues
                    # Generate a random float sales value between 0.01 and 500.99
                    amount_sold = round(random.uniform(0.01, 500.99), 2)

                    # Randomly select "Card" or "Cash"
                    payment_type = random.choice(payment_types)
                    
                    # Format date
                    sales_date = datetime(year, month, day).strftime('%Y-%m-%d')  
                    
                    # Insert into 'sales' table with random payment type
                    cursor.execute("INSERT INTO sales (field_id, amount_sold, date, payment_type) VALUES (?, ?, ?, ?)", 
                                   (field_id, amount_sold, sales_date, payment_type))
    
    # Commit changes to database
    db_connection.commit()

# Run the function to generate sales data
generate_data()

print("✅ Sales data for 2024-2025 has been successfully added with random payment types.")

# Close the database connection
db_connection.close()
