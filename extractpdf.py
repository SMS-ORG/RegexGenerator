import PyPDF2
from regexgen import RegexGen
import re
  
# creating a pdf file object
pdfFileObj = open('Examples\Example1\example1.pdf', 'rb')
  
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  
# printing number of pages in pdf file
print(pdfReader.numPages)
  
# creating a page object
pageObj = pdfReader.getPage(0)

print(pageObj.extractText())

regex1 = RegexGen().preceded_by(RegexGen.exclude('Invoice Num ',pattern_prevent= True),RegexGen.exclude(RegexGen.alphanumeric),oneormore = True)
# print(regex1.get_regex_data())
data1 = re.search(regex1.get_regex_data(), pageObj.extractText())
print(data1.group())
regex1 = RegexGen().preceded_by(RegexGen.exclude('Invoice Date ',pattern_prevent= True),RegexGen.exclude(RegexGen.alphanumeric),oneormore = True)
data2 = re.search(regex1.get_regex_data(), pageObj.extractText())
print(data2.group())