import requests
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class SalesforceConfig:
    client_id: str
    client_secret: str
    instance_url: str

class SalesforceConnector:
    def __init__(self, config: SalesforceConfig):
        self.config = config
        self.session = self._authenticate()
        
    def _authenticate(self):
        """OAuth2 authentication flow"""
        auth_url = f"{self.config.instance_url}/services/oauth2/token"
        response = requests.post(auth_url, data={
            'grant_type': 'client_credentials',
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret
        })
        response.raise_for_status()
        return response.json()['access_token']
    
    def get_accounts(self, modified_since: str = None) -> List[Dict]:
        """Retrieve accounts with optional filtering"""
        endpoint = f"{self.config.instance_url}/services/data/v50.0/query?q=SELECT+Id,+Name+FROM+Account"
        if modified_since:
            endpoint += f"+WHERE+LastModifiedDate+>+{modified_since}"
        return self._make_request(endpoint)

    def _make_request(self, url: str) -> Dict:
        response = requests.get(url, headers={
            'Authorization': f'Bearer {self.session}'
        })
        response.raise_for_status()
        return response.json()
