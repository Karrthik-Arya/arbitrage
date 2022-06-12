#from click import option
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import pandas as pd
#from selenium.webdriver.chrome.options import Options
#from bs4 import BeautifulSoup
import requests

#options = Options()
#options.headless=True
#driver_path = './chromedriver1'
#driver = webdriver.Chrome(options = options, executable_path = driver_path)
#driver.get('https://www.coinbase.com/price')

def find_the_trades():
    #Scraping CoinBase*
    coinbase_url = 'https://api.coinbase.com/v2/exchange-rates?currency=INR'
    response = requests.get(coinbase_url).json()
    #print(response)
    data = pd.DataFrame()
    for coin in response['data']['rates'].keys():
        base = coin
        price = response['data']['rates'][base]
        if(float(price)!=0):
            price = 1/float(price)
        data = data.append({'base':base, 'coinbase_price':float(price)},ignore_index=True)



    #Scraping Binance
    """
    binance_url = "https://www.binance.com/api/v3/ticker/price"
    response = requests.get(binance_url).json()
    bin_data=pd.DataFrame()
    for pair in response:
        if(pair['symbol'][-3:]=='BTC'):
            bin_data=bin_data.append({'base':pair['symbol'][:-3], 'binance_price':1/float(pair['price'])},ignore_index=True)
        elif (pair['symbol'][:3]=='BTC'):
           bin_data=bin_data.append({'base':pair['symbol'][3:], 'binance_price':float(pair['price'])}, ignore_index=True)
    """


    #Scraping Wazirx
    wazir_url = "https://api.wazirx.com/sapi/v1/tickers/24hr"
    response = requests.get(wazir_url).json()
    waz_data= pd.DataFrame()
    for ticker in response:
        if(ticker['quoteAsset'] == "inr"):
            waz_data=waz_data.append({'base':ticker['baseAsset'].upper(), 'wazirx_price':float(ticker['lastPrice'])}, ignore_index=True)

    #Scraping coindcx
    coindcx_url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(coindcx_url).json()
    dcx_data= pd.DataFrame()
    for ticker in response:
        if(ticker['market'][-3:] == "INR"):
            dcx_data=dcx_data.append({'base':ticker['market'][:-3], 'coindcx_price':float(ticker['last_price'])}, ignore_index=True)

    trades = pd.DataFrame()

    data=pd.merge(data, waz_data, on='base')
    data = pd.merge(data, dcx_data, on='base')
    data['diff_cb_wx']=abs(data['coinbase_price']-data['wazirx_price'])/((data['coinbase_price']+data['wazirx_price'])/2)
    data['diff_cb_cd']=abs(data['coinbase_price']-data['coindcx_price'])/((data['coinbase_price']+data['coindcx_price'])/2)

    for id in data.index:
        base = data['base'][id]
        cb_wx = data['diff_cb_wx'][id]
        cb_cd = data['diff_cb_cd'][id]
        if (cb_wx>cb_cd):
            trade = 'coinbase and wazirx'
            diff = cb_wx
        else:
            trade = 'coinbase and coindcx'
            diff = cb_cd
        trades =trades.append({'base':base, 'trade':trade, 'diff(in%)':100*diff}, ignore_index=True)

    needed = trades.sort_values('diff(in%)', ascending=False)
    return needed[:10]
