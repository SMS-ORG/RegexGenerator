import re
from regexgen import RegexGen

email =  RegexGen().linestartwith().text(RegexGen.alphanumeric,oneormore = True).text(RegexGen.characters("@"),1,1).text(RegexGen.alphanumeric,oneormore = True).text(RegexGen.characters("."),1,1).alphabets(2,).endofline()
email_condition = email.get_regex_data()
anyvalue = RegexGen.any_of([{"character": '.', "min": 0, "max": 0, "zeroormore": True}])
password = RegexGen().linestartwith().succeeded_by("",anyvalue+RegexGen.any_of(RegexGen.range("a", "z")), min=1, max=1).succeeded_by("",anyvalue+RegexGen.any_of(RegexGen.range("A", "Z")), min=1, max=1).succeeded_by("",anyvalue+RegexGen.digitsrange, min=1, max=1).text(RegexGen.alphanumeric, min=8).endofline()
password_condition = password.get_regex_data()
user_email = input('Enter your Email :')


if re.search(email_condition, user_email):
    user_password = input('Enter your password :')
    if re.search(password_condition, user_password):
        print("Email and password Validated")
    else:
        print("Invalid Password")
else:
    print("Invalid Email")