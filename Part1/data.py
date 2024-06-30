# data.py
import requests

def fetch_domain_info(domain, api_key):
    url = f'https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        domain_info = {
            'domain': data['data']['domain'],
            'disposable': data['data']['disposable'],
            'webmail': data['data']['webmail'],
            'accept_all': data['data']['accept_all'],
            'pattern': data['data']['pattern'],
            'organization': data['data']['organization'],
            'description': data['data']['description'],
            'industry': data['data']['industry'],
            'twitter': data['data']['twitter'],
            'facebook': data['data']['facebook'],
            'linkedin': data['data']['linkedin'],
            'instagram': data['data']['instagram'],
            'youtube': data['data']['youtube']
        }
        return domain_info
    else:
        print(f"Failed to retrieve domain details. Status code: {response.status_code}")
        return None
