from regexgen import RegexGen
import re

if __name__ == "__main__":

    # regex = RegexGen().text('foo').text(RegexGen().whitespace).text('bar')
    # print(regex.get_regex_data())
    # data = re.match(reg.get_regex_data(), "144")
    # data = re.match(reg.get_regex_data(), "249394")
    # print(data)
    # regex = RegexGen().digits(4, 4).text(RegexGen.characters("-")).digits(3,
    #                                                                           3).text(RegexGen.characters("-"), 1, 1).digits(3, 3)
    # regex = RegexGen().digits(1, 4)

    # regex = RegexGen().text(RegexGen().alphanumeric, 4, 4)
    # print(regex.get_regex_data())

    regex = RegexGen().preceded_by(RegexGen.exclude('INVOICE Number',pattern_prevent= True),RegexGen.exclude(RegexGen.alphanumeric),oneormore = True)
    print(regex.get_regex_data())
