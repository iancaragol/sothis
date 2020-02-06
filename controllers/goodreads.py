import requests
import os
from bs4 import BeautifulSoup
from .book import Book

class GoodReads():
    """
        Handles all interactions with the GoodReads API documented here: https://www.goodreads.com/api/index#shelves.list
    """
    def __init__(self):
        self.key = self.get_key() # Client key
        self.secret = self.get_secret() # Client secret

    def get_key(self):
        """
            Returns client key
        """
        with open(os.getcwd() + "\\controllers\\secrets\\goodreads_key.txt") as f:
            key = f.readline().strip()
            return key
    
    def get_secret(self):
        """
            Returns client secret
        """
        with open(os.getcwd() + "\\controllers\\secrets\\goodreads_secret.txt") as f:
            secret = f.readline().strip()
            return secret
    
    def get_shelf(self, user_id, shelf_name):
        """
            Gets the content of a user's shelf.

            Args:
                user_id: The id of the user (integer)
                shelf_name: The name of the shelf (ex: on-hold)
        """
        url = "https://www.goodreads.com/review/list"
        params = {'v': 2,
                  'id': user_id,
                  'shelf': shelf_name,
                  'sort': 'isbn',
                  'per_page': 200,
                  'key' : self.key} 

        response = requests.get(url, params, verify=False)
        return response.content

    def get_books(self, shelf):
        """
            Creates book objects from the contents of a shelf
        """
        titles = self.parse_titles(shelf)
        isbns = self.parse_isbns(shelf)
        isbn13s = self.parse_isbn13s(shelf)
        authors = self.parse_author(shelf)

        books = []
        for i in range(len(titles)):
            b = Book(titles[i], isbns[i], isbn13s[i], authors[i])
            books.append(b)
        return books


    def parse_isbn13s(self, shelf):
        """
            Parses out all isbn13s from the shelf response
        """
        soup = BeautifulSoup(shelf, features="lxml")
        xml_isbns = soup.findAll('isbn13')
        isbns = [isbn.getText() for isbn in xml_isbns]
        return isbns

    def parse_isbns(self, shelf):
        """
            Parses out all isbns from the shelf response
        """
        soup = BeautifulSoup(shelf, features="lxml")
        xml_isbns = soup.findAll('isbn')
        isbns = [isbn.getText() for isbn in xml_isbns]
        return isbns

    def parse_titles(self, shelf):
        """
            Parses out all titles from the shelf response
        """
        soup = BeautifulSoup(shelf, features="lxml")
        xml_titles = soup.findAll('title_without_series')
        titles = [title.getText() for title in xml_titles]
        return titles

    def parse_author(self, shelf):
        """
            Parses out all author from the shelf response
        """
        soup = BeautifulSoup(shelf, features="lxml")
        xml_authors = soup.findAll('name')
        # xml_authors_names = xml_authors.find_all('name')
        authors = [author.getText() for author in xml_authors]
        return authors