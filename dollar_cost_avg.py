from forex_python.converter import CurrencyRates
from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
import yahoofinancials
from yahoofinancials import YahooFinancials

'''
FinancePy
Author: David Joohoon Kim
Description: Calculates theoretical return rate based on periodic dollar cost averaging of equities.
Parameters:
    The start and end date where investments are made.
    The investment amount at each period.
'''

START_DATE = '2015-05-31'
END_DATE = '2020-05-31'
PERIOD = 'monthly'

c = CurrencyRates()

def getInfo(ticker):
    yahoo_financials = YahooFinancials(ticker)
    my_investment = 0

    data = yahoo_financials.get_historical_price_data(start_date=START_DATE,
                                                      end_date=END_DATE,
                                                      time_interval=PERIOD)
    print("Ticker is: ", ticker)
    counter = 0
    count=0
    total=0
    final=0
    for i in data[ticker].get('prices'):
        if(counter < 18):
            my_investment += 1000
            counter+=1
        else:
            my_investment += 500
        count+=1
        avg=( (i.get('high')+i.get('low')) / 2)
        total+=avg
        final=avg

    dca = total/count
    print("\tCurrent price = $",final)
    print("\tDollar cost avg = $",'%.2f'%dca)
    print("\tMy invested amount = $",my_investment)
    print("\tMy return percentage = ",'%.2f'%((final-dca)/dca),"%")
    print("\tMy return rate = $",'%.2f'%(my_investment*((final-dca)/dca)))

getInfo('VOO')
getInfo('DIA')
getInfo('VFV.TO')
getInfo('XIC.TO')
getInfo('AAPL')
getInfo('MSFT')
getInfo('AMZN')
getInfo('GOOGL')
getInfo('GM')
getInfo('MG.TO')
getInfo('ENB.TO')
getInfo('BMO.TO')
getInfo('BNS.TO')
