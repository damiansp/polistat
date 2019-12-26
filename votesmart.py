'''
TODO
'''

import requests

import pandas as pd


# officeID values
SENATE_ID = 6
SENATE_TYPE_ID = 'C'
STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
    'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
    'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
    'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
    'WI', 'WY']


class APIHandler:
    def __init__(self, api_key):
        self._api_key = api_key
        self.url = 'http://api.votesmart.org'
        self.params = {'key': self._api_key, 'o': 'JSON'}
        self.Officials = Officials(self.url, self.params)

    def get_current_senators(self, return_type='json'):
        print('Getting current senator data...')
        senator_data = []
        for state in STATES:
            res = self.Officials.get_by_office_state(SENATE_ID, state)
            senator_data.append(res)
        self.senator_data = senator_data
        if return_type == 'json':
            return self.senator_data
        if return_type == 'df':
            df = self._senator_json_to_df()
            return df

    def _senator_json_to_df(self):
        dfs = []
        for state in self.senator_data:
            candidates = state['candidateList']['candidate']
            for candidate in candidates:
                df = pd.DataFrame({k: [v] for k, v in candidate.items()})
                dfs.append(df)
        df = pd.concat(dfs)
        return df
                                                                    


class Officials:
    def __init__(self, url, params):
        self.url = f'{url}/Officials'
        self.params = params
        
    def get_by_office_state(self, office, state):
        params = self.params
        params.update({'officeId': office, 'stateId': state})
        url = f'{self.url}.getByOfficeState'
        res = requests.get(url, params=params)
        return res.json()
