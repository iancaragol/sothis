import requests
import os
import json
import base64
import webbrowser

class OverDrive():
    """
        Handles all interactions with the OverDrive API documented here: https://developer.overdrive.com/apis
    """
    def __init__(self):
        self.key = self.get_key() # Client key
        self.secret = self.get_secret() # Client secret
        self.library_catalogs = {} # <Library Id, Catalog Id>
        self.user_agent = "Sothis" # User Agent sent in request header
        self.circulation_host_url = "integration.api.overdrive.com" # Endpoint for circulation
        self.circulation_api_base_url = "https://integration.api.overdrive.com"
        self.patron_api_host_url = "integration-patron.api.overdrive.com" # Endpoint for patron
        self.patron_api_base_url = "https://integration-patron.api.overdrive.com"
        self.redirect_uri = "https://services.slcpl.org/" # User is redirected to this url granting access


    def get_key(self):
        """
            Returns client key
        """
        with open(os.getcwd() + "\\controllers\\secrets\\overdrive_key.txt") as f:
            key = f.readline().strip()
            return key

    def get_secret(self):
        """
            Returns client secret
        """
        with open(os.getcwd() + "\\controllers\\secrets\\overdrive_secret.txt") as f:
            secret = f.readline().strip()
            return secret

    def authorize(self):
        """
            Performs OAuth for Circulation API

            Returns:
                access_token : Access token used in all further requests
                token_type : Type of token (Bearer)
        """
        auth_endpoint = "https://oauth.overdrive.com/token"
        key_secret = self.key + ":" + self.secret
        auth_string = base64.b64encode(key_secret.encode("utf-8"))

        headers = {
            'Authorization': "Basic {}".format(auth_string.decode("utf-8")),
            'Host' : "oauth.overdrive.com",
            'Content-Type' : "application/x-www-form-urlencoded;charset=UTF-8"
        }

        body = "grant_type=client_credentials"

        response = requests.post(auth_endpoint, headers = headers, data = body, verify=False)
        response_json = json.loads(response.content.decode("utf-8"))

        access_token = response_json['access_token']
        token_type = response_json['token_type']

        return access_token, token_type
    
    def authorize_granted(self, library_id):
        login_url = "https://oauth.overdrive.com/auth?client_id={}&redirect_uri={}&scope=accountId:{}&response_type=code&state={}".format(self.key, self.redirect_uri, library_id, 0)
        webbrowser.open(login_url) 

        return access_token, token_type

    def authorize_patron(self, username, password, website_id):
        """
            Performs OAuth for Checkout/Hold API

            Returns:
                access_token : Access token used in all further requests
                token_type : Type of token (Bearer)
        """
        auth_endpoint = "https://oauth-patron.overdrive.com/patrontoken"
        key_secret = self.key + ":" + self.secret
        auth_string = base64.b64encode(key_secret.encode("utf-8"))

        headers = {
            'Authorization': "Basic {}".format(auth_string.decode("utf-8")),
            'Host' : "oauth.overdrive.com",
            'Content-Type' : "application/x-www-form-urlencoded;charset=UTF-8"
        }

        body = "grant_type=password&username={}&scope=websiteid:{} authorizationname:default".format(username, password, website_id)

        response = requests.post(auth_endpoint, headers = headers, data = body, verify=False)
        response_json = json.loads(response.content.decode("utf-8"))

        access_token = response_json['access_token']
        token_type = response_json['token_type']

        return access_token, token_type

    def add_library_catalog(self, access_token, token_type, library_id):
        """
            Gets the catalog associated with the given library id and stores it in the library_catalogs dictionary.
        """
        url = self.circulation_api_base_url + "/v1/libraries/{}".format(library_id)

        headers = {
            'User-Agent': self.user_agent,
            'Authorization': "{} {}".format(token_type, access_token),
            'Host' : self.circulation_host_url
        }

        response = requests.get(url, headers=headers, verify=False)
        response_json = json.loads(response.content)
        self.library_catalogs[library_id] = response_json['collectionToken']
        print("Added <{}, {}> to supported libraries".format(library_id, response_json['collectionToken']))

    def search_for_title(self, access_token, token_type, library_id, book):
        """
            Searches for a title in the library_id's catalog.

            Returns:
                None : If the item was not found in the catalog
                response_json : If an item was found in the catalog, returns search results
        """
        print("Searching for book: {} in Library: {}".format(book.to_str(), library_id))
        endpoint = self.circulation_api_base_url + "/v1/collections/{}/products?q={}&limit={}".format(self.library_catalogs[library_id], book.title, 10)
        headers = {
            'User-Agent': self.user_agent,
            'Authorization': "{} {}".format(token_type, access_token),
            'Host' : self.circulation_host_url
        }

        response = requests.get(endpoint, headers=headers, verify=False)
        response_json = json.loads(response.content)

        if response_json['totalItems'] > 0:
            return response_json
        else:
            print("Item was not found in library catalog.")
            return None

    def get_metadata(self, access_token, token_type, book, search_result):
        """
            Gets the metadata for a title from the search_result. Only returns metadata if authors also match.

            Returns:
                None: If the author did not match, returns none
                response_json : metadata response
        """
        for i in range(search_result['totalItems']):
            author = search_result['products'][i]['primaryCreator']['name']
            if book.author in author: # We use in here because author entries might not match
                endpoint = search_result['products'][i]['links']['metadata']['href']
                headers = {
                    'User-Agent': self.user_agent,
                    'Authorization': "{} {}".format(token_type, access_token),
                    'Host' : self.circulation_host_url
                }

                response = requests.get(endpoint, headers=headers, verify=False)
                response_json = json.loads(response.content)
                return response_json
            else:
                print("Found results but authors did not match. ({} != {})".format(author, book.author))
        return None

    def get_item_id(self, access_token, token_type, book, search_result):
        """
            Gets the item_id of a book from search results.

            Returns:
                None: If there were no matching authors
                item_id: The id of the book in the overdrive library
        """
        for i in range(search_result['totalItems']):
            author = search_result['products'][i]['primaryCreator']['name']
            if book.author in author: # We use in here because author entries might not match
                print("Found matching items: {}".format(book.to_str()))
                return search_result['products'][i]['id']
            else:
                print("Found results but authors did not match. ({} != {})".format(author, book.author))
        return None


    def get_availability(self, access_token, token_type, library_id, book, search_result):
        """
            Gets the availibility of a book from search results.

            Returns:
                None: If there were no matching authors
                response_json: The availability json
        """
        print("Getting availabilty for book: {} in Library: {}".format(book.to_str(), library_id))
        for i in range(search_result['totalItems']):
            author = search_result['products'][i]['primaryCreator']['name']
            if book.author in author: # We use in here because author entries might not match
                endpoint = search_result['products'][i]['links']['availability']['href']
                headers = {
                    'User-Agent': self.user_agent,
                    'Authorization': "{} {}".format(token_type, access_token),
                    'Host' : self.circulation_host_url
                }

                response = requests.get(endpoint, headers=headers, verify=False)
                response_json = json.loads(response.content)
                return response_json
            else:
                print("Found results but authors did not match. ({} != {})".format(author, book.author))
        return None

    def place_hold(self, access_token, token_type, item_id, email):
        """
            Places a hold on a specific item.

            Args:
                item_id: The id of the item in the library catalog
                email: Email to send hold notification to
            
            Returns:
                TODO
        """
        endpoint = self.patron_api_base_url + "/v1/patrons/me/holds"
        headers = {
            'User-Agent': self.user_agent,
            'Authorization': "{} {}".format(token_type, access_token),
            'Host' : self.patron_api_host_url,
            'Content-Type' : "application/json; charset=utf-8"
        }

        body = {
            'reserve_id' : item_id,
            'emailAddress' : email
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(body),verify=False)
        print()

    def checkout(self, access_token, token_type, item_id):
        endpoint = self.patron_api_base_url + "/v1/patrons/me/checkouts"
        headers = {
            'User-Agent': self.user_agent,
            'Authorization': "{} {}".format(token_type, access_token),
            'Host' : self.patron_api_host_url,
            'Content-Type' : "application/json; charset=utf-8"
        }

        body = {
            'reserveId' : item_id
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(body), verify=False)
        print()