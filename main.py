from regexgen import RegexGen
import re

if __name__ == "__main__":
    # reg = RegexGen().digits(
    #     1, 10, RegexGen.exclude("23", True), capture=True)
    # print(reg.get_regex_data())

    # data = re.match(reg.get_regex_data(), "144")
    # data = re.match(reg.get_regex_data(), "249394")
    # print(data)

    regex = RegexGen().digits(1, 4)

    regex = RegexGen().text(RegexGen.anyof((
        RegexGen.characters('@'), RegexGen.characters('.'), RegexGen.digitsrange)))
    print(regex.get_regex_data())
    # print(RegexGen.exclude("23", True))
    # v = type("a").isascii("a123")
    # print(v)
