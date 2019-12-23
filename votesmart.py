'''
TODO
'''

import requests

# officeID values
SENATE_ID = 6
SENATE_TYPE_ID = 'C'


class APIHandler:
    def __init__(self, api_key):
        self._api_key = api_key
        self.url = 'http://api.votesmart.org'
        self.params = {'key': self._api_key, 'o': 'JSON'}
        self.Officials = Officials(self.url, self.params)

    # Test
    def get_current_senators(self):
        res = self.Officials.get_by_office_state(SENATE_ID, 'OR')


class Officials:
    def __init__(self, url, params):
        self.url = f'{url}/Officials'
        self.params = params
        
    def get_by_office_state(self, office, state):
        params = self.params
        params.update({'officeId': office, 'stateId': state})
        url = f'{self.url}.getByOfficeState'
        print('url:', url)
        print('params:', params)
        res = requests.get(url, params=params)
        print(res.json())
        return res.json()
