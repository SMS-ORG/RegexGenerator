import unittest
from regexgen import RegexGen
import re


class TestCases(unittest.TestCase):

    def test_phone_no(self):
        regex = RegexGen().digits(4, 4).text(RegexGen.characters("-")).digits(3,
                                                                              3).text(RegexGen.characters("-"), 1, 1).digits(3, 3)
        self.assertTrue(re.match(regex.get_regex_data(), "9741-012-977"))
        self.assertFalse(re.match(regex.get_regex_data(), "974-4012-977"))
        self.assertFalse(re.match(regex.get_regex_data(), "9741012-977"))

    def test_any_character(self):
        regex = RegexGen()
        regex = regex.any(min=0, max=12)
        self.assertTrue(re.match(regex.get_regex_data(), "a"))
        self.assertTrue(
            re.match(regex.get_regex_data(), "abcdef1234$"))
    
    def test_exclude(self):
        regex = RegexGen().digits(1, 10, RegexGen.exclude("23", True), capture=True)
        self.assertTrue(re.match(regex.get_regex_data(),'12345678912'))
        self.assertTrue(re.match(regex.get_regex_data(),"142356123"))
        self.assertFalse(re.match(regex.get_regex_data(),'231123123232'))
        
    def test_start_of_line(self):
        regex = RegexGen()
        regex = regex.linestartwith().digits(1,3)
        self.assertTrue(re.match(regex.get_regex_data(),"123xs"))
        self.assertTrue(re.match(regex.get_regex_data(),"1xg"))
        self.assertFalse(re.match(regex.get_regex_data(),"a426"))

    def test_end_of_line(self):
        regex = RegexGen()
        regex = regex.text('abc').endofline()
        self.assertTrue(re.search(regex.get_regex_data(),"zabc"))
        self.assertTrue(re.search(regex.get_regex_data(),"thisisabc"))
        self.assertFalse(re.search(regex.get_regex_data(),"abc12ab"))
        self.assertFalse(re.search(regex.get_regex_data(),'abc1a'))

    def test_any_of_functions(self):
        regex = RegexGen().text(RegexGen.anyof('+!@.'),min=1,max=4)
        self.assertTrue(re.match(regex.get_regex_data(),"@+abc"))
        self.assertTrue(re.search(regex.get_regex_data(),"This is a test."))
        self.assertFalse(re.match(regex.get_regex_data(),"Thisisatest"))

    def test_matches_single_whitespace(self):
        regex = RegexGen().text('foo').text(RegexGen().whitespace).text('bar')
        self.assertTrue(re.match(regex.get_regex_data(),'foo bar'))
        self.assertFalse(re.match(regex.get_regex_data(),' foo bar'))
        self.assertFalse(re.match(regex.get_regex_data(),'foo  bar'))

    def test_lowercase_letter(self):
        regex = RegexGen().text(RegexGen().lowercaserange)
        # print(regex.get_regex_data())
        self.assertTrue(re.match(regex.get_regex_data(),'abc'))
        self.assertFalse(re.match(regex.get_regex_data(),'123'))

    def test_ranges(self):
        self.assertTrue(RegexGen.range('a', 'z'))
        self.assertTrue(RegexGen.range('A', 'Z'))
        self.assertTrue(RegexGen.range('0', '9'))
        self.assertTrue(RegexGen.range('0', '2'))

        with self.assertRaises(Exception):
            RegexGen.range('1', '1')
            RegexGen.range('z', 'a')
            RegexGen.range('a', 'a')
            RegexGen.range('Z', 'A')
            RegexGen.range('0', 'Z')
            RegexGen.range('Z', '0')
            RegexGen.range('9', '0')

    def test_character(self):
        self.assertEqual(RegexGen.characters("abc"), "abc")
        self.assertEqual(RegexGen.characters("ab{"), "ab\{")
        self.assertEqual(RegexGen.characters("ab}"),"ab\}")



if __name__ == "__main__":
    unittest.main()
