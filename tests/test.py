import unittest
import re
from src.regexgen import RegexGen


class TestCases(unittest.TestCase):

    def test_phone_no(self):
        regex = RegexGen().digits(4, 4).text(RegexGen.characters("-"), 1, 1).digits(3,
                                                                                    3).text(RegexGen.characters("-"), 1, 1).digits(3, 3)
        self.assertEqual(regex.get_regex_data(), "\d{4}-\d{3}-\d{3}")
        self.assertTrue(re.match(regex.get_regex_data(), "9741-012-977"))
        self.assertFalse(re.match(regex.get_regex_data(), "974-4012-977"))
        self.assertFalse(re.match(regex.get_regex_data(), "9741012-977"))

    def test_any_character(self):
        regex = RegexGen()
        regex = regex.any(min=0, max=12)
        self.assertEqual(regex.get_regex_data(), ".{,12}")
        self.assertTrue(re.match(regex.get_regex_data(), "a"))
        self.assertTrue(re.match(regex.get_regex_data(), "abcdef1234$"))

    def test_exclude(self):
        regex = RegexGen().digits(1, 10, RegexGen.exclude("23", True), capture=True)
        self.assertEqual(regex.get_regex_data(), "((?!23)\d){1,10}")
        self.assertTrue(re.match(regex.get_regex_data(), '19845671'))
        self.assertTrue(re.match(regex.get_regex_data(), "142356142"))
        self.assertFalse(re.match(regex.get_regex_data(), '231123'))

    def test_start_of_line(self):
        regex = RegexGen()
        regex = regex.linestartwith().digits(1, 3)
        self.assertEqual(regex.get_regex_data(), "^\d{1,3}")
        self.assertTrue(re.match(regex.get_regex_data(), "123xs"))
        self.assertTrue(re.match(regex.get_regex_data(), "1xg"))
        self.assertFalse(re.match(regex.get_regex_data(), "a426"))

    def test_end_of_line(self):
        regex = RegexGen()
        regex = regex.text('abc', 1, 1).endofline()
        self.assertEqual(regex.get_regex_data(), "abc$")
        self.assertTrue(re.search(regex.get_regex_data(), "zabc"))
        self.assertTrue(re.search(regex.get_regex_data(), "thisisabc"))
        self.assertFalse(re.search(regex.get_regex_data(), "abc12ab"))
        self.assertFalse(re.search(regex.get_regex_data(), 'abc1a'))

    def test_any_of_functions(self):
        regex = RegexGen().text(RegexGen.any_of(RegexGen.characters('+!@.')), min=1, max=4)
        self.assertEqual(regex.get_regex_data(), "(?:[\+!@\.]){1,4}")
        self.assertTrue(re.match(regex.get_regex_data(), "@+abc"))
        self.assertTrue(re.search(regex.get_regex_data(), "This is a test."))
        self.assertFalse(re.match(regex.get_regex_data(), "Thisisatest"))

    def test_matches_single_whitespace(self):
        regex = RegexGen().text('foo', 1, 1).text(
            RegexGen.whitespace, 1, 1).text('bar', 1, 1)
        self.assertEqual(regex.get_regex_data(), "foo\sbar")
        self.assertTrue(re.match(regex.get_regex_data(), 'foo bar'))
        self.assertFalse(re.match(regex.get_regex_data(), ' foo bar'))
        self.assertFalse(re.match(regex.get_regex_data(), 'foo  bar'))

    def test_lowercase_letter(self):
        regex = RegexGen().text(RegexGen().lowercaserange, 1, 1)
        self.assertEqual(regex.get_regex_data(), "[a-z]")
        self.assertTrue(re.match(regex.get_regex_data(), "a"))
        self.assertTrue(re.match(regex.get_regex_data(), "abc"))
        self.assertFalse(re.match(regex.get_regex_data(), "123"))

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
        self.assertEqual(RegexGen.characters("ab}"), "ab\}")

    def test_combine(self):
        regexa = RegexGen().digits(4, 4).text(RegexGen.characters('-'), 1, 1)
        regexb = RegexGen().digits(3, 3)
        regex = RegexGen.combine(regexa, regexb)
        self.assertEqual(regex.get_regex_data(), "\d{4}-\d{3}")
        self.assertTrue(re.match(regex.get_regex_data(), "9741-012"))
        self.assertFalse(re.match(regex.get_regex_data(), "9741"))
        self.assertFalse(re.match(regex.get_regex_data(), "9741-01"))

    def test_start_and_end(self):
        regex = RegexGen().linestartwith().text(
            'foo', 1, 1).any(1, 5).text('bar', 1, 1).endofline()
        self.assertEqual(regex.get_regex_data(), "^foo.{1,5}bar$")
        self.assertTrue(re.match(regex.get_regex_data(), "foo12345bar"))
        self.assertFalse(re.match(regex.get_regex_data(), "aafoo1234bar"))
        self.assertFalse(re.match(regex.get_regex_data(), "foo12345bar123"))
        self.assertFalse(re.match(regex.get_regex_data(), "foo123458bar123"))

    def test_succeeded_by(self):
        regex = RegexGen().succeeded_by("USD",RegexGen.whitespace + RegexGen.digitsrange,min=1,max=1)
        self.assertEqual(regex.get_regex_data(), "(?:USD(?=\s\d))")
        self.assertTrue(re.match(regex.get_regex_data(), "USD 123"))
        self.assertFalse(re.match(regex.get_regex_data(), "USD Aba"))
    
    def test_preceded_by(self):
        regex = RegexGen().preceded_by("USD",RegexGen.digitsrange,min=1,max=1)
        self.assertEqual(regex.get_regex_data(), "(?:(?<=USD)\d)")
        self.assertTrue(re.search(regex.get_regex_data(), "USD1"))
        self.assertFalse(re.search(regex.get_regex_data(), "Rs1"))
    def test_alphabets(self):
        regex = RegexGen().alphabets(1, 5)
        self.assertEqual(regex.get_regex_data(), "[a-zA-Z]{1,5}")
        self.assertTrue(re.match(regex.get_regex_data(), "hello"))
        self.assertTrue(re.match(regex.get_regex_data(), "HELLO"))
        self.assertFalse(re.match(regex.get_regex_data(), "1923"))

    def test_alphanumerc(self):
        regex = RegexGen().text(RegexGen.alphanumeric, 4, 4)
        self.assertEqual(regex.get_regex_data(), "\w{4}")
        self.assertTrue(re.match(regex.get_regex_data(), "acrs"))
        self.assertTrue(re.match(regex.get_regex_data(), "1a3_"))
        self.assertFalse(re.match(regex.get_regex_data(), '@a+*'))

    def test_email(self):
        regex = RegexGen().linestartwith().text(RegexGen.alphanumeric,oneormore = True).text(RegexGen.characters("@"),1,1).text(RegexGen.alphanumeric,oneormore = True).text(RegexGen.characters("."),1,1).alphabets(2,).endofline()
        self.assertTrue(re.match(regex.get_regex_data(),"aaa@gmail.com"))
        self.assertTrue(re.match(regex.get_regex_data(),'test@test.com'))
        self.assertFalse(re.match(regex.get_regex_data(),'test@test.c'))
        self.assertFalse(re.match(regex.get_regex_data(),'test.com'))
    
    def test_password(self):
        anyvalue = RegexGen.any_of([{"character": '.', "min": 0, "max": 0, "zeroormore": True}])
        regex = RegexGen().linestartwith().succeeded_by("",anyvalue+RegexGen.any_of(RegexGen.range("a", "z")), min=1, max=1).succeeded_by("",anyvalue+RegexGen.any_of(RegexGen.range("A", "Z")), min=1, max=1).succeeded_by("",                                                                         anyvalue+RegexGen.digitsrange, min=1, max=1).text(RegexGen.alphanumeric, min=8).endofline()
        self.assertTrue(re.match(regex.get_regex_data(),"Password123"))
        self.assertFalse(re.match(regex.get_regex_data(),'password'))
        self.assertFalse(re.match(regex.get_regex_data(),'PASSword'))
        self.assertFalse(re.match(regex.get_regex_data(),'pass123'))

if __name__ == "__main__":
    unittest.main()
