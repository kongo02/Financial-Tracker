import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description, date_format

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["Date", "Amount", "Category", "Description"]

    @classmethod
    def initialize_csv(cls):
        """
        Initialize the CSV file with the necessary columns if it doesn't exist.
        """
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """
        Add a new transaction entry to the CSV file.
        """
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry Created Successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """
        Retrieve and display transactions between the given start and end dates.
        """
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=date_format)
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No Records Found")
        else:
            print(f"Transactions From {start_date.strftime(date_format)} To {end_date.strftime(date_format)}")
            print(filtered_df.to_string(index=False, formatters={"Date": lambda x: x.strftime(date_format)}))
            
            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            print("\n---SUMMARY---")
            print(f"Total Income: R {total_income:.2f}")
            print(f"Total Expense: R {total_expense:.2f}")
            print(f"Net Savings: R {total_income - total_expense:.2f}")

        return filtered_df

def add():
    """
    Prompt user to add a new transaction.
    """
    CSV.initialize_csv()
    date = get_date("The Date Of Transaction (dd-mm-yyyy) or Enter For Today's Date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    """
    Plot income and expense transactions over time.
    """
    df.set_index("Date", inplace=True)

    income_df = (
        df[df["Category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    expense_df = (
        df[df["Category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Bank Statement")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to drive the finance manager CLI.
    """
    while True:
        print("\n---Finance Manager---")
        print("1. Add New Transaction")
        print("2. View Transactions")
        print("3. Exit")

        choice = input("Enter Your Choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter Start Date (dd-mm-yyyy): ")
            end_date = get_date("Enter End Date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do You Want To View A Graph? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("EXIT...")
            break
        else:
            print("Invalid Choice. Please Try Again.")

if __name__ == "__main__":
    main()
