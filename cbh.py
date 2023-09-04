import numpy as np
import pandas as pd
import requests as rq
import time, datetime
import json

# Url1 fetches data length
url = 'https://api.exchange.coinbase.com/products/{}/candles?granularity=86400'

# Url2 fetches dataset with given time intervals
url2 = 'https://api.exchange.coinbase.com/products/{}/candles?granularity=86400&start={}&end={}'

# Default ticker Bitcoin/USDollar
ticker = 'BTC-USD'

# Calculates the time length in each batch in seconds
def delta(u):
    resp = rq.get(u.format(ticker)).json()
    dt = resp[0][0] - resp[-1][0]
    return dt

# Converts numeric timestamp to ISO time format to be sent to Coinbase Pro
def timestamp(x, conv='%Y-%m-%dT%H:%M:%SZ'):
    return datetime.datetime.fromtimestamp(x).strftime(conv)


# Batch seconds (Estimated around 8 Months)
dT = delta(url)

# Initial timestamps
t1 = int(time.time())
t0 = t1 - dT

# Number of batches we wish to fetch (approximately)
years = 6

# Holds the data and joins it together
table = []

for t in range(years):
    # Shows how much is left
    print(years - t, ' pulling')

    # Setting ISO Timestamps
    T0, T1 = timestamp(t0), timestamp(t1)
    
    # Building the data table
    table = table + rq.get(url2.format(ticker, T0, T1)).json()

    # Pausing for each second in order to not get kicked out
    time.sleep(1)

    # Subtracting the timestamps
    t0 = t0 - dT
    t1 = t1 - dT

# Creating the data frame with the appropriate columns
dataframe = pd.DataFrame(table, columns=['Time','Low','High','Open','Close','Volume'])

# Changing the Time section to show actual dates instead of numbers
time_values = dataframe['Time'].values
time_values = [timestamp(t, conv='%m-%d-%Y') for t in time_values]
dataframe['Time'] = time_values

print(dataframe)
