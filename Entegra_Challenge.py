import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
import re
import unittest

"""
Author: Timothy Shine

Parses results from Optical Character Recognition (OCR)
Extracts name, phone number and email address from business card
Provides sample test cases and sample main output
"""

class ContactInfo:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def get_name(self):
        """Returns the contact's name""" 
        return self.name

    def get_email_address(self):
        """Returns the contact's email address""" 
        return self.email

    def get_phone_number(self):
        """Returns the contact's phone number"""
        return self.phone

class BusinessCardParser:
    def get_contact_info(self, document):
        """Initializes the variables for the program
            Opens the text files and stores the lines as a list of Strings
            Occupations is a list of job keywords to fix the NLTK recognizing occupations as PERSON
            Sets variables of name, phone_number, and email_address to their respective values from processing functions"""
        try:
            f = open (document, 'r')
        except FileNotFoundError:
            return "Can't open ", document
        else:    
            with f:
                lines = f.readlines()
                self.lines = [x.strip() for x in lines]
                self.occupations = ["engineer", "developer", "computer", "scientist", 
                                    "technology", "analyst", "system", "manager", 
                                    "mathematician", "entrepreneur"]            #list of job keywords for NLP
                self.name = self._process_name()
                self.phone_number = self._process_phone_number()
                self.email_address = self._process_email_address()
                return ContactInfo(self.name, self.email_address, self.phone_number)

    def _process_name(self):
        """Uses natural language processing to determine human names from other parts of speech in each line
            NLTK takes occupations to be labeled as PERSON so a list of occuraptions must be additionally checked to prevent inaccurate data
            Peron's name is returned
            Short circuiting was used to return the name: most often the name is one of the first lines so it stops need to traverse through whole list"""
        for line in self.lines:
            list_of_words = nltk.word_tokenize(line)                    #tokenizes each line into a list of words
            for chunk in nltk.ne_chunk(nltk.pos_tag(list_of_words)):    #Part of speech tag as well as named entity chunking on each chunk of tokens
                if type(chunk) == Tree and not any(word in line.lower() for word in self.occupations):  #double checks each is a proper chunk not containing a job keyword
                    if chunk.label() == 'PERSON':
                        return line     #is a person's name

    def _process_phone_number(self):
        """Determines which line is a phone number in the document using a regular expression
            Checks to see if the line is a fax number before returning: will not return fax numbers"""
        for line in self.lines:
            is_fax = re.match(r'^(Fax|Facsimile|F):?', line, re.IGNORECASE)
            if is_fax:
                continue        #is a fax number
            else:
                result = re.match(r'^([\w ]+)?:?\s*\+?(\d+)?\s?\(?(\d{3})\)?[ .-]?(\d{3})[ .-]?(\d{4})$', line)
                if result:
                    return "{}{}{}{}".format((result.groups(0)[1] if str(result.groups(0)[1]) != '0' else ""), # country code
                                         result.groups(0)[2], # area code
                                         result.groups(0)[3], # NPA
                                         result.groups(0)[4]) # line number
        return None        

    def _process_email_address(self):
        """An email is characterized by one or more characters followed by @ symbol, one or more characters, a period and finally one or more characters
            A regular expression is used to find any lines with this format"""
        for line in self.lines:
            is_email = re.match(r'^([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z{2,}]+)', line)
            if is_email:
                return is_email.group(0)    #email without the indicator "Email:" or variant
            else:
                is_email = re.match(r'^(\w+:?\s?)([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z{2,}]+)', line)
                if is_email:
                    return is_email.group(2) #email with the indicator "Email:" or variant
        return None

def main():
    """Example output for BusinessCardParser and functions that can be accessed"""
    fname = 'Input.txt'
    parser = BusinessCardParser()
    contact = parser.get_contact_info(fname)
    print("Name:", contact.get_name())
    print("Phone:", contact.get_phone_number())
    print("Email:", contact.get_email_address())


class TestChallenge(unittest.TestCase):
    def test_get_name(self):
        """Tests name, phone and email using Arthur Wilson test case in Input.txt"""
        self.assertEqual(BusinessCardParser().get_contact_info("Input.txt").get_name(), 'Arthur Wilson')
        self.assertEqual(BusinessCardParser().get_contact_info("Input.txt").get_phone_number(), '17035551259')
        self.assertEqual(BusinessCardParser().get_contact_info("Input.txt").get_email_address(), 'awilson@abctech.com')

if __name__ == '__main__':
    main()
    unittest.main(exit=False, verbosity=2)
