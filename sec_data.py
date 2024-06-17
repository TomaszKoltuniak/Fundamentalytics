import requests
import json
import os.path
import pandas as pd

header = {'User-Agent': 'Fundamentalytics'}

def download_tickers(filename:str='all_tickers.json'):
    url = 'https://www.sec.gov/files/company_tickers.json'
    response = requests.get(url, headers=header)
    with open(filename, 'w') as f:
        json.dump(response.json(), f)

def load_tickers(filename:str='all_tickers.json'):
    if not os.path.isfile(filename):
        download_tickers()
    with open(filename, 'r') as f:
        all_tickers = json.load(f)
    return all_tickers

def get_all_companies():
    raw = load_tickers()
    all_companies = []
    for _, data in raw.items():
        all_companies.append(str(data['ticker'] + ' ' +  data['title'] + ' ' + str(data['cik_str'])))
    return all_companies

def get_company_facts(cik: str):
    if len(cik) < 10:
        cik = (10 - len(cik)) * '0' + cik
    
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
    response = requests.get(url, headers=header).json()
    
    result = {
        'info': {
            'cik': response['cik'],
            'entityName': response['entityName']
        },
        'facts': {
        }
    }

    facts = response['facts']['dei'] | response['facts']['us-gaap']
    
    for k, v in facts.items():
        # date = []
        # value = []
        # for element in v['units'][str(list(v['units'].keys())[0])]:
        #     if 'frame' in list(element.keys()) and element['form'] in ['10-Q', '10-K']:
        #         date.append(str(element['fy']) + ' ' + element['fp'])
        #         value.append(element['val'])

        # temp_df = pd.DataFrame({'date': date, 'value': value})
        # temp_df = temp_df.sort_values(by=['date'])

        df = pd.DataFrame(v['units'][list(v['units'].keys())[0]])

        temp_dict = {
            'label': v['label'],
            'description': v['description'],
            'unit': list(v['units'].keys())[0],
            'data': df
        }
        result['facts'][k] = temp_dict
    del response
    return result