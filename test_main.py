import unittest
from unittest.mock import patch, mock_open
from main import (
    calculate_total,
    filter_expenses_by_category,
    load_expenses,
    save_expenses
)


class TestCalculateTotal(unittest.TestCase):

    def test_calculate_total(self):
        expenses = [
            {"price": 100},
            {"price": 200},
            {"price": 50}
        ]

        result = calculate_total(expenses)
        expected = 350

        self.assertEqual(result, expected)


    def test_single_expense(self):
        expenses = [
            {"price": 500}
        ]

        result = calculate_total(expenses)
        expected = 500

        self.assertEqual(result, expected)


    def test_empty_expenses(self):
        expenses = []

        result =calculate_total(expenses)
        expected = 0

        self.assertEqual(result, expected)


    def test_float_expenses(self):
        expenses = [
            {"price": 10.5},
            {"price": 20.5}
        ]

        result = calculate_total(expenses)
        expected = 31

        self.assertEqual(result, expected)


    def test_with_zero_expenses(self):
        expenses = [
            {"price": 0},
            {"price": 100}
        ]

        result = calculate_total(expenses)
        expected = 100

        self.assertEqual(result, expected)


class TestFilterExpensesByCategory(unittest.TestCase):
    
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

        self.assertEqual(result, expected)


    def test_expenses_empty(self):
        expenses = []
        
        result = filter_expenses_by_category("", expenses)
        expected = []
        
        self.assertEqual(result, expected)

    
    def test_invalid_category(self):
        expenses = [
            {'category': "food"},
            {'category': "food"},
            {'category': "test"},
            {'category': "education"}
        ]
        
        result = filter_expenses_by_category("book", expenses)
        expected = []
        
        self.assertEqual(result, expected)
        
        
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
        
        self.assertEqual(result, expected)


    def test_one_category(self):
        expenses = [
            {'category': "food"},
            {'category': "test"},
            {'category': "education"}
        ]

        result = filter_expenses_by_category("food", expenses)
        expected = [{'category': "food"}]

        self.assertEqual(result, expected)


class TestLoadExpenses(unittest.TestCase):
    def test_file_not_found(self):
        with patch("main.open", side_effect= FileNotFoundError):
            result = load_expenses()
        expected = []
        
        self.assertEqual(result, expected)

    
    def test_load_valid_json(self):
        mock_file = mock_open(read_data='[{"price": 1, "category": "test", "description": "test"}]')
        
        with patch("main.open", new=mock_file):
            result = load_expenses()
            
        expected = [{'price': 1, 'category': "test", 'description': "test"}]
        
        self.assertEqual(result, expected)
        
        
    def test_invalid_json(self):
        mock_file = mock_open(read_data='{"price": 100')

        with patch("main.open", new=mock_file):
            result = load_expenses()

        expected = []

        self.assertEqual(result, expected)


class TestSaveExpenses(unittest.TestCase):
    
    def test_save_expenses(self):
        mock_file = mock_open()
        expenses = [{"price": 1, "category": "test", "description": "test"}]
        
        with patch("main.open", new=mock_file):
            save_expenses(expenses)
            
        mock_file.assert_called_once_with("expenses.json", "w")

    
    def test_json_dump_called(self):
        mock_file = mock_open()
        expenses = [{"price": 1, "category": "test", "description": "test"}]
    
        with patch("main.open", new=mock_file):
            with patch("main.json.dump") as mock_dump:
                save_expenses(expenses)
    
        mock_dump.assert_called_once_with(expenses, mock_file(), indent=4)
        
        
    def test_save_empty_expenses(self):
        mock_file = mock_open()
        expenses = []
    
        with patch("main.open", new=mock_file):
            with patch("main.json.dump") as mock_dump:
                save_expenses(expenses)
    
        mock_dump.assert_called_once_with(expenses, mock_file(), indent=4)
        

if __name__ == "__main__":  
    unittest.main()
