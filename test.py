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


if __name__ == "__main__":
    unittest.main()
