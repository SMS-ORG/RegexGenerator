from src.regexgen import RegexGen

if __name__ == "__main__":
    anyvalue = RegexGen.any_of(
        [{"character": '.', "min": 0, "max": 0, "zeroormore": True}])
    regex = RegexGen().linestartwith().succeeded_by("",
                                                    anyvalue+RegexGen.any_of(RegexGen.range("a", "z")), min=1, max=1).succeeded_by("",
                                                                                                                                   anyvalue+RegexGen.any_of(RegexGen.range("A", "Z")), min=1, max=1).succeeded_by("",
                                                                                                                                                                                                                  anyvalue+RegexGen.digitsrange, min=1, max=1).text(RegexGen.alphanumeric, min=8).endofline()
    print(regex.get_regex_data())
