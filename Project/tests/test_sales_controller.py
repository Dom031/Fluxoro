import pytest
from app.controllers.sales_controller import SalesController
from app.models.database_manager import DatabaseManager
import os
import time

# Use a temporary database for testing
TEST_DB_PATH = "tests/test_sales.db"

@pytest.fixture
def setup_db():
    """Sets up a fresh test database for each test."""
    db = DatabaseManager(TEST_DB_PATH)

    # ✅ Ensure tables are fresh before running tests
    db.execute_query("DROP TABLE IF EXISTS User")
    db.execute_query("DROP TABLE IF EXISTS Login")
    db.execute_query("DROP TABLE IF EXISTS sales")

    # ✅ Create fresh tables
    db.execute_query("CREATE TABLE User (userID INTEGER PRIMARY KEY, name TEXT, role TEXT)")
    db.execute_query("CREATE TABLE Login (userID INTEGER, username TEXT, passwordHash TEXT, FOREIGN KEY(userID) REFERENCES User(userID))")
    db.execute_query("CREATE TABLE sales (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, date TEXT)")

    # ✅ Insert a test user
    db.execute_query("INSERT INTO User (name, role) VALUES ('Test User', 'standard')")
    db.execute_query("INSERT INTO Login (userID, username, passwordHash) VALUES (1, 'testuser', 'password123')")

    yield db  # Provide the database instance to tests

    # ✅ Close the database connection before cleanup
    db.close_connection()
    time.sleep(0.5)  # Prevent Windows file lock issues

    try:
        os.remove(TEST_DB_PATH)
    except PermissionError:
        print(f"Warning: Could not delete {TEST_DB_PATH}, file still in use.")


def test_validate_user(setup_db):
    """Test if user validation works."""
    sales_controller = SalesController(TEST_DB_PATH)
    
    # Correct login
    assert sales_controller.validate_user('testuser', 'password123') == 'standard'
    
    # Wrong password
    assert sales_controller.validate_user('testuser', 'wrongpassword') is None
    
    # Non-existing user
    assert sales_controller.validate_user('unknown', 'password123') is None

def test_add_sale(setup_db):
    """Test adding a sale."""
    sales_controller = SalesController(TEST_DB_PATH)

    # Add a sale and retrieve it
    sales_controller.add_sale(1, 100.50, "2025-02-18")
    report = sales_controller.generate_report("2025-02-18")

    print("Report Data:", report)  # Debugging: Print actual report data

    assert len(report) == 1  # Ensure a record was inserted

    # Check that the correct column is being accessed
    assert report[0][2] == 100.50  # Verify the amount is stored correctly
