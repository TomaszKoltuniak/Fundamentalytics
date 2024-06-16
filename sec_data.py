import requests
import json

header = {'User-Agent': 'Fundamentalytics'}

def update_tickers(filename:str='all_tickers.json'):
    url = 'https://www.sec.gov/files/company_tickers.json'
    response = requests.get(url, headers=header)
    with open(filename, 'w') as f:
        json.dump(response.json(), f)

def load_tickers(filename:str='all_tickers.json'):
    try:
        with open(filename, 'r') as f:
            all_tickers = json.load(f)
    except:
        update_tickers()
        load_tickers()
    return all_tickers

def show_all_companies():
    raw = load_tickers()
    all_companies = []
    for _, data in raw.items():
        all_companies.append(str(data['ticker'] + ' ' +  data['title'] + ' ' + str(data['cik_str'])))
    return all_companies