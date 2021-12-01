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
    def test_equal_moonboards(self):
        """
        Test that two MoonBoard objects with the same parameters are equal
        """
        # Given
        year = 2017
        # When
        m1 = get_moonboard(year)
        m2 = get_moonboard(year)
        # Then
        self.assertEqual(m1, m2)

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


class GeneratorsTests(unittest.TestCase):
    def test_empy_generator(self):
        """
        Test that an empty generator raises a NotImplementedError when
        generate() is called
        """
        # Given
        from generators.base_generator import BaseGenerator
        # When

        class EmptyGen(BaseGenerator):
            pass
        gen = EmptyGen()
        # Then
        with self.assertRaises(NotImplementedError) as context:
            gen.generate()

    def test_ahoughton_generator(self):
        """
        Test that the Ahoughton generator returns a valid MoonBoard problem
        """
        # Given
        from generators.ahoughton import AhoughtonGenerator
        a_gen = AhoughtonGenerator()
        # When
        problem = a_gen.generate()
        # Then
        self.assertTrue('18' in problem[0])  # assert climb ends at top row
        # assert climb starts at bottom rows
        self.assertTrue(problem[-1][-1] in '6543') # This fails sometimes
        self.assertTrue(len(problem) > 2)  # assert there are more than 2 moves


if __name__ == '__main__':
    unittest.main()
