import pyupbit
import time
import datetime
import pandas as pd
import requests
import pandas as pd
import webbrowser
import numpy as np

# -----------------------------------------------------------------
coin = "KRW-BTC"
count = 1
coinrobot = 1
# -----------------------------------------------------------------
def price_ma():
    url = "https://api.upbit.com/v1/candles/minutes/5"
    querystring = {"market":coin,"count":"100"}
    response = requests.request("GET", url, params=querystring)    
    data = response.json()    
    df = pd.DataFrame(data)    
    df=df['trade_price'].iloc[::-1]    
    ma20 = df.rolling(window=20).mean()    
    ma20_ = round(ma20.iloc[-1], 2)    
    return ma20_
# -----------------------------------------------------------------
access = "nehpcdrsANEdzmeHeWY5MVEElxY4Exl4Y5HymcsH"
secret = "pH5hvBYyC2wvchkGTyz8gYYGsBvSgv0ZGFMPh66Z"
upbit =  pyupbit.Upbit(access, secret)
# -----------------------------------------------------------------

while True:
    now = datetime.datetime.now()
    target_10 = price_ma()
    krw_balance = round(upbit.get_balance("KRW"), 0)
    krw_call_price = round(upbit.get_avg_buy_price(coin), 0)
    price = round(pyupbit.get_current_price(coin), 0)
    price_gap = price - target_10
    
    # 1st_price_value
    target_10 = target_10
    target_10_call = target_10 - (target_10 * 0.006)
    target_10_call_gap = price - target_10_call
    #====================================================================================================    
    # - 6.0% sell value
    target_10 = target_10
    target_10_down = krw_call_price - (krw_call_price * 0.06)
    target_10_down_gap = krw_call_price * 0.06
    #====================================================================================================
    # + 1.8% sell value
    target_10_up = krw_call_price + (krw_call_price * 0.018)
    target_10_up_gap = krw_call_price * 0.018
    #====================================================================================================
        
    # 1st_price_value 
    if coinrobot == 1 and price is not None and count == 1 and price < target_10 and price < target_10_call:
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order(coin, krw_balance * 0.1)
        call_now = datetime.datetime.now()
        price_1st = price
        count = 2
        # 2nd_price_value    
        target_10_call_2nd = price_1st - (price_1st * 0.004)
        target_10_call_2nd__gap = price_1st * 0.002

    # 2nd_price_value 
    if coinrobot == 1 and price is not None and count == 2 and price < target_10 and price < target_10_call_2nd:
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order(coin, krw_balance * 0.2)
        call_now = datetime.datetime.now()
        price_2nd = price
        count = 3
        # 3rd_price_value    
        target_10_call_3rd = price_2nd - (price_2nd * 0.002)
        target_10_call_3rd__gap = price_1st * 0.001

    # 3rd_price_value 
    if coinrobot == 1 and price is not None and count == 3 and price < target_10 and price < target_10_call_3rd:
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order(coin, krw_balance * 0.1)
        call_now = datetime.datetime.now()
        price_3rd = price
      
    # 4th_price_value 
    if coinrobot == 1 and price is not None and count == 4 and price < target_10 and price < target_10_call_4th:
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order(coin, krw_balance)
        call_now = datetime.datetime.now()
        price_4th = price
        count = 1
    
    # - sell value
    if coinrobot == 1 and price < target_10 and price < target_10_down:   
        btc_balance = upbit.get_balance(coin)
        upbit.sell_market_order(coin, btc_balance)
        krw_balance = upbit.get_balance("KRW")
        sell_price1 = pyupbit.get_current_price(coin)
        sell_now = datetime.datetime.now()
        count = 4
        target_10_call_4th = sell_price1 - (price * 0.02)

    # + 1.8% sell value
    if coinrobot == 1 and krw_call_price > 1 and price > target_10 and price > target_10_up:   
        btc_balance = upbit.get_balance(coin)
        upbit.sell_market_order(coin, btc_balance)
        krw_balance = upbit.get_balance("KRW")
        sell_price1 = pyupbit.get_current_price(coin)
        sell_now = datetime.datetime.now()
        count = 1

    print(f"---------------------------------------------------------")
    print(now.strftime('▶ Time: %y/%m/%d %H:%M:%S'))
    print("▶ count: {0:,.0f}".format(count)) 
    print("▶ MA20: {0:,.0f}".format(target_10))
    print("▶ price : {0:,.0f}".format(price))
    print("▶ price MA Gap : {0:,.0f}".format(price_gap))
    print("▶ - sell(6.0%) : {0:,.0f}".format(target_10_down))
    print("▶ - sell Gap : {0:,.0f}".format(target_10_down_gap))
    print("▶ + sell(1.8%) : {0:,.0f}".format(target_10_up))
    print("▶ + sell Gap : {0:,.0f}".format(target_10_up_gap))
    print("▶ call Target 1st (0.07%) : {0:,.0f}".format(target_10_call))
    print("▶ call Gap : {0:,.0f}".format(target_10_call_gap))
    print("▶ Price Avg : {0:,.0f}".format(krw_call_price))    
    print("▶ Upbit KRW : {0:,.0f}".format(krw_balance))   
    
    time.sleep(10)