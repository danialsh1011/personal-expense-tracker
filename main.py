import json
import math
from datetime import date, datetime

def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
        return expenses
    
    except json.decoder.JSONDecodeError:
        return []
    
    except FileNotFoundError:
        return []
    


def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)
        
 
def add_expense(expenses):
    category = (input("Category: ")).capitalize().strip()
    while not category:
        print("Invalid input!")
        category = (input("Category: ")).capitalize().strip()
        
    description = (input("Description: ")).strip()
    while not description:
        print("Invalid input!")
        description = (input("Description: ")).strip()
    while True:
        try:
            price = float(input("Price: "))
            if math.isfinite(price) and price > 0:
                break
            print("Price must be positive. Try again.")
        except ValueError:
            print("Please enter a valid number.")
        
    expense_date = get_expense_date()
                
    expense = {"price": price,
            "category": category,
            "description": description,
            "date": expense_date
            }
    expenses.append(expense)
    save_expenses(expenses)
 
 
def show_expenses(filtered_expenses):
    if not filtered_expenses:
        print("No expenses found.")
        
    else:    
        for index, expense in enumerate(filtered_expenses, start=1):
            print(f"Expense {index}")
            print("----------")
            print(f"Description: {expense['description']}")
            print(f"Category: {expense['category']}")
            print(f"Price: {expense['price']}")
            print(f"Date: {expense.get('date', 'Not recorded')}\n")
                

def calculate_total(expenses):
    total = 0
    for expense in expenses:
        total += expense['price']
    return total


def show_expenses_by_category(expenses):
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        category_totals[category] = category_totals.get(category, 0) + expense['price']
        
    return category_totals


def delete_expense(expenses):
    if not expenses:
        print("No expenses found.")
        return
    else:
        show_expenses(expenses)
        while True:
            try:
                delete = int(input("Choose the expense to delete: "))
                if 1 <= delete <= len(expenses):
                    break
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")
        expenses.pop(delete - 1)
        save_expenses(expenses)
        print(f"Expense {delete} deleted successfully!\n")


def edit_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return
    else:
        show_expenses(expenses)
        while True:
            try:
                choose_expense = int(input("Choose expense: "))
                if 1 <= choose_expense <= len(expenses):
                    break
                print("Invalid number (out of range)! Try again.")
            except ValueError:
                print("Please enter a valid number. Try again.")
                
        new_category = input("Category: ").capitalize().strip()
        while not new_category:
            print("Invalid input!")
            new_category = input("Category: ").capitalize().strip()

        new_description = input("Description: ").strip()
        while not new_description:
            print("Invalid input!")
            new_description = input("Description: ").strip()

        while True:
            try:
                new_price = float(input("Price: "))
                if math.isfinite(new_price) and new_price > 0:
                    break
                print("Price must be positive. Try again.")
            except ValueError:
                print("Please enter a valid number.")
            
        expense = expenses[choose_expense - 1]

        expense['price'] = new_price
        expense['category'] = new_category
        expense['description'] = new_description
        
        current_date = expense.get('date')
        new_date = get_expense_date(current_date)
        expense['date'] = new_date

        save_expenses(expenses)
        print("Expense edited successfully!\n")
        

def filter_expenses_by_category(category, expenses):
    filter_category = [expense for expense in expenses if expense['category'] == category]
    return filter_category


def get_expense_date(current_date=None):
    if current_date is None:
        current_date = date.today()
        current_date = current_date.strftime("%Y-%m-%d")

    while True:
        input_date = input(f"Date (press Enter for {current_date}): ").strip()

        if input_date == "":
            return current_date

        try:
            datetime.strptime(input_date, "%Y-%m-%d")
            return input_date

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")


def main():
    expenses = load_expenses()

    menu = """===== Personal Expense Tracker =====
1. Add expense
2. Show expenses
3. Show total expenses
4. Show expenses by category
5. Filter expenses by category
6. Delete expense
7. Edit expense
8. Exit"""

    while True:
        print(menu)
        try:
            choice = int(input("Choose an option:"))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if choice == 1:
            add_expense(expenses)
            print("Expense added successfully!\n")

        elif choice == 2:
            show_expenses(expenses)

        elif choice == 3:
            if not expenses:
                print("No expenses found.\n")

            else:
                print(f"The total cost is: {calculate_total(expenses)}\n")

        elif choice == 4:
            if not expenses:
                print("No expenses found.\n")

            else:
                categories = show_expenses_by_category(expenses)         
                for key, value in categories.items():
                    print(f"{key}: {value}")
                print()

        elif choice == 5:
            if not expenses:
                print("No expenses found.\n")
            else:
                choose_category = input("Choose your category: ").capitalize().strip()
                filtered_expenses = filter_expenses_by_category(choose_category, expenses)
                show_expenses(filtered_expenses)

        elif choice == 6:
            delete_expense(expenses)

        elif choice == 7:
            edit_expenses(expenses)

        elif choice == 8:
            print("Goodbye!")
            break
        
        else:
            print("Invalid option!")
            
            
if __name__ == "__main__":
    main()