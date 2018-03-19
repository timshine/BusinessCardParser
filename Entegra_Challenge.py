import nltk
from nltk.tokenize import word_tokenize
import unittest
import re

class ContactInfo:
    
    def __init__(self,document):
        """Initializes the variables for the program
            Opens the text files and stores the lines as a list of Strings
            Occupations is a list of job keywords to fix the NLTK recognizing occupations as PERSON"""
        with open (document) as f:
            lines = f.readlines()
            self.lines = [x.strip() for x in lines]
            self.occupations = ["engineer", "developer", "computer", "scientist", "technology", "analyst", "system", "manager", "mathematician", "entrepreneur"]

    def get_name(self):
        """Uses natural language processing to determine human names from other parts of speech in each line
            NLTK takes occupations to be labeled as PERSON so a list of occuraptions must be additionally checked to prevent inaccurate data
            Peron's name is returned
            Short circuiting was used to return the name: most often the name is one of the first lines so it stops need to traverse through whole list"""
        for line in self.lines:
            list_of_words = nltk.word_tokenize(line)
            for chunk in nltk.ne_chunk(nltk.pos_tag(list_of_words)):
                if type(chunk) == nltk.tree.Tree and not any(word in line.lower() for word in self.occupations):
                    if chunk.label() == 'PERSON':
                        return line        

    def get_phone_number(self):
        """Captures any line that has more than 9 numbers in it and with first pass names it a phone number
            Checks that same line for indications of it being a fax number rather than a phone number and only returns phone number
            If more than one number is given (ie. work and mobile) both numbers will be returned in a list"""
        for line in self.lines:
            phone_number=list()
            for char in line:
                try:
                    phone_number.append(int(char))
                except ValueError:
                    continue
            if len(phone_number)>=9 and ("fax" or "f") not in line.lower():
                return ''.join(str(num) for num in phone_number)


    def get_email_address(self):
        """An email is characterized by one or more characters followed by @ symbol, one or more characters, a period and finally one or more characters
            A regular expression is used to find any lines with this format"""
        email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')
        for line in self.lines:
            match = email_regex.match(line)
            if match:
                return match.group() 
        return None

    def get_contact_info(self):
        """Returns get_name, get_phone_number, and get_email_address with proper formatting"""
        return "Name: {}\nPhone Number: {}\nEmail Address: {}".format(self.get_name(), self.get_phone_number(), self.get_email_address())

class BusinessCardParser:

    def get_contact_info(self, document):
        return ContactInfo(document).get_contact_info()
        
        
def main():
    print(BusinessCardParser().get_contact_info("Input.txt"))

class TestChallenge(unittest.TestCase):
    def test_get_name(self):
        self.assertEqual(ContactInfo('Input.txt').get_name(), 'Arthur Wilson')
        self.assertEqual(ContactInfo('Input.txt').get_phone_number(), '17035551259')
        self.assertEqual(ContactInfo('Input.txt').get_email_address(), 'awilson@abctech.com')

if __name__ == '__main__':
    main()
    unittest.main(exit=False, verbosity=2)
