import unittest
from main import calculate_total

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
        

if __name__ == "__main__":  
    unittest.main()
