# test_main.py
import unittest
import os
import pandas as pd
from datetime import datetime
from main import CSV, plot_transactions
from data_entry import get_date, get_amount, get_category, get_description, date_format

class TestCSV(unittest.TestCase):

    def setUp(self):
        """Set up a fresh CSV file for testing."""
        CSV.CSV_FILE = "test_finance_data.csv"
        if os.path.exists(CSV.CSV_FILE):
            os.remove(CSV.CSV_FILE)
        CSV.initialize_csv()

    def tearDown(self):
        """Remove the test CSV file after tests."""
        if os.path.exists(CSV.CSV_FILE):
            os.remove(CSV.CSV_FILE)

    def test_add_entry(self):
        """Test adding an entry to the CSV file."""
        date = "15-07-2024"
        amount = 100.00
        category = "Income"
        description = "Test Income"
        CSV.add_entry(date, amount, category, description)

        df = pd.read_csv(CSV.CSV_FILE)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Date"], date)
        self.assertEqual(df.iloc[0]["Amount"], amount)
        self.assertEqual(df.iloc[0]["Category"], category)
        self.assertEqual(df.iloc[0]["Description"], description)

    def test_get_transactions(self):
        """Test retrieving transactions from the CSV file."""
        date1 = "01-07-2024"
        date2 = "15-07-2024"
        amount1 = 100.00
        amount2 = 200.00
        CSV.add_entry(date1, amount1, "Income", "Test Income 1")
        CSV.add_entry(date2, amount2, "Expense", "Test Expense 1")

        result_df = CSV.get_transactions(date1, date2)
        self.assertEqual(len(result_df), 2)
        self.assertEqual(result_df.iloc[0]["Date"], date1)
        self.assertEqual(result_df.iloc[1]["Date"], date2)
        self.assertAlmostEqual(result_df["Amount"].sum(), amount1 + amount2)

class TestDataEntry(unittest.TestCase):

    def test_get_date(self):
        """Test valid and invalid date input."""
        self.assertEqual(get_date("Enter date (dd-mm-yyyy): ", "15-07-2024"), "15-07-2024")
        self.assertRaises(ValueError, get_date, "Enter date (dd-mm-yyyy): ", "invalid-date", False)

    def test_get_amount(self):
        """Test valid and invalid amount input."""
        self.assertEqual(get_amount(), 100.00)  # Provide 100.00 when prompted
        self.assertRaises(ValueError, get_amount)  # Provide invalid input

    def test_get_category(self):
        """Test valid and invalid category input."""
        self.assertEqual(get_category(), "Income")  # Provide 'I' when prompted
        self.assertRaises(ValueError, get_category)  # Provide invalid input

    def test_get_description(self):
        """Test description input."""
        self.assertEqual(get_description(), "Test Description")  # Provide 'Test Description' when prompted

class TestPlotting(unittest.TestCase):

    def test_plot_transactions(self):
        """Test that the plot function runs without error."""
        date = "15-07-2024"
        amount = 100.00
        CSV.add_entry(date, amount, "Income", "Test Income")
        df = pd.read_csv(CSV.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=date_format)
        try:
            plot_transactions(df)
        except Exception as e:
            self.fail(f"Plotting failed with exception: {e}")

if __name__ == "__main__":
    unittest.main()
