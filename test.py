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


if __name__ == "__main__":
    unittest.main()
