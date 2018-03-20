# BusinessCardParser

**This program is a business card reader with the following attributes**
  * Uses parsed results from Optical Character Recognition (OCR)
  * Extracts name, phone number and email address from business card
  * Provides sample test cases and sample main() output
  
## How to Setup ##
  * Install Natural Language Toolkit (NLTK) from [Install NLTK Module](https://www.nltk.org/install.html)
  * Run most recent version of Python 3.*

## Programming Approach ##
  * Names were extracted from the document using the nltk named entity chunker
    * This chunker assigns values of PERSON, ORGANIZATION, TIME, etc. to each chunk of information
    * A reference used for NLTK is [NLTK Reference](https://stackoverflow.com/questions/31836058/nltk-named-entity-recognition-to-a-python-list) 
    * NLTK assigns job titles as a chunk of PERSON
      * A running list of common job keywords was created and is checked before accepting the information as chunked as PERSON as a name
      * This list should be added to based on positions available, but a few examples were given in this code
  * Phone numbers were extracted using regular expressions
    * A reference used for regular expressions for phone number is [Phone Number RegEx](http://www.diveintopython.net/regular_expressions/phone_numbers.html)
    * The regular expression was then customized for this application
    * A good tool for solving regular expressions is https://www.debuggex.com/ 
  * Email addresses were also extracted using regular expressions
    * A reference used for regular expressions for email addresses is [Email Address RegEx](https://www.regular-expressions.info/email.html)
    * This regular expression was then customized for this application
    
## Interface Specification ##
 * The method get_contact_info(document) will return an instance of the object ContactInfo(name, email, phone)
 * The attributes can then be attained using the respective get methods in the ContactInfo class
