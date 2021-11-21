import pyupbit
import time
import datetime
import pandas as pd
import requests
import pandas as pd
import webbrowser
import numpy as np

def price_ma():
    url = "https://api.upbit.com/v1/candles/minutes/10"    
    querystring = {"market":"KRW-ETH","count":"100"}    
    response = requests.request("GET", url, params=querystring)    
    data = response.json()    
    df = pd.DataFrame(data)    
    df=df['trade_price'].iloc[::-1]
    ma15 = df.rolling(window=15).mean()
    ma20 = df.rolling(window=20).mean()

    ma15_ = round(ma15.iloc[-1], 2)
    ma20_ = round(ma20.iloc[-1], 2)    
    return ma20_


# 객체 생성
access = "nehpcdrsANEdzmeHeWY5MVEElxY4Exl4Y5HymcsH"
secret = "pH5hvBYyC2wvchkGTyz8gYYGsBvSgv0ZGFMPh66Z"
upbit =  pyupbit.Upbit(access, secret)

#변수 생성
target_20 = price_ma()                                                  # 목표가
op_mode = True                                                          # 거래 가능 상태  
hold = False                                                            # 코인 보유 상태
count = 1
sell_price1 = pyupbit.get_current_price("KRW-ETH") * 0.0015              # 2차 매수 목표가격 갱신 (매도가격 * 0.05) + 매도가격   / 1차는 현재가 매수 조건입니다.
sell_price2 = pyupbit.get_current_price("KRW-ETH") + sell_price1

while True:
    now = datetime.datetime.now()
    krw_balance = round(upbit.get_balance("KRW"), 0)                                  # 잔고확인    
    krw_call_price = round(upbit.get_avg_buy_price("KRW-ETH"), 0)                     # 매수금액    
    price = round(pyupbit.get_current_price("KRW-ETH"), 0)                            # 현재가격    
    price_gap = price - target_20                                                     # 현재가격과 목표가의 차이
    
    #====================================================================================================
    target_20 = price_ma()                                                            # MA20 
    target_20_call = target_20 - (target_20 * 0.008)                                  # 매수 목표가 (MA20보다 0.008 하락시 매수)
    target_20_call_gap = target_20 * 0.008                                            # 매수 목표가 Gap
    #====================================================================================================
    #====================================================================================================
    target_20 = price_ma()                                                            # MA20 
    target_20_down = target_20 - (target_20 * 0.007)                                  # 손절 MA20 목표가
    target_20_down_gap = target_20 * 0.007                                            # 손절 MA20 목표가 Gap    
    #====================================================================================================    
    #====================================================================================================    
    target_20_up = krw_call_price + (krw_call_price * 0.015)                          # 익절 목표가
    target_20_up_gap = krw_call_price * 0.05                                          # 익절 목표가 Gap     
    #====================================================================================================
        
    # [매수] 조건 시도 (현재가격이 10분봉 MA20보다 낮고, 매수목표가보다 낮으면 매수)
    if price is not None and price < target_20 and price < target_20_call:
        krw_balance = upbit.get_balance("KRW")                                        # 잔고확인 
        upbit.buy_market_order("KRW-ETH", krw_balance)                                # 원화잔고 전체로 시장가로 매수 krw_balance * 0.5 <-- 50%만 매수
        call_now = datetime.datetime.now()                                            # 매수시간  
    
    # [손절] 현재가격이 10분봉 MA20선 아래에 있고, 그리고 MA20선보다 0.005% 하락한 가격이면 손절
    if price < target_20 and price <= target_20_down:   
        btc_balance = upbit.get_balance("KRW-ETH")                                        # 잔고확인
        upbit.sell_market_order("KRW-ETH", btc_balance)                                   # 시장가 매도
        krw_balance = upbit.get_balance("KRW")                                            # 매도후 잔고확인
        sell_price1 = pyupbit.get_current_price("KRW-ETH")                                # 매도한 가격
        sell_now = datetime.datetime.now()                                                # 매도한 시간        

    # [익절] 현재가격이 10분봉 MA20선 위에 있고, 매수가 보다 수익 1.5%이면 익절
    if price > target_20 and price >= target_20_up:   
        btc_balance = upbit.get_balance("KRW-ETH")                                        # 잔고확인
        upbit.sell_market_order("KRW-ETH", btc_balance)                                   # 시장가 매도
        krw_balance = upbit.get_balance("KRW")                                            # 매도후 잔고확인
        sell_price1 = pyupbit.get_current_price("KRW-ETH")                                # 매도한 가격
        sell_now = datetime.datetime.now()                                                # 매도한 시간            

    print(f"---------------------------------------------------------")
    print(now.strftime('▶ 시간: %y/%m/%d %H:%M:%S'))
    print("▶ MA20: {0:,.0f}".format(target_20))
    print("▶ price (현재가): {0:,.0f}".format(price))
    print("▶ price MA Gap (MA차이): {0:,.0f}".format(price_gap))
    print("▶ - sell(손절가격): {0:,.0f}".format(target_20_down))
    print("▶ - sell Gap (손절가격Gap): {0:,.0f}".format(target_20_down_gap))
    print("▶ + sell (익절가격1.5%): {0:,.0f}".format(target_20_up))
    print("▶ sell Gap (익절가격Gap): {0:,.0f}".format(target_20_up_gap))
    print("▶ call Target (매수목표가): {0:,.0f}".format(target_20_call))
    print("▶ call Gap (매수목표가Gap): {0:,.0f}".format(target_20_call_gap))
    print("▶ call Price (매수한금액): {0:,.0f}".format(krw_call_price))
    print("▶ Upbit KRW (잔고현황): {0:,.0f}".format(krw_balance))
    print(f"---------------------------------------------------------")
    print(f"---------------------------------------------------------")
    
    time.sleep(30)
