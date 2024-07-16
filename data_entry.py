from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {
    "I" : "Income",
    "E" : "Expense"
}

def get_date(prompt, date_str=None, allow_default=False):
    while True:
        if date_str is None:
            date_str = input(prompt)
        
        if allow_default and not date_str:
            return datetime.today().strftime(date_format)
        
        try:
            valid_date = datetime.strptime(date_str, date_format)
            return valid_date.strftime(date_format)
        except ValueError:
            print("Invalid Date Format. Please Enter: dd-mm-yyyy Format")
            date_str = None  # Reset date_str to allow new input

def get_amount():
    while True:
        try:
            amount = float(input("Enter Amount: "))
            if amount <= 0:
                raise ValueError("Invalid Amount. Amount Must Be Positive")
            return amount
        except ValueError as e:
            print(e)
        

def get_category():
    while True:
        category = input("Enter Category ('I' For Income OR 'E' For Expense): ").upper()
        if category in CATEGORIES:
            return CATEGORIES[category]
        print("Invalid Category. Category Must Be 'I' For Income OR 'E' For Expense")

def get_description():
    return input("Enter Description: ")