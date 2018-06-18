import requests
from urllib.parse import urljoin
import os

class ApiService:
    def __init__(self, base_url, access_token=None):
        self.base_url = base_url
        self.access_token = access_token
        self.session = requests.Session()

        self.session.headers.update({
            'User-Agent': 'Microservice Demo',
            'Content-Type': 'application/json'
        })

        if access_token:
            self.session.headers.update({
                'Authorization': f'Bearer {access_token}',
            })

    def update_token(self, access_token):
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
        })

    def resource_url(self, resource):
        return urljoin(self.base_url, resource)

    def get(self, resource, params=None):
        response = self.session.get(self.resource_url(resource), params=params)
        response.raise_for_status()
        return response.json()

    def post(self, resource, params=None, data=None):
        response = self.session.post(self.resource_url(resource), params=params, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, resource, params=None, data=None):
        response = self.session.put(self.resource_url(resource), params=params, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, resource, params=None):
        response = self.session.delete(self.resource_url(resource), params=params)
        response.raise_for_status()
        return response.json()