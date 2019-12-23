import json

from votesmart import APIHandler


def main():
    vs = init_vs()
    vs.get_current_senators()
    
def init_vs():
    with open('config/keys.json') as f:
        keys = json.load(f)
    votesmart_api_key = keys['votesmart']['APIKey']
    vs = APIHandler(votesmart_api_key)
    return vs


if __name__ == '__main__':
    main()
