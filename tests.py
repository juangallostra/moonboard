from genericpath import isfile
import unittest
from moonboard import MoonBoard, get_moonboard

# class BaseAPITestClass(unittest.TestCase):
#     """
#     BaseClass for testing
#     """

#     def setUp(self):
#         """
#         Set up method that will run before every test
#         """
#         pass

#     def tearDown(self):
#         """
#         Tear down method that will run after every test
#         """
#         pass


class MoonboardTests(unittest.TestCase):
    def test_get_valid_moonboard(self):
        """
        Test that a valid moon year returns a MoonBoard object
        """
        # Given
        year = [2016, 2017, 2019]  # Valid moon year layouts
        # When
        moonboards = [get_moonboard(y) for y in year]
        # Then
        self.assertTrue(all([isinstance(mb, MoonBoard) for mb in moonboards]))
        self.assertTrue(
            all([mb.get_year_layout() in year for mb in moonboards]))
        self.assertTrue(all([mb.get_cols() == 11 for mb in moonboards]))
        self.assertTrue(all([mb.get_rows() == 18 for mb in moonboards]))
        self.assertTrue(all([isfile(mb.get_image()) for mb in moonboards]))

    def test_get_invalid_moonboard(self):
        """
        Test that an invalid moon year raises an error
        """
        # Given
        year = 2015  # Invalid moon year layout
        # When
        with self.assertRaises(ValueError) as context:
            get_moonboard(year)
        # Then
        self.assertTrue(
            'Invalid year' in str(context.exception)
        )  # Test error message?
        self.assertRaises(ValueError, get_moonboard, year)


if __name__ == '__main__':
    unittest.main()
