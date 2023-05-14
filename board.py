import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import datetime, time
from matplotlib import rcParams

rcParams['figure.autolayout'] = True

def convert_time(x):
    return datetime.datetime.fromtimestamp(x).strftime('%m-%d-%Y %H:%M:%S')

fig = plt.figure()
ax = fig.add_subplot(111)
fig.tight_layout()

data = pd.read_csv('BTC-USD.csv')

close = data['Close'].values[::-1].tolist()
dates = data['Time'].values[::-1].tolist()
x = range(len(close))

ax.plot(x, close, color='red')
ax.set_xticks(range(len(dates)))
ax.set_xticklabels([convert_time(j) if i % 250 == 0 or i == 0 or i == len(dates) - 1 else '' for i, j in enumerate(dates)], rotation=45)
ax.set_xlabel('Time')
ax.set_ylabel('Bitcoins Price')
plt.show()