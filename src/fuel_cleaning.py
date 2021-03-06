# -*- coding: utf-8 -*-
"""fuel_cleaning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jqHXZt8llGZN9n22luU_UcvQWD2v8tan
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime
from datetime import datetime as dt


df = pd.read_csv('../data/fuel_unclean.csv')
df.head()

# filling in the missing values for the price with the median from a 10 day window around the missing day

date = np.array(df['Date'])
price = np.array(df['Jet Fuel Spot Price'])
price_list = price.tolist()

# plt.plot(price)

start_date = datetime.datetime(2020, 1, 22)
end_date = datetime.datetime(2021, 4, 3)
delta = datetime.timedelta(days=1)

date_formatted = []
for x in date:
  date_format = dt.strptime(x, "%m/%d/%Y")
  date_formatted.append(date_format)

  

  # np.insert(date_formatted, dt.strptime(date, "%M/%d/%Y"))

while start_date <= end_date:
    if start_date not in date_formatted:
      index = np.searchsorted(date_formatted, start_date, side='right')
      # np.insert(date, index, start_date)
      date_formatted.insert(index, start_date)
      median = np.median(price_list[index-2:index+2])
      price_list.insert(index, median)
    start_date += delta
  
price_list.pop()
date_formatted.pop()
print(len(date_formatted))
print(len(price_list))

plt.plot(price_list)
plt.show()

# apply tukeys rule for removing outliers

import statistics

def tukey(price_list):
  month_price_list = []
  # lst1 = price_list[i:i+30] for i in range(0,len(df)-30+1,30)]
  for i in range(0,len(price_list)-30+1,30):
    month_price_list.append(price_list[i:i+30])
  month_price_list.append(price_list[420:])
  price_list_tukey = []
  for month in month_price_list:
    median = statistics.median(month)
    month_sorted = np.sort(month)
    q25 = month_sorted[math.ceil((25/100)*len(month))-1]
    q75 = month_sorted[math.ceil((75/100)*len(month))-1]
    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off
    numchanges = 0
    for i, x in enumerate(month):
        if x < lower or x > upper:
            month[i] = median
            numchanges += 1
    print("outliers = ", numchanges)
    price_list_tukey.extend(month)
    # plt.plot(price_list_tukey)
  return price_list_tukey


price_list = tukey(price_list)
plt.plot(price_list)
plt.show()

dict = {'Date': date_formatted, 'Price': price_list}         
df1 = pd.DataFrame(dict)

df1.to_csv('../data/fuel_clean.csv')

df = pd.read_csv('../data/fuel_clean.csv')
df.head()

#plt.plot(df['Date'], df['Price'])
#plt.xticks(np.arange(df['Date'][0]), max(x)+1, 1.0))

#print(type(df['Date'][0]))

