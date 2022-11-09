import re
from regexgen import RegexGen

streets = [
    "21 Bungana Drive, Kybunga SA 5453",
    "Thomas Lane, Fitzroy North VIC 3068",
    "107 Quayside Vista, Kingston ACT 2604",
    "94 Prince Street, Lower Coldstream NSW 2460",
    "George Street, Brisbane QLD 4000"
]
regex = RegexGen().digits(zeroormore=True,capture=True).text(RegexGen.whitespace,0,1).any(oneormore=True,capture=True).text(RegexGen.characters(","),1,1).text(RegexGen.whitespace,1,1).any(oneormore=True,capture=True).alphabets(2,3,capture=True).text(RegexGen.whitespace,1,1).digits(4,4,capture=True)

# regex = r'(\d*)\s?(.+),\s(.+)([a-zA-Z]{2,3})\s(\d{4})'
# results = {}
print('{:<26} {:<20}  {:<30} {:<20} {:<10}'.format('\033[1;32mHouse_Number',    'Street Name', 'Suburb', 'State', 'Postcode\033[0;0m'))
for street in streets:
    match = re.search(regex.get_regex_data(), street, flags=re.IGNORECASE)
    house_number = match.group(1)
    street_name = match.group(2)
    suburb = match.group(3)
    state = match.group(4)
    postcode = match.group(5)
    result = '{:<20} {:<20}  {:<30} {:<20} {:<10}'.format(house_number, street_name, suburb, state, postcode)
    print(result)
