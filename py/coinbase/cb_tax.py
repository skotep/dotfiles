import datetime
import cbpro
import pandas as pd
from collections import deque
import logging
from cb import get_client

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

def get_all_fills():
    c = get_client()
    fills = pd.DataFrame()
    for p in c.get_products():
        f = c.get_fills(product_id=p['id'])
        df = pd.DataFrame.from_records([ff for ff in f])
        logging.info(f'fetched {len(df)} for {p["id"]}')
        if df.empty:
            continue
        if fills.empty:
            fills = df
        else:
            fills = pd.concat([fills, df])
    filename = f'fills_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
    fills.to_csv(filename, index=False)
    logging.info(f'Wrote to {filename}')

def Trade(buy, sell, remaining):
    qty = min(buy['size'], remaining)
    return dict(
            date_sold=sell['created_at'].date(),
            qty=qty,
            product=sell['product_id'],
            description=f"{qty:.6f} {sell['product_id']}",
            date_acquired=buy['created_at'].date(),
            buy_price=buy['price'],
            sell_price=sell['price'],
            proceeds=qty * sell['price'],
            basis=qty * buy['price'],
            pnl=qty * (sell['price'] - buy['price']),
            wash_sale = '',
            wash_adj = 0,
            )


def compute_trades(df):
    qty = 0
    buys = deque()
    trades = []
    bal = 0
    last_buy = None
    for _, row in df.iterrows():
        logging.debug(f"{bal} {len(buys)} :: {row['created_at']} {row['side']} px={row['price']} q={row['size']} f={row['fee']}")
        if row['side'] == 'buy' and row['size'] > 0:
            if row['size'] >= 4:
                last_buy = row
            buys.append(row)
            bal += row['size']
            # Process through trades
            wash_qty = row['size']
            for t in reversed(trades):
                if t['pnl'] >= 0:
                    continue
                if (row['created_at'].date() - t['date_sold']).days >= 30:
                    break
                t['wash_sale'] = 'W'
                qty = min(t['qty'], wash_qty)
                adj = t['wash_adj'] + qty * t['sell_price']
                t['wash_adj'] = min(adj, t['pnl'])
                t['pnl'] = t['proceeds'] - t['basis'] - t['wash_adj'] 


            # done washing
            continue

        if row['side'] != 'sell' or not row['settled']:
            logging.error("ERROR unknown side")
            import pdb;pdb.set_trace()

        qty = row['size'] 
        while abs(qty) > 1e-9:
            if not buys and row['product_id'] == 'ETH-USD':
                # well, add back the last big buy we saw?
                buys.append(last_buy)
                logging.debug(f"{bal} {len(buys)} :: ADD {row['size']}")
            if not buys:
                import pdb;pdb.set_trace()
            t = Trade(buys[0], row, qty)
            if buys[0]['size'] <= t['qty']:
                buys.popleft()
            else:
                buys[0]['size'] -= t['qty']
            qty -= t['qty']
            bal -= t['qty']
            trades.append(t)
            logging.debug(f'bal: {bal}; buys: {len(buys)}; traded: {t}')

    return trades

def prepare_taxact(filename):
    df = pd.read_csv(filename, parse_dates=['created_at'], usecols=['created_at', 'product_id', 'price', 'size', 'fee',
        'side', 'settled', 'usd_volume'])

    df.loc[df['product_id'] == 'ADA-USDC', 'product_id'] = 'ADA-USD'

    # special case for LTC-BTC
    x = df[df['product_id'] == 'LTC-BTC']
    row = x.iloc[0].copy()
    row['product_id'] = 'BTC-USD'
    row['side'] = 'buy'
    row['size'] = (x['price'] * x['size']).sum()
    row['usd_volume'] = x['usd_volume'].sum()
    row['price'] = row['usd_volume'] / row['size']
#    eth = x.iloc[0].copy()
#    eth['product_id'] = 'ETH-USD'
#    eth['created_at'] = df[df['product_id'] == 'ETH-USD'].created_at.min()
#    eth['side'] = 'buy'
#    eth['size'] = 10.0
#    eth['price'] = 1000
#    eth['usd_volume'] = 1000
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)


    df.sort_values('created_at', inplace=True, ignore_index=True)
    trades = []
    for p in df.product_id.unique():
        if p == 'LTC-BTC':
            continue

        logging.debug('\n')
        logging.debug(f'Processing for {p}')
        trades.extend(compute_trades(df[df['product_id'] == p]))

    logging.info('*'*120)

    ttt = pd.DataFrame(trades)
    ttt['year'] = ttt.date_sold.apply(lambda x: x.year)
    ttt['long_term'] = (ttt['date_sold'] - ttt['date_acquired']).dt.days > 356

    taxes = ttt[ttt['year'] == datetime.datetime.now().year - 1]
    taxes.drop_duplicates(inplace=True)
    filename = f'taxes_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
    taxes.to_csv(filename, index=False, float_format='%.6f')
    logging.info(f'Wrote to {filename}\n')

    agg = taxes.groupby('long_term').sum()[['proceeds', 'basis', 'pnl', 'wash_adj']]
    agg['raw_pnl'] = agg['proceeds'] - agg['basis']
    print(agg.to_string(float_format='%.2f'))

    #import pdb;pdb.set_trace()


if __name__ == '__main__':
    #get_all_fills()
    prepare_taxact('fills_20220402.csv')
