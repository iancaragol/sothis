class Book:
    """
        Container for various information on a book
    """
    def __init__(self, title, isbn, isbn13, author):
        self.title = title
        self.isbn = isbn
        self.isbn13 = isbn13
        self.author = author

    def to_str(self):
        """
            Returns <title, author - (ISBN: , ISBN13: )
        """
        return self.title + ", " + self.author + " - (ISBN: " + self.isbn + ", ISBN13: " + self.isbn13 + ")"