from forex_python.converter import CurrencyRates
from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
import yahoofinancials
from yahoofinancials import YahooFinancials
import datetime
import numpy as np
import matplotlib.pyplot as plt

'''
FinancePy
Author: David Joohoon Kim
Description: Calculates theoretical return rate based on periodic dollar cost averaging of equities.
Parameters:
    The start and end date where investments are made.
    The investment amount at each period.
'''

# Default dates 
start_year = 2010
start_month = 10
start_day = 1
end_year = 2019
end_month = 10
end_day = 1

colors =['blue','red','green','orange']
counter = 0

def getInfoBiWeekly(ticker,start_dt,end_dt):
    yahoo_financials = YahooFinancials(ticker)
    my_investment = 0

    print("Investment Type: Bi-Weekly")
    print("Range of investment date",start_dt," to ",end_dt)
    data = yahoo_financials.get_historical_price_data(start_date=start_dt,
                                                      end_date=end_dt,
                                                      time_interval='weekly')
    print("Ticker is: ", ticker)
    counter = 0
    count=0
    total=0
    final=0
    index=0
    for i in data[ticker].get('prices'):
        if not(index%2):
            my_investment += 500
            count+=1
            avg=( (i.get('high')+i.get('low')) / 2)
            total+=avg
            final=avg
        index+=1

    dca = total/count
    print("\tCurrent price = $",final)
    print("\tDollar cost avg = $",'%.2f'%dca)
    print("\tNumber of payments = ",count)
    print("\tMy invested amount = $",my_investment)
    print("\tMy return percentage = ",'%.2f'%(((final-dca)/dca)*100),"%")
    print("\tMy return rate = $",'%.2f'%(my_investment*((final-dca)/dca)))

def getInfoMonthly(ticker,start_dt,end_dt,ax):
    global counter
    yahoo_financials = YahooFinancials(ticker)
    my_investment = 0

    print("Investmenet Type: Monthly")
    print("Range of investment date",start_dt," to ",end_dt)
    data = yahoo_financials.get_historical_price_data(start_date=start_dt,
                                                      end_date=end_dt,
                                                      time_interval='monthly')
    print("Ticker is: ", ticker)
    counter = 0
    count=0
    total=0
    final=0

    date_list = []
    total_list = []
    dates = np.array(date_list)
    totals = np.array(total_list)
    print(data)
    total_shares = 0
    for i in data[ticker].get('prices'):
        my_investment += 500
        count+=1
        avg=( (i.get('high')+i.get('low')) / 2)
        total+=avg
        final=avg
        num_shares =500/avg
        total_shares+=num_shares
        current_equity = total_shares*avg

        dates = np.append(dates, i.get('date'))
        totals = np.append(totals, current_equity)

    ax.plot(dates, totals, color=colors[counter])
    counter +=1

    dca = total/count
    print("\tCurrent price = $",final)
    print("\tDollar cost avg = $",'%.2f'%dca)
    print("\tNumber of payments = ",count)
    print("\tMy invested amount = $",my_investment)
    print("\tMy return percentage = ",'%.2f'%(((final-dca)/dca)*100),"%")
    print("\tMy return rate = $",'%.2f'%(my_investment*((final-dca)/dca)))

fig, ax = plt.subplots()
while(True):
    t = input("Enter ticker symbol: ")
    start_date = input("Enter start date (Y-m-d): ")
    end_date = input("Enter end date (Y-m-d): ")

    for i in range(1):
        if(not(start_date) or not(end_date)):
            ds = datetime.date(start_year,start_month,start_day).strftime("%Y-%m-%d")
            de = datetime.date(end_year,start_month,start_day).strftime("%Y-%m-%d")
        else:
            ds = start_date
            de = end_date
        if(not(t)):
            t = "VFV.TO"
        # getInfoBiWeekly(t,ds,de)
        getInfoMonthly(t,ds,de,ax)

    ax.set(xlabel='Time (s)', ylabel='Total ($)',
       title='Investment Total by Time')
    ax.grid()

    fig.savefig("investment.png")
