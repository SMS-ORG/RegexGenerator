from typing_extensions import Self
from typing import Tuple
import re

"""
Docs for RegexGenerator
"""

class RegexGen:
    """
    Start of the class
    """
    # ranges
    lowercaserange: str = "[a-z]"
    uppercaserange: str = "[A-Z]"
    digitsrange: str = "[0-9]"
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



    def linestartwith(self):
        '''
        <p><code>linestartwith</code> adds a expression to indicates beginning of the string and is always added on a new line.<br>
        The function definition is: </p> 
            ```
            linestartwith(self)
            ```
        <p>When this function is called, the function adds the expression '^' if no regex data exists already.</p>
        <p>If the regex data already exists then the function adds the expression '\\n^' indicating line is changed before signifying beginning of the string.  </p>
        <p><code>Linestartwith</code> function can be used in combination with other function to create a regex syntax to check if the expression starts with certain pattern.<br>
        </p>
        ```
        regex = RegexGen().linestartwith().text('foo').any(1,5).text('bar').endofline()
        ```       
        <p>This code checks for text starting with 'foo' and starting with 'bar' after any characters of length of min 1 and max 5 digits.</p>
        <p>The regex is displayed as:</p>
        <pre> regex = "^foo.{1,5}bar"</pre>
    ^ character symbolizes the start of the string or line.
    '''
        if not len(self.__regex_data):
            self.__regex_data += '^'
        else:
            self.__regex_data += '\n^'
        return self



    def endofline(self):
        '''
        <p><code>endofline</code> adds a expression to indicates end of the string and end of the line.<br>
            The function definition is:  
            <code>endofline(self)</code></p>
        <p>When this function is called, the function adds the expression '$' to the regex data.</p>
        <p>If the regex data already exists then the function adds the expression '\n^' indicating line is changed before signifying beginning of the string.  </p>
        <p><code>endofline</code> function can be used in combination with other function to create a regex syntax to check if the expression ends with certain pattern.<br>
        </p>
<pre><code><p>regex = RegexGen().regex.text('abc', 1, 1).endofline()</p></code></pre>           
<p>This code checks for text ending with 'abc' after any characters of any length </p>
<p>The regex is displayed as:</p>
<pre> regex = "abc$"</pre>
    $ character symbolizes as end of a line
    '''
        self.__regex_data += '$'
        return self
    
    @staticmethod
    def range(start: str, end: str) -> str:
        """
        <p><code>Range</code> function provides syntax for defining range.<br><br>
            In the function definition, 
            <code>range(start: str, end: str)</code>
            ,
            <ol class="list-group list-group-numbered">
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                        start accepts string for starting range whose length must be 1.                 
                    </div></li>
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                        end accepts string for ending range whose length must be 1.                
                    </div></li>
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                        return returns the range in format &#60;start>-&#60;end>
                    </div></li>
                </ol><br></p>
        <pre><code><p>regex = RegexGen().regex.range('a', 'z')</p></code></pre>           
        <p>The regex is displayed as:</p>
        <pre> regex = "[a-z]"</pre>
        Range for symbols will throw an error
        start : str // length must be 1
        end : str  //length must be 1
        return : str //returns the range in format <start>-<end>
    """
        if (not start and not end) and (len(start) > 1 and len(end) > 1):
            raise Exception("In function {}, range_start : {}, range_end:{} => Characters cannot be None".format(
                RegexGen.range.__name__, start, end))

        # check if range is valid
        character_range = f"({start}-{end})"
        if (valid_ranges(character_range, is_lower_case, is_upper_case, is_number)):
            return character_range
        raise Exception("In function {}, range_start : {}, range_end:{} => This is not a valid range. Valid ranges are 0-9,A-Z or a-z or \W".format(
            RegexGen.range.__name__, start, end))


    @staticmethod
    def exclude(characters: str, pattern_prevent: bool = False) -> Tuple[str, bool]:
        '''
        <p><code>Exclude</code> function is a static function. It excludes certain pattern based upon the input of the user.<br>
                            In the function definition, <code>exclude(characters: str, pattern_prevent: bool = False) -> tuple</code>,
                            <ol class="list-group list-group-numbered">
                                <li class="list-group-item d-flex justify-content-between align-items-start">
                                    <div class="ms-2 me-auto">
                                        the characters : str signifies characters to be matched, <br>
                                    </div></li>
                                <li class="list-group-item d-flex justify-content-between align-items-start">
                                    <div class="ms-2 me-auto">
                                        pattern_prevent : str (default = False) Here, on True, prevents the characters sequence to match(The sequence must not contain a range) <br>
                                        and on false prevent piecewise occuring of characters.
                                        and returns a tuple                    
                                    </div></li>
                               </p>
                        <pre><code><p>RegexGen().digits(1, 10, RegexGen.exclude("23", True), capture=True) </p></code></pre>           
                        
                        <p>The regex is displayed as:</p>
                        <pre> regex = "\b(?:(?![23])\d)+\b"</pre>
        characters : str  //characters to be matched
        pattern_prevent : bool  => default = False //On True, prevents the characters sequence to match(The sequence must not contain a range) 
                                                //and on false prevent piecewise occuring of characters.
        return : tuple
    '''
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

    @staticmethod
    def boundary_character(character: str, start: bool = True) -> str:
        '''
        character: str,
        start : bool, => default = True //On true, the letter is the left boundary of the word 
                                        //and on false the letter is the right boundary of the word
    '''
        if len(character) > 2:
            raise Exception("In function {}, start : {} => Character cannot be length greater than two",
                            RegexGen.boundary_character.__name__, start)
        elif len(character) == 2 and character not in {"\w", "\W", "\d", "\."}:
            raise Exception("In function {}, start : {} => Character is not a \w or \W or \d or \.",
                            RegexGen.boundary_character.__name__, start)

        character_str = "\b" + character if start else character + "\b"
        return character_str



    def __add_quantifier(self, min: int, max: int, **kwargs) -> str:
        '''
        <p><code>__add_quantifier</code>adds quantifiers like ? + * x(n,m).<br>
        The function definition is:  
            <code>__add_quantifier(self, min: int, max: int, **kwargs)</code></p>
        The regex generated depends on the value of min and max.
            <ol class="list-group list-group-numbered">
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="fw-bold">min == max and max == 0:</div>
                    If no characters exist then the exception is raised stating min and max can't be zero.       

                    <div class="ms-2 me-auto">
                        <pre> regex = " "</pre>                    </div></li>
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="fw-bold">max == min and min == 1:</div>
                    <div class="ms-2 me-auto">
                        <pre> regex = "^foo.{1,5}bar"</pre>                    </div></li>
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="fw-bold">max == min:</div>
                    <div class="ms-2 me-auto">
                        <pre> regex = "^foo.{1,5}bar"</pre>                    </div></li>                
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="fw-bold">min == 0 and max == 1:</div>
                    <div class="ms-2 me-auto">
                        <pre> regex = "^foo.{1,5}bar"</pre>                    </div></li>  
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="fw-bold">max == 0 and min > 0:</div>
                    <div class="ms-2 me-auto">
                        <pre> regex = "^foo.{1,5}bar"</pre>                    </div></li>  
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="fw-bold">max > min and min > 0:</div>
                    <div class="ms-2 me-auto">
                        <pre> regex = "^foo.{1,5}bar"</pre>                    </div></li>  
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="fw-bold">Else:</div>
                    <div class="ms-2 me-auto">
                    <!-- If no characters exist then the exception is raised stating min and max can't be zero.        -->
                    </div></li>                      
                </ol><br>
            </p>
        <pre> regex = "^foo.{1,5}bar"</pre>
        Add Quantifiers like {0},{0,1},?,*,+,{0,1}
    '''
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
                                .format(self.__add_quantifier.__name__))
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

    def text(self, character: str, min: int = 0, max: int = 0, **kwargs) -> Self:
        ''' 
        <p><code>Text</code> function simply adds the input to regex syntax.</p>
        <pre><code><p>RegexGen.text("This is a text.") </p></code></pre>           
        
        <p>The regex is displayed as:</p>
        <pre> regex = "This is a text."</pre>
        Text is generated using Characters function.
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

    def any(self, min: int = 0, max: int = 0, capture: bool = False, **kwargs) -> Self:
        ''' 
        <p><code>Any</code> function generates a regex which can be utilized to check if a certain character exists in the expression<br>
            In the function definition, 
            <code>any(self, min: int = 0, max: int = 0, capture: bool = False, **kwargs) -> Self:</code>
            ,
            <ol class="list-group list-group-numbered">
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                        the min : int and max : int has default = 0. If min and max are both zero it must pass a keyword argument as True max : int (default = 0). <br>
                    </div></li>
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                        If on capture : bool (default=False) True is passed, it  enclose . in parenthesis so that regex engine capture data. <br>
                    </div></li>
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                        The kwargs : dict accepts {<br>
                            zeroormore : bool  (default=False), <br>
                            oneormore : bool  (default=False)            
                    </div></li>
                    <li class="list-group-item d-flex justify-content-between align-items-start">
                        <div class="ms-2 me-auto">
                            The return returns RegexGen
                        </div></li></ol><br></p>
        <pre><code>regex = RegexGen()
            regex = regex.any(min=0, max=12)</code></pre>           
        
        <p>The regex is displayed as:</p>
        <pre>  regex = ".{0,12}"</pre> 
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
        anystr: str = str()
        temp: str = str()

        try:
            temp = self.__add_quantifier(min, max, **kwargs)
        except (...):
            raise

        anystr = f"(.{temp})" if capture else f".{temp}"
        self.__regex_data += anystr

        return self


    def digits(self, min: int = 0, max: int = 0, pattern: Tuple[str, bool] = None, capture: bool = False, **kwargs) -> Self:
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

    def alphabets(self, min: int = 0, max: int = 0, pattern: Tuple[str, bool] = None, capture: bool = False, **kwargs) -> Self:
        '''
        <p><code>Alphabets</code> function matches only words(not numbers) that may not contain a sequence of letters or each of the letters exist independently.<br>
                </p>
        In the function definition, 
        <code>alphabets(self, min: int = 0, max: int = 0, pattern: Tuple[str, bool] = None, capture: bool = False, **kwargs)</code>
        , <br><br>
        <ol class="list-group list-group-numbered">
        <li class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
                the min : int and max : int has default = 0. If min and max are both zero it must pass a keyword argument as True max : int (default = 0). <br>
            </div></li>
        <li class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
                In pattern, a tuple[str, bool] is expected as a return type from exclude static function. <br>
            </div></li>
        <li class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
                If on capture : bool (default=False), True is passed, it  encloses the regex syntax in parenthesis so that regex engine captures data.<br>
            </div></li>
        <li class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
                The kwargs : dict accepts {<br>
                    zeroormore : bool  (default=False), <br>
                    oneormore : bool  (default=False)            
            </div></li>
            <li class="list-group-item d-flex justify-content-between align-items-start">
                <div class="ms-2 me-auto">
                    The return returns RegexGen
                </div></li></ol><br>
        <pre><code><p>regex = RegexGen().alphabets(1,5)</p></code></pre>           
        <p>The regex is displayed as:</p>
        <pre> regex = "[a-zA-Z]{1,5}"</pre>
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

    def get_non_capturing_regex(self) -> str:
        '''
        If the program have capture parameters it will prevent regex engine from capturing index and patterns from the string 
        reducing capturing overhead and hence increase efficiency
        return : str 
    '''
        return f"(?:{self.__regex_data})"

    def get_regex_data(self) -> str:
        '''
        Returns a regex syntax that may capture the text from the input string. 
        return : str
    '''
        return self.__regex_data

    def combine(self, regex: Self) -> Self:
        '''
        <p><code>Combine</code> function creates a regex syntax to combine two regex expressions in one to create a pattern.<br>
                </p>
        In the function definition, 
        <code>combine(self, regex: Self)</code>
        , the function accepts value of two different regex to perform the combination operation. <br>
        <pre><code><p>regexa = RegexGen().digits(4,4).text(RegexGen.characters('-'))
            regexb = RegexGen().digits(3,3)
            regex = RegexGen.combine(regexa, regexb) </p></code></pre>           
        
        <p>The regex is displayed as:</p>
        <pre> regex = "\d{4,4}-\d{3,3}"</pre>
        regex : RegexGen //Object that has regex syntax which is addable
        return : RegexGen 
    '''
        if len(regex.__regex_data) == 0:  # and regex.__regex_data[0] == '^':
            raise Exception("Invalid regex to combine")

        self.__regex_data += regex.__regex_data

        return self

    @staticmethod
    def anyof(characters: str, capture: bool = False, pattern_prevent: bool = False) -> str:
        '''
        Accepts characters or ranges that forms a or operation of characters
        return : str
    '''
        character_string: str = str()

        for character in characters:
            if not type("a").isascii(character):
                raise Exception("In function {}, character : {} => Non ascii character is not acceptable".format(
                    RegexGen.anyof.__name__, character))
            try:
                if valid_ranges(character, is_number, is_lower_case, is_upper_case) or character.find(RegexGen.symbolsrange) != -1:
                    pass
            except (...):
                raise

            character_string += f"{character}|" if pattern_prevent else character

        if pattern_prevent:
            character_string = character_string[:-2]

        character_string = f"[{character_string}]" if not pattern_prevent else character_string

        return f"({character_string})" if capture else f"(?:{character_string})"

    @staticmethod
    def characters(char: str) -> str:
        '''
        <p><code>Characters</code> function is a static function which is unable to create a regex syntax.<br>
                                Instead, a function like Text is required to submit to the regex syntax. <br>
                                Charcters is used some characters predefined in the regex library are used and thus they need to be escaped.</p>
                        <pre><code><p>RegexGen.text(RegexGen.characters("This+is{a$text.") </p></code></pre>           
                        
                        <p>The regex is displayed as:</p>
                        <pre> regex = "This\+is\{a\$text\."</pre>
        some characters are predefined in the regex library thus they need to be escaped
        return : str 
    '''
        letters: str = str()
        if not char:
            raise Exception("In function {}, character : {} => Input cannot be none ".format(
                RegexGen.character.__name__, char))

        predefined_symbols: set = {
            '\\', '.', '(', ')', '*', '{', '}', '^', '+', '?', '[', ']', '$', '|'}

        for lettr in char:
            if lettr in predefined_symbols:
                letters += f"\\{lettr}"
            else:
                letters += lettr
        return letters

    def succeeded_by(self, preceeding: Tuple[str, bool], succeeding: Tuple[str, bool], min: int = 0, max: int = 0, capture: bool = False, invert: bool = False, **kwargs) -> Self:
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

    def preceded_by(self, preceding: Tuple[str, bool], succeeding: Tuple[str, bool], min: int = 0, max: int = 0, capture: bool = False, invert: bool = False, **kwargs) -> Self:
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

    def any_of_q(self, character_list: Tuple[str], min: int = 0, max: int = 0, capture: bool = False, **kwargs):
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
        character_str = str()
        tempstr = str()

        if not len(character_list):
            return self
        try:
            tempstr = self.__add_quantifier(min, max, **kwargs)
        except (...):
            raise

        character_str = "(" if capture else '(?:'
        character_str += ('|').join(character_list)
        character_str += ')'

        character_str += tempstr
        self.__regex_data += character_str
        return self
