from src.regexgen import RegexGen

if __name__ == "__main__":
    # anyvalue = RegexGen.any_of(
    #     [{"character": '.', "min": 0, "max": 0, "zeroormore": True}])
    # regex = RegexGen().linestartwith().succeeded_by("",
    #                                                 anyvalue+RegexGen.any_of(RegexGen.range("a", "z")), min=1, max=1).succeeded_by("",
    # #                                                                                                                                anyvalue+RegexGen.any_of(RegexGen.range("A", "Z")), min=1, max=1).succeeded_by("",
    # #     
    # regex = RegexGen.digits(0,9,capture=True)                                                                                                                                                                                                          anyvalue+RegexGen.digitsrange, min=1, max=1).text(RegexGen.alphanumeric, min=8).endofline()
    regex = RegexGen().digits(zeroormore=True,capture=True).text(RegexGen.whitespace,0,1).any(oneormore=True,capture=True).text(RegexGen.characters(","),1,1).text(RegexGen.whitespace,1,1).any(oneormore=True,capture=True).alphabets(2,3,capture=True).text(RegexGen.whitespace,1,1).digits(4,4,capture=True)
    print(regex.get_regex_data())
