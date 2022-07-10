import email
import string
import nltk
from Stripper import MLStripper

# sirve para limpiar el archivo html de los tags
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



# The class has a method called parse that takes an email as a string and returns a dictionary with
# the subject, body, and content type of the email. 
# 
# The parse method calls the get_email_content method. 
# 
# The get_email_content method takes a message object and returns a dictionary with the subject, body,
# and content type of the email. 
# 
# The get_email_content method calls the get_email_body method. 
# 
# The get_email_body method takes a payload and a content type and returns a list of tokens. 
# 
# The get_email_body method calls the tokenize method. 
# 
# The tokenize method takes a text string and returns a list of tokens. 
# 
# The tokenize method calls the stemmer method. 
# 
# The stemmer method takes a word and returns the stem of the word. 
# 
# The stemmer method calls the stopwords method
class Parser:

    def __init__(self):
        self.stemmer = nltk.PorterStemmer()
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        self.punctuation = list(string.punctuation)

    def parse(self, email_data):
        """
        It opens the email file, reads it, and then returns the content of the email
        
        :param email_path: The path to the email file
        :return: The email content.
        """
        msg=email.message_from_string(email_data)
        return None if not msg else self.get_email_content(msg)

    def get_email_content(self, msg):
        """
        It takes a message object, and returns a dictionary with the subject, body, and content type of
        the message
        
        :param msg: The email message
        :return: A dictionary with the subject, body, and content type of the email.
        """
        # print (msg)
        subject = self.tokenize(msg['Subject']) if msg['Subject'] else []
        body = self.get_email_body(msg.get_payload(),
                                    msg.get_content_type())
        content_type = msg.get_content_type()
        return {"subject": subject,
                "body": body,
                "content_type": content_type}

    def get_email_body(self, payload, content_type):
        """
        If the payload is a string and the content type is text/plain, return the tokenized payload. 
        
        If the payload is a string and the content type is text/html, return the tokenized payload with
        the HTML tags stripped. 
        
        If the payload is a list, iterate through the list and call the function recursively. 
        
        The function returns a list of tokens. 
        
        The function is called recursively because the payload can be a list of payloads. 
        
        The function is called recursively because the payload can be a list of payloads. 
        
        The function is called recursively because the payload can be a list of payloads. 
        
        The function is called recursively because the payload can be a list of payloads. 
        
        The function is called recursively because the payload can be a list of payloads. 
        
        The function is called rec
        
        :param payload: The payload of the email
        :param content_type: The content type of the email
        :return: A list of tokens
        """
        body = []
        if type(payload) is str and content_type == 'text/plain':
            return self.tokenize(payload)
        elif type(payload) is str and content_type == 'text/html':
            return self.tokenize(strip_tags(payload))
        elif type(payload) is list:
            for p in payload:
                body += self.get_email_body(p.get_payload(),
                                            p.get_content_type())
        return body

    def tokenize(self, text):
        """Transform a text string in tokens. Perform two main actions,
        clean the punctuation symbols and do stemming of the text."""
        for c in self.punctuation:
            text = text.replace(c, "")
        text = text.replace("\t", " ")
        text = text.replace("\n", " ")
        tokens = list(filter(None, text.split(" ")))
        return [self.stemmer.stem(w) for w in tokens if w not in self.stopwords]