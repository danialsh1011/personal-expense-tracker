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
        price = int(input("Price: "))
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
            total = 0
            for dic in expenses:
                total += dic['price']
            print(f"The total cost is: {total}\n")
        
    elif choice == 4:
        if not expenses:
            print("No expenses found.\n")
        
        else:
            categories = {}
            for dic in expenses:
                if dic['category'] in categories:
                    categories[dic['category']] += dic['price']
                
                else:
                    categories[dic['category']] = dic['price']
                    
            for key, value in categories.items():
                print(f"{key}: {value}")
            print()
        
    elif choice == 5:
        show_expenses()
        if expenses:
            delete = int(input("Choose the expense to delete: "))
            if 1 <= delete <= len(expenses):
                expenses.pop(delete - 1)
                print(f"Expense {delete} deleted successfully!\n")
            else:
                print("Invalid number.")
                
    elif choice == 6:
        print("Goodbye!")
        break
    
    else:
        print("Invalid option!")