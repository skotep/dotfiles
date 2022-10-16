import cbpro
import pandas as pd

def get_client():
    # ...
    return cbpro.AuthenticatedClient(key, secret, passphrase)

def balances(client):
    act = [a for a in client.get_accounts() if float(a['balance']) > 0]
    for a in act:
        cur = a['currency']
        a['balance'] = float(a['balance'])
        if cur == 'USD' or cur == 'USDC':
            a['price'] = 1.0
            a['dlr'] = a['balance']
            continue
        pp = client.get_product_ticker(product_id=f'{cur}-USD')
        if pp.get('message') == 'NotFound':
            pp = client.get_product_ticker(product_id=f'{cur}-USDC')
        if 'price' not in pp:
            import pdb;pdb.set_trace()
        a['price'] = float(pp['price'])
        a['dlr'] = a['price'] * a['balance']
    return client.get_time(), act

def display():
    c = get_client()
    t, bal = balances(c)
    df = pd.DataFrame(bal)
    df['time'] = pd.Timestamp(t['epoch'], unit='s')
    df = df[['time','currency','balance','price','dlr']]
    old = pd.read_csv('data.csv')
    pd.concat([old, df]).to_csv('data.csv', index=False)
    #df.to_csv('data.csv', index=False)


if __name__ == '__main__':
    display()
