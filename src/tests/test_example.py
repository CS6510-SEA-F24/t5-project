import unittest
from src.main.t5_grp import example_function


class TestExampleFunction(unittest.TestCase):
    def test_example_function(self):
        # Call the function
        result = example_function()

        # Check if the result is as expected
        self.assertEqual(result, "Hello, World!")


if __name__ == '__main__':
    unittest.main()
