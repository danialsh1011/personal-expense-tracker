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
        delete = int(input("Choose the expense to delete: "))
        if 1 <= delete <= len(expenses):
            expenses.pop(delete - 1)
            print(f"Expense {delete} deleted successfully!\n")
        else:
            print("Invalid number.")


expenses = []
menu = """===== Personal Expense Tracker =====
1. Add expense
2. Show expenses
3. Show total expenses
4. Show expenses by category
5. Delete expense
6. Exit"""
while True:
    print(menu)
    choice = int(input("Choose an option:"))

    if choice == 1:
        print("Add expense selected")
        category = (input("Category: "))
        description = (input("Description: "))
        
        while True:
            try:
                price = int(input("Price: "))
                if price > 0:
                    break
                print("Price must be positive. Try again.")
            except ValueError:
                print("Please enter a valid number.")
                
        dic = {"price": price,
               "category": category,
               "description": description
               }
        expenses.append(dic)
        
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
        print("Goodbye!")
        break
    
    else:
        print("Invalid option!")