import json
import math

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
        
 
def show_expenses():
    if not expenses:
        print("No expenses found.")
        
    else:    
        for i in range(len(expenses)):
            print(f"Expense {i + 1}")
            print("----------")
            print(f"Description: {expenses[i]['description']}")
            print(f"Category: {expenses[i]['category']}")
            print(f"Price: {expenses[i]['price']}\n")
                

def calculate_total():
    total = 0
    for dic in expenses:
        total += dic['price']
    return total


def show_expenses_by_category():
    category_totals = {}
    for dic in expenses:
        if dic['category'] in category_totals:
            category_totals[dic['category']] += dic['price']
                            
        else:
            category_totals[dic['category']] = dic['price']
    
    return category_totals


def delete_expense():
    if not expenses:
        print("No expenses found.")
        return
    else:
        show_expenses()
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


def edit_expenses():
    if not expenses:
        print("No expenses found.")
        return
    else:
        show_expenses()
        while True:
            try:
                choose_expense = int(input("Choose expense: "))
                if 1 <= choose_expense <= len(expenses):
                    break
                print("Invalid number (out of range)! Try again.")
            except ValueError:
                print("Please enter a valid number. Try again.")
                
        new_category = input("Category: ").strip()
        while not new_category:
            print("Invalid input!")
            new_category = input("Category: ").strip()

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

        save_expenses(expenses)
        print("Expense edited successfully!\n")
        
        
expenses = load_expenses()

menu = """===== Personal Expense Tracker =====
1. Add expense
2. Show expenses
3. Show total expenses
4. Show expenses by category
5. Delete expense
6. Edit expense
7. Exit"""

while True:
    print(menu)
    try:
        choice = int(input("Choose an option:"))
    except ValueError:
        print("Please enter a valid number.")
        continue
    
    if choice == 1:
        category = (input("Category: ")).strip()
        while not category:
            print("Invalid input!")
            category = (input("Category: ")).strip()
        
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
                
        dic = {"price": price,
               "category": category,
               "description": description
               }
        expenses.append(dic)
        save_expenses(expenses)
        
        print("Expense added successfully!\n")
    
    elif choice == 2:
        show_expenses()
        
    elif choice == 3:
        if not expenses:
            print("No expenses found.\n")
        
        else:
            print(f"The total cost is: {calculate_total()}\n")
        
    elif choice == 4:
        if not expenses:
            print("No expenses found.\n")
        
        else:
            categories = show_expenses_by_category()         
            for key, value in categories.items():
                print(f"{key}: {value}")
            print()
        
    elif choice == 5:
        delete_expense()

    elif choice == 6:
        edit_expenses()
                        
    elif choice == 7:
        print("Goodbye!")
        break
    
    else:
        print("Invalid option!")