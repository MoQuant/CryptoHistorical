import requests
import json
import datetime
import time
import pandas as pd

time_a = '%Y-%m-%dT%H:%M:%SZ'
time_b = '%m-%d-%Y %H:%M:%S'

# granularity_list = [60, 300, 900, 3600, 21600, 86400]
url = 'https://api.exchange.coinbase.com/products/{}/candles?granularity={}&start={}&end={}'

ticker = 'BTC-USD'

def fetch(sess, ticker, gran, t0, t1):
    return sess.get(url.format(ticker, gran, t0, t1)).json()

def delta(sess, ticker):
    data = sess.get(f'https://api.exchange.coinbase.com/products/{ticker}/candles?granularity=86400').json()
    return data[0][0] - data[-1][0]

def convert_time(x):
    return datetime.datetime.fromtimestamp(x).strftime(time_a)

session = requests.Session()
dt = delta(session, ticker)

t1 = int(time.time())
t0 = t1 - dt

hold = []
j = 10
for i in range(j):
    print(j - i, ' periods left')
    T0, T1 = convert_time(t0), convert_time(t1)
    hold += fetch(session, ticker, 86400, T0, T1)
    time.sleep(1)
    t1 -= dt 
    t0 -= dt

df = pd.DataFrame(data=hold, columns=['Time','Open','High','Low','Close','Volume'])
df.to_csv(f'{ticker}.csv')