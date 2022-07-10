from html.parser import HTMLParser

# Esta clase sirve para limpiar el codigo html
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        """
        It takes a string as input and appends it to the list fed
        
        :param d: the data that was just read in
        """
        self.fed.append(d)

    def get_data(self):
        """
        It takes a string and returns a string
        :return: The data that was fed to the parser.
        """
        return ''.join(self.fed)