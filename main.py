#! /usr/bin/env python3

# NEXT: BallotMeasure, Votes
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
    vs.get_current_senators()
    #vs.get_senator_bios()
    vs.get_all_senator_voting_records()
    vs.save_data()

    
def init_vs():
    with open(f'{CONFIG}/keys.json') as f:
        keys = json.load(f)
    votesmart_api_key = keys['votesmart']['APIKey']
    vs = APIHandler(votesmart_api_key)
    return vs


if __name__ == '__main__':
    main()
