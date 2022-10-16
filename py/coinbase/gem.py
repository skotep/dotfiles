import requests
import json
import base64
import hmac
import hashlib
import datetime, time
import pandas as pd


gemini_api_key = master_key
gemini_api_secret = master_secret.encode()

def wrap(endpoint, extra={}):
    now = datetime.datetime.now()
    payload_nonce =  str(int(time.mktime(now.timetuple())*1000))
    payload =  {"request": f"/v1/{endpoint}", "nonce": payload_nonce, **extra}
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

    request_headers = {
        'Content-Type': "text/plain",
        'Content-Length': "0",
        'X-GEMINI-APIKEY': gemini_api_key,
        'X-GEMINI-PAYLOAD': b64,
        'X-GEMINI-SIGNATURE': signature,
        'Cache-Control': "no-cache"
    }

    url = f"https://api.gemini.com/v1/{endpoint}"
    response = requests.post(url, headers=request_headers)
    response.raise_for_status()
    return response.json()

def update():
    res = wrap('balances/earn', dict(account='primary'))[0]
    now = datetime.datetime.now()
    df = pd.DataFrame.from_records([{
        'time': pd.Timestamp(now, unit='s'),
        'currency': res['currency'],
        'balance': res['balance'],
        }])
    old = pd.read_csv('gem.csv')
    pd.concat([old, df]).to_csv('gem.csv', index=False)

#accounts = wrap('account/list')

if __name__ == '__main__':
    update()
