from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import yfinance as yf
from forex_python.converter import CurrencyRates
import re

'''
FinancePy - key_ratios.py
Author: David Joohoon Kim
Description: Calculates earnings per share, book value per share, return on invested capital, and price to earnings ratio  of equities.
'''

apple_url='https://financials.morningstar.com/ratios/r.html?t=AAPL#tab-profitability'
gm_url='https://financials.morningstar.com/ratios/r.html?t=GM#tab-profitability'
enb_url='https://financials.morningstar.com/ratios/r.html?t=ENB#tab-profitability'
mg_url='https://financials.morningstar.com/ratios/r.html?t=MGA#tab-profitability'

c = CurrencyRates()

def simple_get(url):
    try:
        with closing(get(url,stream=True)) as resp:
            if is_good_response(resp):
                return render_page(url)
            else:
                return None

    except RequestException as e:
        log_error('Error during requests {0} : {1}'.format(url,str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return( (resp.status_code==200) and \
            (content_type is not None) and \
            (content_type.find('html') > -1) )

def log_error(e):
    print(e)

def render_page(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(5)
    r=driver.page_source
    driver.quit()
    return r

def displayRatios(html,sign):
    pe = []
    pe_curr = 0                                         #USD Default
    bv_curr = 0                                         #USD Default
    not_complete=False
    for p in html.select('tr'):
        for i, th in enumerate(p.select('th')):
            if(th.text=='Book Value Per Share * USD'):
                for j, td in enumerate(p.select('td')):
                    book_value_TTM = float(td.text)
            if(th.text=='Book Value Per Share * CAD'):
                for j, td in enumerate(p.select('td')):
                    book_value_TTM = float(td.text)
                    bv_curr=1
            if(th.text=='Earnings Per Share USD'):
                for j, td in enumerate(p.select('td')):
                    pe.append(float(td.text))
            if(th.text=='Earnings Per Share CAD'):
                for j, td in enumerate(p.select('td')):
                    pe.append(float(td.text))
                    pe_curr=1
            if(th.text=='Return on Invested Capital %'):
                for j, td in enumerate(p.select('td')):
                    if(bool(re.search(r'\d', td.text))):
                        ROIC = (float(td.text))
                    else:
                        not_complete=True
    pe_val = calc_PEValue(pe,15,pe_curr,sign)
    calc_BookValue(book_value_TTM,1.5,bv_curr,sign)
    calc_PEValue(pe,20,pe_curr,sign)
    bv_val = calc_BookValue(book_value_TTM,2.5,bv_curr,sign)
    if(not_complete):
        ROIC=0
    else:
        calc_ROIC(ROIC)
    avg = (pe_val+bv_val)/2
    results = [avg,ROIC]
    return results

def get_Val(value, curr, sign):
    if(curr != sign):
        if(sign):
            return value*c.get_rate('USD','CAD')
        else:
            return value*c.get_rate('CAD','USD')
    return value

def calc_PEValue(x,mult,curr,sign):
    avg = (x[len(x)-2]+x[len(x)-3]+x[len(x)-4])/3.0
    val = get_Val(avg*mult,curr,sign)
    if(sign):
        print("\tShare Price based on PE Ratio using {}: %.2f".format(mult) %val+" CAD")
    else:
        print("\tShare Price based on PE Ratio using {}: %.2f".format(mult) %val+" USD")
    return val

def calc_BookValue(x,mult,curr,sign):
    val = get_Val(x*mult,curr,sign)
    print("\tShare Price based on Book Value using {}: %.2f".format(mult) %val)
    return val

def calc_ROIC(x):
    print("\tROIC Value is %.2f" %x +"%.")

def getStockPrice(ticker):
    data = yf.Ticker(ticker)
    price = data.info.get("regularMarketOpen","")
    return price

def run_Analysis(comp, url,ticker):
    print("ANALYSIS FOR "+comp)
    raw_html = simple_get(url)
    soup = BeautifulSoup(raw_html,"html.parser")
    sp = getStockPrice(ticker)
    if(ticker[len(ticker)-3]=='.'):
        results = displayRatios(soup,1)
        print("\tCurrent SP is %.2f" %sp+" CAD")
    else:
        results = displayRatios(soup,0)
        print("\tCurrent SP is %.2f" %sp+" USD")
    avg = results[0]
    print("---COMPLETE---")


if __name__=='__main__':
    run_Analysis("APPLE INC.", apple_url,'AAPL')
    run_Analysis("GENERAL MOTORS",gm_url,'GM')
    run_Analysis("ENBRIDGE",enb_url,'ENB.TO')
    run_Analysis("MAGNA INTERNATIONAL",mg_url,'MG.TO')
