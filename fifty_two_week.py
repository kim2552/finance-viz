import yfinance as yf
from forex_python.converter import CurrencyRates

'''
FinancePy - fifty_two_week.py
Author: David Joohoon Kim
Description: Calculates the 52 week high and low share price of equities.
Parameters:
    Return the share price at a certain percentage value of the 52 week high and low.
'''

# Default Parameter(s)
PERCENT = 0.9

c = CurrencyRates()

def getInfo(ticker,percent):
    data = yf.Ticker(ticker)
    print(ticker,":")
    price = data.info.get("regularMarketPrice","")
    high_price = data.info.get("fiftyTwoWeekHigh","")
    low_price = data.info.get("fiftyTwoWeekLow","")

    print("\tRegular Market Price $",price)
    print("\t52 Week High $",high_price)
    print("\t",'%.0f'%(percent*100),"% of 52 Week High $",'%.2f'%(high_price*percent))
    print("\t52 Week Low $",low_price)
    print("\t",'%.0f'%(100+((1-percent)*100)),"% of 52 Week Low $",'%.2f'%(low_price*(1+(1-percent))))
    print("\tAverage $",'%.2f'%((high_price+low_price)/2))

#getInfo('VOO',PERCENT)
#getInfo('DIA',PERCENT)
#getInfo('VFV.TO',PERCENT)
#getInfo('XIC.TO',PERCENT)
#getInfo('AAPL',PERCENT)
#getInfo('MSFT',PERCENT)
#getInfo('AMZN',PERCENT)
#getInfo('GOOGL',PERCENT)
#getInfo('GM',PERCENT)
#getInfo('MG.TO',PERCENT)
#getInfo('ENB.TO',PERCENT)
#getInfo('BMO.TO',PERCENT)
#getInfo('BNS.TO',PERCENT)

t = input("Enter ticker symbol: ")
getInfo(t,PERCENT)
