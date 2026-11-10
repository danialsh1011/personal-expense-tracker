import unittest
from main import (
    calculate_total,
    filter_expenses_by_category
)

class TestCalculateTotal(unittest.TestCase):

    def test_calculate_total(self):
        expenses = [
            {"price": 100},
            {"price": 200},
            {"price": 50}
        ]

        result = calculate_total(expenses)

        self.assertEqual(result, 350)


    def test_single_expense(self):
        expenses = [
            {"price": 500}
        ]

        result = calculate_total(expenses)

        self.assertEqual(result, 500)


    def test_empty_expenses(self):
        expenses = []

        result =calculate_total(expenses)

        self.assertEqual(result, 0)


    def test_float_expenses(self):
        expenses = [
            {"price": 10.5},
            {"price": 20.5}
        ]

        result = calculate_total(expenses)

        self.assertEqual(result, 31)

    def test_with_zero_expenses(self):
        expenses = [
            {"price": 0},
            {"price": 100}
        ]

        result = calculate_total(expenses)

        self.assertEqual(result, 100)


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


if __name__ == "__main__":  
    unittest.main()
