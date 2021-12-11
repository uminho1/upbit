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
total_krw = 300000  #사용할 잔고
call_total_krw = 0
# -----------------------------------------------------------------
while True:
    now = datetime.datetime.now()
    upbit_target = price_ma()    
    krw_balance = round(upbit.get_balance("KRW"), 0) #잔고조회
    coin_balance = upbit.get_balance(coin)
    krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
    price = round(pyupbit.get_current_price(coin), 0) #현재가
    #====================================================================================================
    #Setting Value
    call_KRW_1st = total_krw * (7.0/100)
    call_KRW_2nd = total_krw * (45.0/100)
    call_KRW_3rd = total_krw * (48/100)
    recall_KRW_4th = total_krw * (30.0/100)
    #====================================================================================================
    # 1st_price_value    
    upbit_target_call_1st = upbit_target - (upbit_target * (0.35/100))    
    upbit_target_call_2nd = upbit_target - (upbit_target * (0.50/100))
    upbit_target_call_3rd = upbit_target - (upbit_target * (0.65/100))

    Gap1st = abs(upbit_target - upbit_target_call_1st)
    Gap2nd = abs(upbit_target - upbit_target_call_2nd)
    Gap3rd = abs(upbit_target - upbit_target_call_3rd)
    #====================================================================================================    
    # - sell value
    upbit_target_down = krw_call_avg_price - (krw_call_avg_price * (1.5/100))
    #====================================================================================================
    # + sell value
    upbit_target_plusup = krw_call_avg_price + (krw_call_avg_price * (0.60/100))
    #====================================================================================================        
    # 1st_price_value 
    if price is not None and call_count == 1 and price < upbit_target and price < upbit_target_call_1st:
        krw_balance = upbit.get_balance("KRW")               
        time.sleep(1000) #1sec wait
        upbit.buy_market_order(coin, call_KRW_1st * 0.9995) #7% 시장가 주문
        call_total_krw = call_total_krw + call_KRW_1st
        call_count = 2

    # 2nd_price_value 
    if price is not None and call_count == 2 and price < upbit_target and price < upbit_target_call_2nd:
        krw_balance = upbit.get_balance("KRW")
        time.sleep(1000) #1sec wait
        upbit.buy_market_order(coin, call_KRW_2nd * 0.9995) #45%
        call_total_krw = call_total_krw + call_KRW_2nd
        call_count = 3

    # 3rd_price_value 
    if price is not None and call_count == 3 and price < upbit_target and price < upbit_target_call_3rd:
        krw_balance = upbit.get_balance("KRW")        
        time.sleep(1000) #1sec wait
        upbit.buy_market_order(coin, call_KRW_3rd * 0.9995) #48%
        call_total_krw = call_total_krw + call_KRW_3rd

    # - sell (손절)
    if krw_call_avg_price > 1 and price < upbit_target_down:        
        coin_balance = upbit.get_balance(coin)
        upbit.sell_market_order(coin, coin_balance)
        call_count = 1
        call_total_krw = 0
        time.sleep(360000) #60min wait

    # + sell (익절)
    if krw_call_avg_price > 1 and price > upbit_target and price > upbit_target_plusup:
        coin_balance = upbit.get_balance(coin)
        upbit.sell_market_order(coin, coin_balance)
        call_count = 1
        call_total_krw = 0

    print(f"=========================================================")
    print(now.strftime('▶ Time: %y/%m/%d %H:%M:%S'))    
    print("▶ MA20: {0:,.0f}".format(upbit_target))
    print("▶ price : {0:,.0f}".format(price))
    print(f"---------------------------------------------------------")
    print("▶ call_count: {0:,.0f}".format(call_count))    
    print("▶ call Target 1st : {0:,.0f}".format(upbit_target_call_1st), "▶ Gap 1st : {0:,.0f}".format(Gap1st))
    print("▶ call Target 2nd : {0:,.0f}".format(upbit_target_call_2nd), "▶ Gap 2nd : {0:,.0f}".format(Gap2nd))
    print("▶ call Target 3rd : {0:,.0f}".format(upbit_target_call_3rd), "▶ Gap 3rd : {0:,.0f}".format(Gap3rd))
    print("▶ recall_count: {0:,.0f}".format(recall_count))

    print(f"---------------------------------------------------------")
    print("▶ sell_count: {0:,.0f}".format(sell_count)) 
    print("▶ - sell 1st : {0:,.0f}".format(upbit_target_down))
    print(f"---------------------------------------------------------")
    print("▶ plus_sell_count: {0:,.0f}".format(plus_sell_count)) 
    print("▶ plus sell 1st : {0:,.0f}".format(upbit_target_plusup))
    print(f"---------------------------------------------------------")
    print("▶ Coin Price Avg : {0:,.0f}".format(krw_call_avg_price))  #코인 매수 평단가
    print("▶ Coin Total KRW : {0:,.0f}".format(coin_balance))  #코인 매수 합계
    print(f"---------------------------------------------------------")
    print("▶ Coin Total KRW : {0:,.0f}".format(call_total_krw))  #코인 매수 합계
    print("▶ Jango KRW : {0:,.0f}".format(krw_balance))  #계좌 잔고

    time.sleep(3)
