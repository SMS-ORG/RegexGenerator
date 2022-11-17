import mysql.connector
from regexgen import RegexGen
import re
import config as cfg

#Establishing the connection with the database using the config file
mydb = mysql.connector.connect(**cfg.config)

mycursor = mydb.cursor()

#regex to find the detail pf the user whose email start with r and ends with @gmail.com
regex1 = RegexGen()
regex1 = regex1.linestartwith().text('r',1,1).any(zeroormore = True).text('@gmail.com', 1, 1).endofline()
query1 = "SELECT * FROM users where email REGEXP (%s)"
regex1 = regex1.get_regex_data()
mycursor.execute(query1,(regex1,))
myresult = mycursor.fetchall()
print(query1.format(myresult))
for x in myresult:
  print(x)

print('-'*60)

#regex to find the detail of the user whose phone number start with +977 98
regex2 = RegexGen()
regex2 = regex2.linestartwith().text(RegexGen.characters("+977"),1,1).text(RegexGen.whitespace, 1, 1).text('98',1,1).digits(8,8)
query2 = "SELECT * FROM users where phone REGEXP (%s)"
regex2 = regex2.get_regex_data()
mycursor.execute(query2,(regex2,))
myresult = mycursor.fetchall()

for x in myresult:
  print(x)

