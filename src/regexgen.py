from typing_extensions import Self
from typing import Tuple
import re
from multipledispatch import dispatch

def is_lower_case(x: int): return x > 96 and x < 123
def is_upper_case(x: int): return x > 64 and x < 91
def is_number(x: int): return x > 47 and x < 58

"""
    data: str //any character or range
    args: list //list of functions for testing ranges, is_lower_case, is_upper_case, is_number
"""


def valid_ranges(data: str, *args) -> bool:
    capture = "(.(?=-)-(?<=-).)"
    contains_ranges = False

    data = re.finditer(capture, data)

    for ran_ge in data:
        contains_ranges = True
        range_start = ran_ge.group()[0]
        range_end = ran_ge.group()[2]

        ascii_range_start = ord(range_start)  # ascii value of character
        ascii_range_end = ord(range_end)  # ascii value of character

        is_invalid = True

        for func in args:
            if func(ascii_range_start) and func(ascii_range_end) and ascii_range_start < ascii_range_end:
                is_invalid = False
                break

        if is_invalid:
            raise Exception("In function {}, range_start : {}, range_end:{} => \nAccepted Types \n"
                            "\tlowercaseletter-lowercaseletter\n"
                            "\tuppercaseletter-uppercaseletter\n"
                            "\tdigit-digit\n"
                            .format(
                                valid_ranges.__name__, range_start, range_end))

    # if contains_ranges:  # check for redundancy to aware programmer and need to implement later
    #     pass

    return contains_ranges


class RegexGen:
    """
    Start of the class
    """
    # ranges
    lowercaserange: str = "[a-z]"
    uppercaserange: str = "[A-Z]"
    digitsrange: str = "\d"
    symbolsrange: str = "\W"
    alphanumeric: str = "\w"
    # ecape sequences
    block_word: str = "\b"
    nonblock_word: str = "\B"
    new_line: str = "\n"
    tab_space: str = "\t"
    carriage_return: str = "\r"
    whitespace = "\s"

    def __init__(self):
        self.__regex_data: str = str()

    '''
    ^ character symbolizes the start of the string or line
    '''

    def linestartwith(self):
        if not len(self.__regex_data):
            self.__regex_data += '^'
        else:
            self.__regex_data += '\s^'
        return self

    '''
    $ character symbolizes as end of a line
    '''

    def endofline(self):
        self.__regex_data += '$'
        return self


    @staticmethod
    def range(start: str, end: str) -> str:
        if (not start and not end) and (len(start) > 1 and len(end) > 1):
            raise Exception("In function {}, range_start : {}, range_end:{} => Characters cannot be None".format(
                RegexGen.range.__name__, start, end))

        # check if range is valid
        character_range = f"{start}-{end}"
        if (valid_ranges(character_range, is_lower_case, is_upper_case, is_number)):
            return character_range
        raise Exception("In function {}, range_start : {}, range_end:{} => This is not a valid range. Valid ranges are 0-9,A-Z or a-z or \W".format(
            RegexGen.range.__name__, start, end))

    '''
        characters : str  //characters to be matched
        pattern_prevent : bool  => default = False //On True, prevents the characters sequence to match(The sequence must not contain a range) 
                                                //and on false prevent piecewise occuring of characters.
        return : tuple
    '''
    @staticmethod
    def exclude(characters: str, pattern_prevent: bool = False) -> Tuple[str, bool]:
        if not characters:
            raise Exception("In function {}, Character : {} => Characters cannot be None".format(
                RegexGen.exclude.__name__, characters))
        # check if charaters is a range
        try:
            if valid_ranges(characters, is_lower_case, is_upper_case, is_number) or characters.find(RegexGen.symbolsrange) != -1:
                pattern_prevent = False
        except (...):
            raise

        return characters, pattern_prevent

    '''
        character: str,
        start : bool, => default = True //On true, the letter is the left boundary of the word 
                                        //and on false the letter is the right boundary of the word
    '''
    @staticmethod
    def boundary_character(character: str, start: bool = True) -> str:
        if len(character) > 2:
            raise Exception("In function {}, start : {} => Character cannot be length greater than two",
                            RegexGen.boundary_character.__name__, start)
        elif len(character) == 2 and character not in {"\w", "\W", "\d", "\."}:
            raise Exception("In function {}, start : {} => Character is not a \w or \W or \d or \.",
                            RegexGen.boundary_character.__name__, start)

        character_str = "\b" + character if start else character + "\b"
        return character_str

    '''
        Add Quantifiers like {0},{0,1},?,*,+,{0,1}
    '''
    @classmethod
    def __add_quantifier(cls, min: int, max: int, **kwargs) -> str:
        regexchar: str = str()

        if min == max and max == 0:
            zeroormore = kwargs.get("zeroormore", False)
            oneormore = kwargs.get("oneormore", False)
            if zeroormore:
                regexchar += '*'
            elif oneormore:
                regexchar += '+'
            else:
                raise Exception("In function {} => Min And Max Cannot be Zero"
                                .format(cls.__add_quantifier.__name__))
        elif max == min and min == 1:
            regexchar = ""
        elif max == min:
            regexchar = f"{{{min}}}"
        elif min == 0 and max == 1:
            regexchar = "?"
        elif max == 0 and min > 0:
            regexchar = f"{{{min},}}"
        elif max > min and min > 0:
            regexchar = f"{{{min},{max}}}"
        else:
            regexchar = f"{{,{max}}}"

        return regexchar

    ''' 
        character : str // A character can be a word, alphabet, a digit or number and symbols or a range
        min : int => default = 0  // if min and max are both zero it must pass a keyword argument as True 
        max : int  => default = 0
        capture : bool => default = False //On True enclose the character in parenthesis so that regex engine capture data
        kwargs : dict => {
            zeroormore : bool => default=False,
            oneormore : bool => default=False
        }
        return : RegexGen
    '''

    def text(self, character: str, min: int = 0, max: int = 0, **kwargs) -> Self:
        letterstr: str = str()
        temp: str = str()

        if not character:
            raise Exception("In function {}, Character : {} => Character cannot be None".format(
                self.text.__name__, character))

        letterstr = character

        try:
            temp = self.__add_quantifier(min, max, **kwargs)
        except Exception as e:
            raise

        self.__regex_data += letterstr
        self.__regex_data += temp

        return self

    ''' 
        . character symbolizes any character
        min : int => default = 0 // if min and max are both zero it must pass a keyword argument as True 
        max : int => default = 0
        capture : bool => default=False //On True enclose . in parenthesis so that regex engine capture data
        kwargs : dict => {
            zeroormore : bool => default=False,
            oneormore : bool => default=False
        }
        return : RegexGen
    '''

    def any(self, min: int = 0, max: int = 0, capture: bool = False, **kwargs) -> Self:
        anystr: str = str()
        temp: str = str()

        try:
            temp = self.__add_quantifier(min, max, **kwargs)
        except (...):
            raise

        anystr = f"(.{temp})" if capture else f".{temp}"
        self.__regex_data += anystr

        return self
    '''
        This function is used to match only numbers that may not contain a sequence of number or the each numbers existing independently.
        min : int => default = 0 // if min and max are both zero it must pass a keyword argument as True 
        max : int => default = 0
        pattern : a tuple[str, bool] expected a return type from exclude static function
        capture : bool => default=False //On True enclose the regex syntax in parenthesis so that regex engine capture data
        kwargs : dict => {
            zeroormore : bool => default=False,
            oneormore : bool => default=False
        }
        return : RegexGen
    '''

    def digits(self, min: int = 0, max: int = 0, pattern: Tuple[str, bool] = None, capture: bool = False, **kwargs) -> Self:
        digitstr: str = str()
        temp: str = str()

        try:
            temp = self.__add_quantifier(min, max, **kwargs)
        except (...):
            raise

        if pattern is None:
            digitstr = f"(\d{temp})" if capture else f"\d{temp}"
        elif pattern[1]:
            digitstr = f"((?!{pattern[0]})\d){temp}" if capture else f"(?:(?!{pattern[0]})\d){temp}"
        else:
            digitstr = f"((?![{pattern[0]}])\d){temp}" if capture else f"(?:(?![{pattern[0]}])\d){temp}"

        self.__regex_data += digitstr

        return self
    '''
        This function is used to match only words(not numbers) that may not contain a sequence of letters or the each letters existing independently.
        min : int => default = 0 // if min and max are both zero it must pass a keyword argument as True 
        max : int => default = 0
        pattern : a tuple[str, bool] expected a return type from exclude static function
        capture : bool => default=False //On True enclose the regex syntax in parenthesis so that regex engine capture data
        kwargs : dict => {
            zeroormore : bool => default=False,
            oneormore : bool => default=False
        }
        return : RegexGen
    '''

    def alphabets(self, min: int = 0, max: int = 0, pattern: Tuple[str, bool] = None, capture: bool = False, **kwargs) -> Self:
        characterstr: str = str()
        temp: str = str()

        try:
            temp = self.__add_quantifier(min, max, **kwargs)
        except (...):
            raise

        if pattern is None:
            characterstr = f"([a-zA-Z]{temp})" if capture else f"[a-zA-Z]{temp}"
        elif pattern[1]:
            characterstr = f"((?!{pattern[0]})a-zA-Z){temp}" if capture else f"(?:(?!{pattern[0]})a-zA-Z){temp}"
        else:
            characterstr = f"((?![{pattern[0]}])a-zA-Z){temp}\b" if capture else f"(?:(?![{pattern[0]}])a-zA-Z){temp}"

        self.__regex_data += characterstr

        return self

    '''
        If the program have capture parameters it will prevent regex engine from capturing index and patterns from the string 
        reducing capturing overhead and hence increase efficiency
        return : str 
    '''

    def get_non_capturing_regex(self) -> str:
        return f"(?:{self.__regex_data})"

    '''
        Returns a regex syntax that may capture the text from the input string. 
        return : str
    '''

    def get_regex_data(self) -> str:
        return self.__regex_data

    '''
        regex : RegexGen //Object that has regex syntax which is addable
        return : RegexGen 
    '''

    def combine(self, regex: Self) -> Self:
        try:
            if regex.__regex_data.startswith("^") and not self.__regex_data.endswith(('\s', " ", "\n", "\r")):
                raise Exception("In function {}, {} cannot be combined".format(
                    self.combine.__name__, regex.__regex_data))
        except (...):
            raise

        self.__regex_data += regex.__regex_data

        return self

    '''
        Accepts characters or ranges that forms a or operation of characters
        return : str
    '''
    @dispatch(str)
    @staticmethod
    def any_of(characters: str, capture: bool = False, **kwargs) -> str:
        if valid_ranges(characters, is_number, is_lower_case, is_upper_case) or characters.find(RegexGen.symbolsrange) != -1:
            pass

        for character in characters:
            if not type("a").isascii(character):
                raise Exception("In function {}, character : {} => Non ascii character is not acceptable".format(
                    RegexGen.any_of.__name__, character))
        return f"([{characters}])" if capture else f"(?:[{characters}])"

    '''
        This function is any_of_the_block with quantifiers or this function defines repetition of words in the list. 
        min : int => default = 0 // if min and max are both zero it must pass a keyword argument as True 
        max : int => default = 0
        pattern : a tuple[str, bool] expected a return type from exclude static function
        capture : bool => default=False //On True enclose the regex syntax in parenthesis so that regex engine capture data
        kwargs : dict => {
            zeroormore : bool => default=False,
            oneormore : bool => default=False
        }
        return : RegexGen
    '''
    # to be edited
    @dispatch((list, tuple))
    @staticmethod
    def any_of(characters: tuple[dict], capture: bool = False, **kwargs) -> str:
        character_str = str()
        tempstr = str()

        if not len(characters):
            return ""

        character_pair = list()
        for index, listitem in enumerate(characters):
            character = listitem.pop("character", None)
            min = listitem.pop("min", 0)
            max = listitem.pop("max", 0)
            if character is None:
                raise Exception("In function {}, at index {} doesn't have character pair.".format(
                    RegexGen.any_of.__name__, index))
            if len(character) == 0:
                continue
            elif len(character) == 1 or (len(character) == 2 and character in {"\s", "\d", "\w", "\W"}):
                pass
            elif len(character) == 3 and valid_ranges(character, is_lower_case, is_number, is_upper_case):
                pass
            else:
                raise Exception("In function {}, at index {}, Unknown Character: {}.".format(
                    RegexGen.any_of.__name__, index, character))
            tempstr = RegexGen.__add_quantifier(min=min, max=max, **listitem)
            character_pair.append(character+tempstr)

        character_str = "|".join(character_pair)
        return f"({character_str})" if capture else f"(?:{character_str})"

    '''
        some characters are predefined in the regex library thus they need to be escaped
        return : str 
    '''
    @staticmethod
    def characters(char: str) -> str:
        letters: str = str()
        if not char:
            raise Exception("In function {}, character : {} => Input cannot be none ".format(
                RegexGen.character.__name__, char))

        predefined_symbols: set = {
            '\\', '.', '(', ')', '*', '{', '}', '^', '+', '?', '[', ']', '$', '|'}

        list_iter = iter(enumerate(char))
        for index, lettr in list_iter:
            if lettr == "\\" and index != len(char) - 1 and char[index+1] in {'b', 'd', 'w', 'W'}:
                letters += f"{char[index:index+2]}"
                next(char, None)
                continue
            elif len(lettr) == 1 and lettr in predefined_symbols:
                letters += f"\\{lettr}"
            else:
                letters += lettr
        return letters

    '''
        This function is used to match the pattern succeeded by another pattern.
        min : int => default = 0 // if min and max are both zero it must pass a keyword argument as True 
        max : int => default = 0
        pattern : a tuple[str, bool] expected a return type from exclude static function
        capture : bool => default=False //On True enclose the regex syntax in parenthesis so that regex engine capture data
        kwargs : dict => {
            zeroormore : bool => default=False,
            oneormore : bool => default=False
        }
        return : RegexGen
    '''

    @dispatch(str, str)
    def succeeded_by(self, preceeding: str, succeeding: str, min: int = 0, max: int = 0, capture: bool = False, invert: bool = False, **kwargs) -> Self:
        return self.succeeded_by((preceeding, True), (succeeding, True), min=min, max=max, capture=capture, invert=invert, **kwargs)

    @dispatch((list, tuple), (list, tuple))
    def succeeded_by(self, preceeding: Tuple[str, bool], succeeding: Tuple[str, bool], min: int = 0, max: int = 0, capture: bool = False, invert: bool = False, **kwargs) -> Self:
        if not preceeding or len(preceeding) != 2:
            raise Exception("In function {} => characters1 tuple cannot be none or its length must be 2".format(
                RegexGen.succeeded_by.__name__))
        if not succeeding or len(succeeding) != 2:
            raise Exception("In function {} => characters2 tuple cannot be none or its length must be 2".format(
                RegexGen.succeeded_by.__name__))

        characterstr: str = str()
        temp: str = str()

        try:
            temp = self.__add_quantifier(min, max, **kwargs)
        except (...):
            raise

        followblock: str = str()
        if invert:
            followblock = f"(?!{succeeding[0]})" if succeeding[1] else f"(?![{succeeding[0]}])"
        else:
            followblock = f"(?={succeeding[0]})" if succeeding[1] else f"(?=[{succeeding[0]}])"

        precedingblock: str = f"{preceeding[0]}{temp}" if preceeding[1] else f"[{preceeding[0]}]{temp}"

        if len(self.__regex_data) > len(precedingblock) and \
                self.__regex_data.rindex(precedingblock) == len(self.__regex_data)-len(precedingblock)-1:
            characterstr += followblock
            self.__regex_data = self.__regex_data[:-1]
            characterstr += ')'
        else:
            characterstr = precedingblock + followblock
            characterstr = f"({characterstr})" if capture else f"(?:{characterstr})"
        self.__regex_data += characterstr
        return self

    '''
        This function is used to match pattern that is preceded by another pattern. If the pattern of the succeeded_by and preceeded_by matches the combination is union. 
        min : int => default = 0 // if min and max are both zero it must pass a keyword argument as True 
        max : int => default = 0
        pattern : a tuple[str, bool] expected a return type from exclude static function
        capture : bool => default=False //On True enclose the regex syntax in parenthesis so that regex engine capture data
        kwargs : dict => {
            zeroormore : bool => default=False,
            oneormore : bool => default=False
        }
        return : RegexGen
    '''

    @dispatch((list, tuple), (list, tuple))
    def preceded_by(self, preceding: Tuple[str, bool], succeeding: Tuple[str, bool], min: int = 0, max: int = 0, capture: bool = False, invert: bool = False, **kwargs) -> Self:
        if not preceding or len(preceding) != 2:
            raise Exception("In function {} => characters1 tuple cannot be none or its length must be 2".format(
                RegexGen.preceded_by.__name__))
        if not succeeding or len(succeeding) != 2:
            raise Exception("In function {} => characters2 tuple cannot be none or its length must be 2".format(
                RegexGen.preceded_by.__name__))

        characterstr: str = str()
        temp: str = str()

        try:
            temp = self.__add_quantifier(min, max, **kwargs)
        except (...):
            raise

        preceedingblock: str = str()
        if invert:
            preceedingblock = f"(?<!{preceding[0]})" if preceding[1] else f"(?<![{preceding[0]}])"
        else:
            preceedingblock = f"(?<={preceding[0]})" if preceding[1] else f"(?<=[{preceding[0]}])"

        followblock: str = f"{succeeding[0]}{temp}" if succeeding[1] else f"[{succeeding[0]}]{temp}"
        characterstr = preceedingblock + followblock
        characterstr = f"({characterstr})" if capture else f"(?:{characterstr})"
        self.__regex_data += characterstr
        return self

    @dispatch(str, str)
    def preceded_by(self, preceding: str, succeeding: str, min: int = 0, max: int = 0, capture: bool = False, invert: bool = False, **kwargs) -> Self:
        return self.preceded_by(RegexGen.exclude(preceding, True), RegexGen.exclude(succeeding, True), min=min, max=max, capture=capture, invert=invert, **kwargs)
