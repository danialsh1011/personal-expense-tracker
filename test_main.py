import unittest
from unittest.mock import patch, mock_open
from main import (
    calculate_total,
    filter_expenses_by_category,
    load_expenses,
    save_expenses,
    delete_expense,
    edit_expenses
)


class TestCalculateTotal:
    def test_calculate_total(self):
        expenses = [
            {"price": 100},
            {"price": 200},
            {"price": 50}
        ]
        result = calculate_total(expenses)
        expected = 350
        assert result == expected


    def test_single_expense(self):
        expenses = [
            {"price": 500}
        ]
        result = calculate_total(expenses)
        expected = 500

        assert result == expected


    def test_empty_expenses(self):
        expenses = []
        result = calculate_total(expenses)
        expected = 0

        assert result == expected


    def test_float_expenses(self):
        expenses = [
            {"price": 10.5},
            {"price": 20.5}
        ]
        result = calculate_total(expenses)
        expected = 31

        assert result == expected


    def test_with_zero_expenses(self):
        expenses = [
            {"price": 0},
            {"price": 100}
        ]
        result = calculate_total(expenses)
        expected = 100

        assert result == expected


class TestFilterExpensesByCategory:
    def test_filter_food_expenses(self):
        expenses = [
            {'category': "food"},
            {'category': "food"},
            {'category': "test"},
            {'category': "education"}
        ]

        result = filter_expenses_by_category("food", expenses)
        expected = [
            {'category': "food"},
            {'category': "food"}
        ]

        assert result == expected


    def test_expenses_empty(self):
        expenses = []

        result = filter_expenses_by_category("", expenses)
        expected = []

        assert result == expected


    def test_invalid_category(self):
        expenses = [
            {'category': "food"},
            {'category': "food"},
            {'category': "test"},
            {'category': "education"}
        ]

        result = filter_expenses_by_category("book", expenses)
        expected = []

        assert result == expected


    def test_all_expenses_same_category(self):
        expenses = [
            {'category': "food"},
            {'category': "food"},
            {'category': "food"},
            {'category': "food"}
        ]

        result = filter_expenses_by_category("food", expenses)
        expected = [
            {'category': "food"},
            {'category': "food"},
            {'category': "food"},
            {'category': "food"}
        ]

        assert result == expected


    def test_one_category(self):
        expenses = [
            {'category': "food"},
            {'category': "test"},
            {'category': "education"}
        ]

        result = filter_expenses_by_category("food", expenses)
        expected = [{'category': "food"}]

        assert result == expected


class TestLoadExpenses:
    def test_file_not_found(self):
        with patch("main.open", side_effect= FileNotFoundError):
            result = load_expenses()
        expected = []
        
        assert result == expected

    
    def test_load_valid_json(self):
        mock_file = mock_open(read_data='[{"price": 1, "category": "test", "description": "test"}]')
        
        with patch("main.open", new=mock_file):
            result = load_expenses()
            
        expected = [{'price': 1, 'category': "test", 'description': "test"}]
        
        assert result == expected
        
        
    def test_invalid_json(self):
        mock_file = mock_open(read_data='{"price": 100')

        with patch("main.open", new=mock_file):
            result = load_expenses()

        expected = []

        assert result == expected
        
        
    def test_json_object_instead_of_list(self):
        mock_file = mock_open(read_data='{"price": 100}')

        with patch("main.open", new=mock_file):
            result = load_expenses()
            
        excepted = []

        assert result == excepted


class TestSaveExpenses:
    
    def test_save_expenses(self):
        mock_file = mock_open()
        expenses = [{"price": 1, "category": "test", "description": "test"}]
        
        with patch("main.open", new=mock_file):
            save_expenses(expenses)
            
        mock_file.assert_called_once_with("expenses.json", "w", encoding="utf-8")

    
    def test_json_dump_called(self):
        mock_file = mock_open()
        expenses = [{"price": 1, "category": "test", "description": "test"}]
    
        with patch("main.open", new=mock_file):
            with patch("main.json.dump") as mock_dump:
                save_expenses(expenses)
    
        mock_dump.assert_called_once_with(expenses, mock_file(), indent=4, ensure_ascii=False)
        
        
    def test_save_empty_expenses(self):
        mock_file = mock_open()
        expenses = []
    
        with patch("main.open", new=mock_file):
            with patch("main.json.dump") as mock_dump:
                save_expenses(expenses)
    
        mock_dump.assert_called_once_with(expenses, mock_file(), indent=4, ensure_ascii=False)
        
        
class TestDeleteExpense:
    
    def test_delete_empty_expense(self):
        expenses = []
        
        with patch("builtins.print") as mock_print:
            with patch("builtins.input") as mock_input:
                delete_expense(expenses)
        
        mock_print.assert_called_once_with("No expenses found.")
        mock_input.assert_not_called()
        
        
    def test_delete_expense(self):
        expenses = [
            {"price": 100, "category": "food", "description": "lunch"},
            {"price": 200, "category": "taxi", "description": "university"},
            {"price": 300, "category": "books", "description": "python"}
        ]
        
        expected = [
            {"price": 100, "category": "food", "description": "lunch"},
            {"price": 300, "category": "books", "description": "python"}
        ]
        
        with patch("builtins.input", side_effect=['2', 'y']):
            with patch("main.save_expenses") as mock_save:
                with patch("builtins.print") as mock_print:
                    delete_expense(expenses)
            
            
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense 2 deleted successfully!\n")
        assert expenses == expected
        
        
    def test_delete_invalid_number(self):
        expenses = [
            {"price": 100, "category": "food", "description": "lunch"},
            {"price": 200, "category": "taxi", "description": "university"},
            {"price": 300, "category": "books", "description": "python"}
        ]
 
        expected = [
            {"price": 100, "category": "food", "description": "lunch"},
            {"price": 300, "category": "books", "description": "python"}
        ]
               
        with patch("builtins.input", side_effect=['5', '2', 'y']):
            with patch("main.save_expenses") as mock_save:
                with patch("builtins.print") as mock_print:
                    delete_expense(expenses)
                
        mock_print.assert_any_call("Invalid number.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense 2 deleted successfully!\n")
        assert expenses == expected       
        
        
    def test_delete_invalid_input(self):
        expenses = [
            {"price": 100, "category": "food", "description": "lunch"},
            {"price": 200, "category": "taxi", "description": "university"},
            {"price": 300, "category": "books", "description": "python"}
        ]
        

        expected = [
            {"price": 100, "category": "food", "description": "lunch"},
            {"price": 300, "category": "books", "description": "python"}
        ]
                
        with patch("builtins.input", side_effect=['a', '2', 'y']):
            with patch("main.save_expenses") as mock_save:
                with patch("builtins.print") as mock_print:
                    delete_expense(expenses)
                
        mock_print.assert_any_call("Please enter a valid number.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense 2 deleted successfully!\n")
        assert expenses == expected
        
        
class TestEditExpense(unittest.TestCase):
    
    def test_edit_empty_expenses(self):
        expenses = []
        
        with patch("builtins.print") as mock_print:
            with patch("builtins.input") as mock_input:
                edit_expenses(expenses)
        
        mock_print.assert_called_once_with("No expenses found.")
        mock_input.assert_not_called()
        
        
    def test_edit_expenses(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
        
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "python course", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
        
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_invalid_number_input(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
        
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["2" ,"1", "book", "python course", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
        
        mock_print.assert_any_call("Invalid number (out of range)! Try again.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_invalid_string_input(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
        
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["a" ,"1", "book", "python course", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
        
        mock_print.assert_any_call("Please enter a valid number. Try again.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_empty_input_category(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
        
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "", "book", "python course", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
        
        mock_print.assert_any_call("Invalid input!")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
    def test_edit_empty_input_description(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
        
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "", "python course", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
        
        mock_print.assert_any_call("Invalid input!")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_invalid_price_input(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
    
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "python course", "a", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
                        
        mock_print.assert_any_call("Please enter a valid number.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
    
    
    def test_edit_non_positive_price(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
    
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "python course", "-100", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
                        
        mock_print.assert_any_call("Price must be positive. Try again.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_zero_price(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
    
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "python course", "0", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
                        
        mock_print.assert_any_call("Price must be positive. Try again.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_infinite_price(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
    
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "python course", "inf", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
                        
        mock_print.assert_any_call("Price must be positive. Try again.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_nan_price(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch"} ]
    
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "python course", "nan", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16"):
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
                        
        mock_print.assert_any_call("Price must be positive. Try again.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_date(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch", "date": "2026-11-15"} ]
        
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "python course", "250.0"]):
            with patch("main.get_expense_date", return_value="2026-11-16") as mock_date:
                with patch("main.save_expenses") as mock_save:
                    with patch("builtins.print") as mock_print:
                        edit_expenses(expenses)
                        
        mock_date.assert_called_once_with("2026-11-15")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        
        
    def test_edit_invalid_date(self):
        expenses = [ {"price": 100, "category": "food", "description": "lunch", "date": "2026-11-15"} ]
        
        expected = [ {"price": 250, "category": "Book", "description": "Python course", "date": "2026-11-16"}]
        
        with patch("builtins.input", side_effect=["1", "book", "python course", "250.0", "a", "2026-11-16"]):
            with patch("main.save_expenses") as mock_save:
                with patch("builtins.print") as mock_print:
                    edit_expenses(expenses)
                        
        mock_print.assert_any_call("Invalid date. Please use YYYY-MM-DD.")
        mock_save.assert_called_once_with(expenses)
        mock_print.assert_any_call("Expense edited successfully!\n")
        self.assertEqual(expenses, expected)
        

if __name__ == "__main__":  
    unittest.main()
