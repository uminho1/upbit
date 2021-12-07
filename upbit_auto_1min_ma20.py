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
    target_10_call_1st = target_10 - (target_10 * (0.4/100))
    target_10_call_1st_gap = price - target_10_call_1st
    target_10_call_ = ((price / target_10) * 100) - 100

    target_10_call_2nd = target_10 - (target_10 * (0.65/100))
    target_10_call_3rd = target_10 - (target_10 * (1.0/100))
    target_10_call_4th = target_10 - (target_10 * (5.5/100))
    #====================================================================================================    
    # - sell value
    target_10 = target_10
    target_10_down = krw_call_price - (krw_call_price * (1.5/100))
    if target_10_down == 0:
        target_10_down_gap = krw_call_price * (1.5/100)
    else:    
        target_10_down_gap = krw_call_price * (1.5/100)
        target_10_down_ = abs(100 - ((price / krw_call_price) * 100))
    #====================================================================================================
    # + sell value
    target_10_up_1st = krw_call_price + (krw_call_price * (0.45/100))
    target_10_up_2nd = krw_call_price + (krw_call_price * (0.85/100))
    if target_10_up_1st == 0:
        target_10_up_1st_gap = 0
    else:    
        target_10_up_1st_gap = krw_call_price - price
        target_10_up_ = abs(100 - ((price / krw_call_price) * 100))
    #====================================================================================================
        
    # 1st_price_value 
    if price is not None and count == 1 and price < target_10 and price < target_10_call_1st:
        krw_balance = upbit.get_balance("KRW")               
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, krw_balance * (1.0/100))
        count = 2

    # 2nd_price_value 
    if price is not None and count == 2 and price < target_10 and price < target_10_call_2nd:
        krw_balance = upbit.get_balance("KRW")        
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, krw_balance * (10.0/100))
        count = 3

    # 3rd_price_value 
    if price is not None and count == 3 and price < target_10 and price < target_10_call_3rd:
        krw_balance = upbit.get_balance("KRW")        
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, krw_balance * (15.0/100))        
        count = 3        

    # - sell value
    if count <=3 and price < target_10 and price < target_10_down:   
        btc_balance = upbit.get_balance(coin)        
        krw_balance = upbit.get_balance("KRW")        
        sell_now = datetime.datetime.now()
        upbit.sell_market_order(coin, btc_balance * (0.5/100))        
        count = 4
        time.sleep(300000) #5min wait

    # 4th_price_value 
    if price is not None and count == 4 and price < target_10 and price < target_10_call_4th:
        krw_balance = upbit.get_balance("KRW")        
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, krw_balance * (15.0/100))
        count = 1

    # + sell value 1st
    if krw_call_price > 1 and price > target_10 and price > target_10_up_1st:
        btc_balance = upbit.get_balance(coin)
        upbit.sell_market_order(coin, btc_balance * (30.0/100))
        krw_balance = upbit.get_balance("KRW")

    # + sell value 2nd
    if krw_call_price > 1 and price > target_10 and price > target_10_up_2nd:
        btc_balance = upbit.get_balance(coin)
        upbit.sell_market_order(coin, btc_balance)
        krw_balance = upbit.get_balance("KRW")
        #sell_price1 = pyupbit.get_current_price(coin)
        #sell_now = datetime.datetime.now()
        count = 1

    print(f"=========================================================")
    print(now.strftime('▶ Time: %y/%m/%d %H:%M:%S'))
    print("▶ count: {0:,.0f}".format(count)) 
    print("▶ MA20: {0:,.0f}".format(target_10))
    print("▶ price : {0:,.0f}".format(price))
    print("▶ price MA Gap : {0:,.0f}".format(price_gap))

    print(f"---------------------------------------------------------")        
    print("▶ call Target 1st : {0:,.0f}".format(target_10_call_1st))
    print("▶ call Gap : {0:,.0f}".format(target_10_call_1st_gap))
    print("▶ call Gap % : {0:,.2f}".format(target_10_call_))    
    print("▶ call Target 2nd : {0:,.0f}".format(target_10_call_2nd))    
    print("▶ call Target 3rd : {0:,.0f}".format(target_10_call_3rd))    
    print("▶ call Target 4th : {0:,.0f}".format(target_10_call_4th))

    print(f"---------------------------------------------------------")    
    print("▶ - sell : {0:,.0f}".format(target_10_down))
    if target_10_down == 0:
        print("▶ - sell Gap : {0:,.0f}".format(target_10_down_gap))
    else:
        print("▶ - sell Gap : {0:,.0f}".format(target_10_down_gap))
        print("▶ - sell Gap % : {0:,.2f}".format(target_10_down_))
    
    print(f"---------------------------------------------------------")
    print("▶ + sell 1st : {0:,.0f}".format(target_10_up_1st))
    print("▶ + sell 2nd : {0:,.0f}".format(target_10_up_2nd))
    if target_10_up_1st == 0:
        print("▶ + sell 1st Gap : {0:,.0f}".format(target_10_up_1st_gap))
    else:        
        print("▶ + sell 1st Gap : {0:,.0f}".format(target_10_up_1st_gap))
        print("▶ + sell 1st Gap % : {0:,.2f}".format(target_10_up_))
    print(f"---------------------------------------------------------")
    print("▶ Price Avg : {0:,.0f}".format(krw_call_price))
    print("▶ Upbit KRW : {0:,.0f}".format(krw_balance))

    time.sleep(3)
