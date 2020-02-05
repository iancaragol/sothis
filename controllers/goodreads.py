import requests
import os
from bs4 import BeautifulSoup

# DOCS: https://www.goodreads.com/api/index#shelves.list

class GoodReads():
    def __init__(self):
        self.key = self.get_key()
        self.secret = self.get_secret()

    def get_key(self):
        with open(os.getcwd() + "\\controllers\\secrets\\goodreads_key.txt") as f:
            key = f.readline().strip()
            return key
    
    def get_secret(self):
        with open(os.getcwd() + "\\controllers\\secrets\\goodreads_secret.txt") as f:
            secret = f.readline().strip()
            return secret
    
    def get_shelf(self, user_id, shelf_name):
        url = "https://www.goodreads.com/review/list"
        params = {'v': 2,
                  'id': user_id,
                  'shelf': shelf_name,
                  'sort': 'isbn',
                  'per_page': 200,
                  'key' : self.key} 

        response = requests.get(url, params)
        return response.content

    def parse_isbns(self, shelf):
        soup = BeautifulSoup(shelf)
        xml_isbns = soup.findAll('isbn13')
        isbns = [isbn.getText() for isbn in xml_isbns]
        return isbns