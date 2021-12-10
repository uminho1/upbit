import pyupbit
import time
import datetime
import pandas as pd
import requests
import pandas as pd

# -----------------------------------------------------------------
def price_ma():
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market":coin,"count":"200"}    
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
# -----------------------------------------------------------------
coin = "KRW-ETH"
call_count = 1
sell_count = 0
recall_count = 0
plus_sell_count = 0

total_krw = 50000
call_total_krw = 0
# -----------------------------------------------------------------
while True:
    now = datetime.datetime.now()
    upbit_target = price_ma()    
    krw_balance = round(upbit.get_balance("KRW"), 0)    
    krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
    price = round(pyupbit.get_current_price(coin), 0)
    price_gap = price - upbit_target
    #====================================================================================================
    #Setting Value
    call_KRW_1st = total_krw * (12.0/100)
    call_KRW_2nd = total_krw * (38.0/100)
    call_KRW_3rd = total_krw * (52.0/100)
    recall_KRW_4th = total_krw * (25.0/100)
    
    sell_KRW_1st = total_krw * (0.5/100)
    sell_KRW_2nd = total_krw * (99.5/100)
    
    plus_KRW_1st = call_total_krw * (45.0/100)
    plus_KRW_2nd = call_total_krw * (55.0/100)
    #====================================================================================================
    # 1st_price_value    
    upbit_target_call_1st = upbit_target - (upbit_target * (0.4/100))
    upbit_target_call_1st_gap = price - upbit_target_call_1st
    upbit_target_call_ = ((price / upbit_target) * 100) - 100
    upbit_target_call_2nd = upbit_target - (upbit_target * (0.55/100))
    upbit_target_call_3rd = upbit_target - (upbit_target * (0.75/100))
    #====================================================================================================    
    upbit_target_recall_1th = upbit_target - (upbit_target * (2.5/100))
    #====================================================================================================    
    # - sell value
    upbit_target = upbit_target
    upbit_target_down_1st = krw_call_avg_price - (krw_call_avg_price * (1.5/100))
    upbit_target_down_2nd = krw_call_avg_price - (krw_call_avg_price * (2.0/100))
    if upbit_target_down_1st == 0:
        upbit_target_down_gap = krw_call_avg_price * (1.5/100)
    else:    
        upbit_target_down_gap = krw_call_avg_price * (1.5/100)
        upbit_target_down_ = abs(100 - ((price / krw_call_avg_price) * 100))
    #====================================================================================================
    # + sell value
    upbit_target_up_1st = krw_call_avg_price + (krw_call_avg_price * (0.45/100))
    upbit_target_up_2nd = krw_call_avg_price + (krw_call_avg_price * (0.7/100))
    if upbit_target_up_1st == 0:
        upbit_target_up_1st_gap = 0
    else:
        upbit_target_up_1st_gap = krw_call_avg_price - price
        upbit_target_up_ = abs(100 - ((price / krw_call_avg_price) * 100))
    #====================================================================================================
        
    # 1st_price_value 
    if price is not None and call_count == 1 and price < upbit_target and price < upbit_target_call_1st:
        krw_balance = upbit.get_balance("KRW")               
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, call_KRW_1st) #10%
        call_total_krw = call_KRW_1st
        call_count = 2

    # 2nd_price_value 
    if price is not None and call_count == 2 and price < upbit_target and price < upbit_target_call_2nd:
        krw_balance = upbit.get_balance("KRW")        
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, call_KRW_2nd) #38%
        call_total_krw = call_total_krw + call_KRW_2nd
        call_count = 3

    # 3rd_price_value 
    if price is not None and call_count == 3 and price < upbit_target and price < upbit_target_call_3rd:
        krw_balance = upbit.get_balance("KRW")        
        call_now = datetime.datetime.now()
        upbit.buy_market_order(coin, call_KRW_3rd) #52%
        call_total_krw = call_total_krw + call_KRW_3rd
        call_count = 3

    # - sell 1st
    if call_count <=3 and sell_count == 0 and price < upbit_target and price < upbit_target_down_1st:   
        krw_balance = upbit.get_balance("KRW")
        upbit.sell_market_order(coin, sell_KRW_1st)
        sell_count = 1
        recall_count = 1
        time.sleep(900000) #15min wait

    # - sell 2nd
    if sell_count == 1 and price < upbit_target and price < upbit_target_down_2nd:   
        krw_balance = upbit.get_balance("KRW")
        upbit.sell_market_order(coin, sell_KRW_2nd)        
        recall_count = 1        
        time.sleep(1800000) #30min wait    

    # recall 1th_price
    if recall_count == 1 and price is not None and price < upbit_target and price < upbit_target_recall_1th:                   
        upbit.buy_market_order(coin, recall_KRW_4th)
        call_count = 1
        sell_count = 0
        recall_count = 0
        plus_sell_count = 0

    # + sell 1st
    if plus_sell_count == 0 and krw_call_avg_price > 1 and price > upbit_target and price > upbit_target_up_1st:        
        upbit.sell_market_order(coin, plus_KRW_1st)        
        call_total_krw = call_total_krw - plus_KRW_1st
        call_count = 1
        sell_count = 1
        recall_count = 0
        plus_sell_count = 1

    # + sell 2nd
    if plus_sell_count == 1 and krw_call_avg_price > 1 and price > upbit_target and price > upbit_target_up_2nd:        
        upbit.sell_market_order(coin, plus_KRW_2nd)
        call_total_krw = call_total_krw - plus_KRW_2nd
        call_count = 1
        sell_count = 0
        recall_count = 0
        plus_sell_count = 0

    print(f"=========================================================")
    print(now.strftime('▶ Time: %y/%m/%d %H:%M:%S'))    
    print("▶ MA20: {0:,.0f}".format(upbit_target))
    print("▶ price : {0:,.0f}".format(price))
    print("▶ price MA Gap : {0:,.0f}".format(price_gap))

    print(f"---------------------------------------------------------")
    print("▶ call_count: {0:,.0f}".format(call_count))    
    print("▶ call Target 1st : {0:,.0f}".format(upbit_target_call_1st), "▶ call Gap : {0:,.0f}".format(upbit_target_call_1st_gap), "▶ call Gap % : {0:,.2f}".format(upbit_target_call_))    
    print("▶ call Target 2nd : {0:,.0f}".format(upbit_target_call_2nd))    
    print("▶ call Target 3rd : {0:,.0f}".format(upbit_target_call_3rd))    
    print("▶ call Target 4th : {0:,.0f}".format(upbit_target_recall_1th))
    print("▶ recall_count: {0:,.0f}".format(recall_count))

    print(f"---------------------------------------------------------")
    print("▶ sell_count: {0:,.0f}".format(sell_count)) 
    print("▶ - sell 1st : {0:,.0f}".format(upbit_target_down_1st))
    print("▶ - sell 2nd : {0:,.0f}".format(upbit_target_down_2nd))
    if upbit_target_down_1st == 0:
        print("▶ - sell (1st) Gap : {0:,.0f}".format(upbit_target_down_gap))
    else:
        print("▶ - sell (1st) Gap : {0:,.0f}".format(upbit_target_down_gap), "▶ - sell (1st) Gap % : {0:,.2f}".format(upbit_target_down_))        
    
    print(f"---------------------------------------------------------")
    print("▶ plus_sell_count: {0:,.0f}".format(plus_sell_count)) 
    print("▶ plus sell 1st : {0:,.0f}".format(upbit_target_up_1st), "▶ plus sell KRW 1st : {0:,.0f}".format(plus_KRW_1st))    
    print("▶ plus sell 2nd : {0:,.0f}".format(upbit_target_up_2nd), "▶ plus sell KRW 2nd : {0:,.0f}".format(plus_KRW_2nd))
    if upbit_target_up_1st == 0:
        print("▶ + sell (1st) Gap : {0:,.0f}".format(upbit_target_up_1st_gap))
    else:        
        print("▶ + sell (1st) Gap : {0:,.0f}".format(upbit_target_up_1st_gap), "▶ + sell (1st) Gap % : {0:,.2f}".format(upbit_target_up_))        
    print(f"---------------------------------------------------------")
    print("▶ Call Price Avg : {0:,.0f}".format(krw_call_avg_price))  #매수 평단가
    print("▶ Call_Total_KRW : {0:,.0f}".format(call_total_krw))  #매수 합계
    print("▶ Jango KRW : {0:,.0f}".format(krw_balance))  #잔고

    time.sleep(3)
