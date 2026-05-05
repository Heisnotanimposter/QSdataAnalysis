import requests
import json
import os
from datetime import datetime

# QS 2026 API Endpoint
QS_API_URL = "https://www.topuniversities.com/rankings/endpoint?nid=4061771&page=0&items_per_page=100&tab=indicators"

def fetch_qs_data():
    print("Fetching data from QS API...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(QS_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Failed to fetch QS data: {response.status_code}")
        return []

def sync_data():
    qs_raw = fetch_qs_data()
    if not qs_raw:
        return
    
    # In a real scenario, we would also crawl THE and ARWU here.
    # For now, we update the existing rankings.json with any new QS data found.
    
    output_path = '/Users/seungwonlee/QSdataAnalysis/univrank-app/src/data/rankings.json'
    with open(output_path, 'r') as f:
        existing_data = json.load(f)
    
    # Create lookup for existing universities
    lookup = {u['university_name'].lower(): u for u in existing_data}
    
    updates = 0
    for entry in qs_raw:
        name = entry.get('title', '').replace('</a>', '').split('>')[-1].strip()
        rank = entry.get('rank_display', '').replace('=', '')
        try:
            rank_int = int(rank)
        except:
            continue
            
        if name.lower() in lookup:
            lookup[name.lower()]['qs_rank'] = rank_int
            lookup[name.lower()]['last_updated'] = datetime.now().isoformat()
            updates += 1
            
    with open(output_path, 'w') as f:
        json.dump(existing_data, f, indent=2)
        
    print(f"Data sync complete. Updated {updates} universities.")

if __name__ == "__main__":
    sync_data()
