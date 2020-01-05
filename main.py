#! /usr/bin/env python3

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
    senators = vs.get_current_senators()
    senator_bios = vs.get_senator_bios()
    vs.save_data()

    
def init_vs():
    with open(f'{CONFIG}/keys.json') as f:
        keys = json.load(f)
    votesmart_api_key = keys['votesmart']['APIKey']
    vs = APIHandler(votesmart_api_key)
    return vs


if __name__ == '__main__':
    main()
