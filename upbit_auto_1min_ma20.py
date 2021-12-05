import pyupbit
import time
import datetime
import pandas as pd
import requests
import pandas as pd
# -----------------------------------------------------------------
coin = "KRW-ETH"
count = 1
coinrobot = 1
# -----------------------------------------------------------------
def price_ma():
    url = "https://api.upbit.com/v1/candles/minutes/1"
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
    target_10_call = target_10 - (target_10 * (0.4/100))    
    target_10_call_gap = price - target_10_call
    #====================================================================================================    
    # - sell value
    target_10 = target_10
    target_10_down = krw_call_price - (krw_call_price * (6.0/100))
    target_10_down_gap = krw_call_price * (6.0/100)
    #====================================================================================================
    # + sell value
    target_10_up = krw_call_price + (krw_call_price * (1.0/100))
    if target_10_up == 0:        
        target_10_up_gap = 0
    else:    
        target_10_up_gap = krw_call_price - price        
    #====================================================================================================
        
    # 1st_price_value 
    if coinrobot == 1 and price is not None and count == 1 and price < target_10 and price < target_10_call:
        krw_balance = upbit.get_balance("KRW")
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, krw_balance * (7.0/100))
        call_price1 = pyupbit.get_current_price(coin)
        count = 2
        target_10_call_2nd = call_price1 - (call_price1 * (0.2/100))

    # 2nd_price_value 
    if coinrobot == 1 and price is not None and count == 2 and price < target_10 and price < target_10_call_2nd:
        krw_balance = upbit.get_balance("KRW")
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, krw_balance * (10.0/100))
        call_price2 = pyupbit.get_current_price(coin)
        count = 3
        target_10_call_3rd = call_price2 - (call_price2 * (0.3/100))

    # 3nd_price_value 
    if coinrobot == 1 and price is not None and count == 3 and price < target_10 and price < target_10_call_3rd:
        krw_balance = upbit.get_balance("KRW")
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, krw_balance * (15.0/100))
        call_price3 = pyupbit.get_current_price(coin)

    # - sell value  5% sell
    if coinrobot == 1 and price < target_10 and price < target_10_down:   
        btc_balance = upbit.get_balance(coin)        
        krw_balance = upbit.get_balance("KRW")        
        sell_now = datetime.datetime.now()
        upbit.sell_market_order(coin, btc_balance * (5.0/100))
        price = pyupbit.get_current_price(coin)
        count = 4
        target_10_call_4th = price - (price * (1.5/100))

    # 4th_price_value 
    if coinrobot == 1 and price is not None and count == 4 and price < target_10 and price < target_10_call_4th:
        krw_balance = upbit.get_balance("KRW")        
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, krw_balance * (20.0/100))
        price = round(pyupbit.get_current_price(coin), 0)
        count = 1

    # + sell value
    if coinrobot == 1 and krw_call_price > 1 and price > target_10 and price > target_10_up:   
        btc_balance = upbit.get_balance(coin)
        upbit.sell_market_order(coin, btc_balance)
        krw_balance = upbit.get_balance("KRW")
        sell_price1 = pyupbit.get_current_price(coin)
        sell_now = datetime.datetime.now()
        count = 1

    print(f"=========================================================")
    print(now.strftime('▶ Time: %y/%m/%d %H:%M:%S'))
    print("▶ count: {0:,.0f}".format(count)) 
    print("▶ MA20: {0:,.0f}".format(target_10))
    print("▶ price : {0:,.0f}".format(price))
    print("▶ price MA Gap : {0:,.0f}".format(price_gap))
    print(f"---------------------------------------------------------")    
    print("▶ call Target 1st : {0:,.0f}".format(target_10_call))
    print("▶ call Gap : {0:,.0f}".format(target_10_call_gap))    
    print(f"---------------------------------------------------------")
    print("▶ - sell : {0:,.0f}".format(target_10_down))
    print("▶ - sell Gap : {0:,.0f}".format(target_10_down_gap))
    print(f"---------------------------------------------------------")
    print("▶ + sell : {0:,.0f}".format(target_10_up))
    print("▶ + sell Gap : {0:,.0f}".format(target_10_up_gap))
    print(f"---------------------------------------------------------")
    print("▶ Price Avg : {0:,.0f}".format(krw_call_price))
    print("▶ Upbit KRW : {0:,.0f}".format(krw_balance))

    time.sleep(5)
