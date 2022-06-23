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

def find_the_trades(ex_1, ex_2):
    #Scraping CoinBase
    dbs = []
    if(ex_1=='cb' or  ex_2=='cb'):
        coinbase_url = 'https://api.coinbase.com/v2/exchange-rates?currency=USDT'
        response = requests.get(coinbase_url).json()
        #print(response)
        coinbase_data = pd.DataFrame()
        for coin in response['data']['rates'].keys():
            base = coin
            price = response['data']['rates'][base]
            if(float(price)!=0):
                price = 1/float(price)
            coinbase_data = coinbase_data.append({'base':base, 'coinbase_price':float(price)},ignore_index=True)
        dbs.append(coinbase_data)


    #Scraping KuCoin
    if(ex_1=='kcs' or  ex_2=='kcs'):
        kcs_url = "https://api.kucoin.com/api/v1/market/allTickers"
        response = requests.get(kcs_url).json()
        response = response['data']['ticker']
        kcs_data=pd.DataFrame()
        for pair in response:
            if(pair['symbol'][-4:]=='USDT'):
                kcs_data = kcs_data.append({'base':pair['symbol'][:-5], 'kcs_buy_price':float(pair['buy']), 'kcs_sell_price': float(pair['sell'])},ignore_index=True)
        dbs.append(kcs_data)

    #Scraping Binance
    if(ex_1=='binance' or  ex_2=='binance'):
        binance_url = "https://www.binance.com/api/v3/ticker/bookTicker"
        response = requests.get(binance_url).json()
        bin_data=pd.DataFrame()
        for pair in response:
            if(float(pair['askQty'])==0 or float(pair['bidQty'])==0):
                continue
            if(pair['symbol'][-4:]=='USDT'):
                bin_data=bin_data.append({'base':pair['symbol'][:-4], 'binance_sell_price':float(pair['askPrice']), 'binance_buy_price':float(pair['bidPrice'])},ignore_index=True)
        dbs.append(bin_data)
        print(dbs)



    #Scraping Wazirx
    if(ex_1=='wazirx' or  ex_2=='wazirx'):
        wazir_url = "https://api.wazirx.com/sapi/v1/tickers/24hr"
        response = requests.get(wazir_url).json()
        waz_data= pd.DataFrame()
        for ticker in response:
            if(ticker['quoteAsset'] == "usdt"):
                waz_data=waz_data.append({'base':ticker['baseAsset'].upper(), 'wazirx_buy_price':float(ticker['bidPrice']), 'wazirx_sell_price':float(ticker['askPrice']) }, ignore_index=True)
        dbs.append(waz_data)

    #Scraping coindcx
    if(ex_1=='coindcx' or  ex_2=='coindcx'):
        coindcx_url = "https://api.coindcx.com/exchange/ticker"
        response = requests.get(coindcx_url).json()
        dcx_data= pd.DataFrame()
        for ticker in response:
            if(ticker['market'][-4:] == "USDT"):
                dcx_data=dcx_data.append({'base':ticker['market'][:-4], 'coindcx_buy_price':float(ticker['bid']), 'coindcx_sell_price':float(ticker['ask'])}, ignore_index=True)
        dbs.append(dcx_data)

    trades = pd.DataFrame()

    data = pd.merge(dbs[0], dbs[1], on='base')
    data['diff_'+ex_1+'_'+ex_2]=(data[ex_1+'_buy_price']-data[ex_2+'_sell_price'])/((data[ex_2+'_sell_price']+data[ex_1+'_buy_price'])/2)
    data['diff_'+ex_2+'_'+ex_1]=(data[ex_2+'_buy_price']-data[ex_1+'_sell_price'])/((data[ex_1+'_sell_price']+data[ex_2+'_buy_price'])/2)


    for id in data.index:
        base = data['base'][id]
        if (data['diff_'+ex_1+'_'+ex_2][id]>data['diff_'+ex_2+'_'+ex_1][id]):
            diff = data['diff_'+ex_1+'_'+ex_2][id]
            buy_from = ex_2
            sell_to = ex_1
            buy_price = data[ex_2+'_sell_price'][id]
            sell_price = data[ex_1+'_buy_price'][id]
        else:
            trade = ex_2+ ' and ' +ex_1
            diff = data['diff_'+ex_2+'_'+ex_1][id]
            buy_from = ex_1
            sell_to = ex_2
            buy_price = data[ex_1+'_sell_price'][id]
            sell_price = data[ex_2+'_buy_price'][id]

        trades =trades.append({'base':base, 'buy_from':buy_from,'sell_to':sell_to, 'buy_price':buy_price, 'sell_price':sell_price, 'diff(in%)':100*diff}, ignore_index=True)

    needed = trades.sort_values('diff(in%)', ascending=False)
    return needed[:20].reset_index()
if __name__=="__main__":
    print(find_the_trades())
