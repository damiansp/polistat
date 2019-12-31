'''
TODO
'''

import requests

import pandas as pd


# officeID values
DEV = True
OFFICE_SENATE = 6
SENATE_TYPE_ID = 'C'
STATES = ['CA', 'KY', 'OR'] if DEV else [
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
        self.CandidateBio = CandidateBio(self.url, self.params)

    def get_current_senators(self):
        print('Getting current senator data...')
        #senator_data = []
        for state in STATES:
            res = self.Officials.get_by_office_state(OFFICE_SENATE, state)
        res = {k.replace('candidateList_', ''): v for k,v in res.items()}
        self.senator_data = res
        self.senator_ids = res['candidateId']
        self.senator_df = pd.DataFrame(res)
        print(self.senator_df.head())
        return self.senator_data
        
    def get_senator_bios(self):
        print('Getting senator bios...')
        msg = ('Must obtain Senator IDs using APIHandler.get_current_senators()'
               ' first')
        assert self.senator_ids is not None, msg
        bios = {}
        for senator in self.senator_ids:
            print(f'  for senator with ID: {senator}...')
            bio = self.CandidateBio.get_bio(senator)
            bios[senator] = bio
            detailed_bio = self.CandidateBio.get_detailed_bio(senator)
            bios[senator].update(detailed_bio)
        self.senator_bios = bios
        return bios
     

    def _senator_json_to_df(self):
        dfs = []
        for state in self.senator_data:
            candidates = state['candidateList']['candidate']
            for candidate in candidates:
                df = pd.DataFrame({k: [v] for k, v in candidate.items()})
                dfs.append(df)
        df = pd.concat(dfs)
        return df                                                 

    
# Super class for API Calls
class APIClassHandler:
    def __init__(self, params):
        self.params = params

    def call(self, url, params):
        try:
            res = requests.get(url, params)
            return res.json()
        except BaseException as e:
            print(f'Error obtaining data from {url} with params: '
                  f'{self.params}\n{e}')
            return {}

    def flatten(self, json_obj, prefix='', out={}, ignore=None):
        ignore = ['generalInfo', 'pronunciation', 'shortTitle']
        if type(json_obj) is str:
            if prefix in out:
                out[prefix].append(json_obj)
            else:
                out[prefix] = [json_obj]
        else:
            for k, v in json_obj.items():
                if k in ignore:
                    continue
                k_adj = f'{prefix}_{k}' if prefix else k
                if type(v) in [str, int, float, bool] or v is None:
                    out[k_adj] = v
                elif type(v) is dict:
                    self.flatten(v, k_adj, out)
                elif type(v) is list:
                    if type(v[0]) is str:
                        out[k_adj] = v
                    else:
                        for d in v:
                            for lk, lv in d.items():
                                lk_adj = f'{prefix}_{lk}'
                                if lk_adj in out:
                                    out[lk_adj].append(lv)
                                else:
                                    out[lk_adj] = [lv]
        return out
        

class Officials(APIClassHandler):
    def __init__(self, url, params):
        super().__init__(params)
        self.url = f'{url}/Officials'
        
    def get_by_office_state(self, office, state):
        params = self.params.copy()
        params.update({'officeId': office, 'stateId': state})
        url = f'{self.url}.getByOfficeState'
        res = super().call(url, params)
        flat = super().flatten(res)
        return flat


class CandidateBio(APIClassHandler):
    def __init__(self, url, params):
        super().__init__(params)
        self.url = f'{url}/CandidateBio'
        self.ignore = ['generalInfo', 'pronunciation', 'shortTitle']

    def get_bio(self, candidate_id):
        params = self.params
        params.update({'candidateId': candidate_id})
        url = f'{self.url}.getBio'
        res = super().call(url)
        return super().flatten(res, ignore=self.ignore)
        
    def get_detailed_bio(self, candidate_id):
        params = self.params
        params.update({'candidateId': candidate_id})
        url = f'{self.url}.getDetailedBio'
        res = super().call(url)
        return super().flatten(res, ignore=self.ignore)
