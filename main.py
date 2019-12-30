#! /usr/bin/env python3

# TODO:
# NEXT: Unpack senator bios -> to DF; merge; APIClass Super
from datetime import datetime
import json
from pprint import pprint

from votesmart import APIHandler


DATA = 'data'
CONFIG = 'config'
DATE = datetime.now()
YEAR = DATE.year


def main():
    vs = init_vs()
    senators_df = vs.get_current_senators('df')
    print(senators_df.head())
    print('Saving senator data...')
    senators_df.to_csv(f'{DATA}/senators_{YEAR}.csv', index=False)
    senator_bios = vs.get_senator_bios()
    print(senator_bios)

    
def init_vs():
    with open(f'{CONFIG}/keys.json') as f:
        keys = json.load(f)
    votesmart_api_key = keys['votesmart']['APIKey']
    vs = APIHandler(votesmart_api_key)
    return vs


if __name__ == '__main__':
    main()
