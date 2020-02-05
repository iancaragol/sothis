import requests
import os
import json
import base64

class OverDrive():
    def __init__(self):
        self.key = self.get_key()
        self.secret = self.get_secret()
        self.library_catalogs = {}
        self.user_agent = "Sothis"
        self.circulation_host_url = "integration.api.overdrive.com"

    def get_key(self):
        with open(os.getcwd() + "\\controllers\\secrets\\overdrive_key.txt") as f:
            key = f.readline().strip()
            return key

    def get_secret(self):
        with open(os.getcwd() + "\\controllers\\secrets\\overdrive_secret.txt") as f:
            secret = f.readline().strip()
            return secret

    def authorize(self, library_id):
        auth_endpoint = "https://oauth.overdrive.com/token"
        key_secret = self.key + ":" + self.secret
        auth_string = base64.b64encode(key_secret.encode("utf-8"))

        headers = {
            'Authorization': "Basic {}".format(auth_string.decode("utf-8")),
            'Host' : "oauth.overdrive.com",
            'Content-Type' : "application/x-www-form-urlencoded;charset=UTF-8"
        }

        body = "grant_type=client_credentials"

        response = requests.post(auth_endpoint, headers = headers, data = body)
        response_json = json.loads(response.content.decode("utf-8"))

        access_token = response_json['access_token']
        token_type = response_json['token_type']

        return access_token, token_type


    def add_library_catalog(self, access_token, token_type, library_id):
        url = "https://api.overdrive.com/v1/libraries/{}".format(library_id)

        headers = {
            'User-Agent': self.user_agent,
            'Authorization': "{} {}".format(token_type, access_token),
            'Host' : self.circulation_host_url
        }

        response = requests.get(url, headers=headers)
        response_json = json.loads(response.content)
        self.library_catalogs[library_id] = response.json['products']
        print("Added <{}, {}> to supported libraries".format(library_id, response.json['products']))

    def check_availability(self, isbn):
        return False