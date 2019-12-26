#! /usr/bin/env python3

# TODO:
# NEXT: CandidateBio.getBio() .getDetailedBio() .getAddlBio() and merge
import json

from votesmart import APIHandler


DATA = 'data'
YEAR = '2019'


def main():
    vs = init_vs()
    senators_df = vs.get_current_senators('df')
    print(senators_df.head())
    print('Saving senator data...')
    senators_df.to_csv(f'{DATA}/senators_{YEAR}.csv', index=False)

    
def init_vs():
    with open('config/keys.json') as f:
        keys = json.load(f)
    votesmart_api_key = keys['votesmart']['APIKey']
    vs = APIHandler(votesmart_api_key)
    return vs


if __name__ == '__main__':
    main()
