import pyupbit
import time
import datetime
import pandas as pd
import requests
import telegram

bot = telegram.Bot(token='5007441586:AAF-TCPvcJbGYVn224m-dvlqgsePkvW_gW8')
chat_id ="849745003"
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
plus_count = 0
total_krw = 300000  #사용할 잔고
call_total_krw = 0
call_1st = "No"
call_2nd = "No"
call_3rd = "No"
# -----------------------------------------------------------------
while True:
    now = datetime.datetime.now()
    upbit_target = price_ma()    
    krw_balance = round(upbit.get_balance("KRW"), 0) #잔고조회
    coin_balance = upbit.get_balance(coin)
    krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
    price = round(pyupbit.get_current_price(coin), 0) #현재가
    call_total_krw_ = krw_call_avg_price * coin_balance
    #====================================================================================================
    #Setting Value
    call_KRW_1st = total_krw * (12.0/100)
    call_KRW_2nd = total_krw * (40.0/100)
    call_KRW_3rd = total_krw * (45.0/100)    
    #====================================================================================================
    # 1st_price_value    
    upbit_target_call_1st = upbit_target - (upbit_target * (0.30/100))    
    upbit_target_call_2nd = upbit_target - (upbit_target * (0.40/100))
    upbit_target_call_3rd = upbit_target - (upbit_target * (0.53/100))

    Gap1st = abs(upbit_target - upbit_target_call_1st)
    Gap2nd = abs(upbit_target - upbit_target_call_2nd)
    Gap3rd = abs(upbit_target - upbit_target_call_3rd)
    #====================================================================================================    
    # - sell value
    upbit_target_down = krw_call_avg_price - (krw_call_avg_price * (1.5/100))
    #====================================================================================================
    # + sell value
    upbit_target_plus_up = krw_call_avg_price + (krw_call_avg_price * (0.65/100))
    #====================================================================================================        
    # 1st_price_value 
    if price is not None and call_count == 1 and price < upbit_target and price < upbit_target_call_1st:
        upbit.buy_market_order(coin, call_KRW_1st) #20% 시장가 주문
        time.sleep(0.5) #1sec wait
        call_1st = "Cell OK"
        call_count = 2
        sell_count = 1
        plus_count = 1
        #telegram-------------------------------------------------
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
        call_total_krw_ = krw_call_avg_price * coin_balance
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d %H:%M:%S'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (-3.0%) : {0:,.0f}".format(price))        
        bot.sendMessage(chat_id=chat_id, text="매수금액_1st (15%) : {0:,.0f}".format(call_KRW_1st))        
        bot.sendMessage(chat_id=chat_id, text="매수금액(누적) : {0:,.0f}".format(call_total_krw_))

    # 2nd_price_value 
    if price is not None and call_count == 2 and price < upbit_target and price < upbit_target_call_2nd:
        upbit.buy_market_order(coin, call_KRW_2nd) #35%
        time.sleep(0.5) #1sec wait        
        call_2nd = "Cell OK"
        call_count = 3
        sell_count = 1
        plus_count = 1
        #telegram-------------------------------------------------
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
        call_total_krw_ = krw_call_avg_price * coin_balance
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d %H:%M:%S'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (-3.8%): {0:,.0f}".format(price))        
        bot.sendMessage(chat_id=chat_id, text="매수금액_2nd (40%) : {0:,.0f}".format(call_KRW_2nd))
        bot.sendMessage(chat_id=chat_id, text="매수금액(누적) : {0:,.0f}".format(call_total_krw_))

    # 3rd_price_value 
    if price is not None and call_count == 3 and price < upbit_target and price < upbit_target_call_3rd:
        upbit.buy_market_order(coin, call_KRW_3rd) #45%
        time.sleep(0.5) #1sec wait
        call_3rd = "Cell OK"
        sell_count = 1
        plus_count = 1
        #telegram-------------------------------------------------
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
        call_total_krw_ = krw_call_avg_price * coin_balance
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d %H:%M:%S'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (-5.6%): {0:,.0f}".format(price))        
        bot.sendMessage(chat_id=chat_id, text="매수금액_3rd (45%) : {0:,.0f}".format(call_KRW_3rd))
        bot.sendMessage(chat_id=chat_id, text="매수금액(누적) : {0:,.0f}".format(call_total_krw_))

    # - sell (손절)
    if sell_count == 1 and price < upbit_target and price < upbit_target_down:        
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)        
        sell_total_krw_ = krw_call_avg_price * coin_balance
        upbit.sell_market_order(coin, coin_balance)
        call_count = 1
        sell_count = 0
        plus_count = 0
        call_total_krw = 0
        #telegram-------------------------------------------------        
        _sell_krw_ = sell_total_krw_ - call_total_krw_
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d %H:%M:%S'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (-1.5%): {0:,.0f}".format(price))
        bot.sendMessage(chat_id=chat_id, text="손절코인수량 : {0:,.0f}".format(coin_balance))
        bot.sendMessage(chat_id=chat_id, text="손절금액 : {0:,.0f}".format(sell_total_krw_))
        bot.sendMessage(chat_id=chat_id, text="손실금액 : {0:,.0f}".format(_sell_krw_))
        #telegram-------------------------------------------------
        time.sleep(10800) #3Hr wait
        #if now.hour > 8 and now.hour < 18:
        #    time.sleep(3600) #60min wait
        #else:
        #    time.sleep(3600) #60min wait

    # + sell (익절)
    if plus_count == 1 and price > upbit_target and price > upbit_target_plus_up:
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
        plus_sell_total_krw_ = krw_call_avg_price * coin_balance
        upbit.sell_market_order(coin, coin_balance)
        call_count = 1
        plus_count = 0
        call_total_krw = 0
        #telegram-------------------------------------------------        
        _plus_krw_ = call_total_krw_ - sell_total_krw_
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d %H:%M:%S'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (+6.0%): {0:,.0f}".format(price))
        bot.sendMessage(chat_id=chat_id, text="익절코인수량 : {0:,.0f}".format(coin_balance))
        bot.sendMessage(chat_id=chat_id, text="익절금액 : {0:,.0f}".format(plus_sell_total_krw_))
        bot.sendMessage(chat_id=chat_id, text="수익금액 : {0:,.0f}".format(_plus_krw_))
        #telegram-------------------------------------------------
        
    print(f"=========================================================")
    print(now.strftime('▶ Time: %y/%m/%d %H:%M:%S'))    
    print("▶ MA20: {0:,.0f}".format(upbit_target))
    print("▶ price : {0:,.0f}".format(price))
    print(f"---------------------------------------------------------")
    print("▶ call_count: {0:,.0f}".format(call_count))    
    print("▶ call Target 1st : {0:,.0f}".format(upbit_target_call_1st), "▶ Gap 1st : {0:,.0f}".format(Gap1st), "▶ ", call_1st)
    print("▶ call Target 2nd : {0:,.0f}".format(upbit_target_call_2nd), "▶ Gap 2nd : {0:,.0f}".format(Gap2nd), "▶ ", call_2nd)
    print("▶ call Target 3rd : {0:,.0f}".format(upbit_target_call_3rd), "▶ Gap 3rd : {0:,.0f}".format(Gap3rd), "▶ ", call_3rd)
    print(f"---------------------------------------------------------")    
    print("▶ - sell 1st : {0:,.0f}".format(upbit_target_down))
    print(f"---------------------------------------------------------")    
    print("▶ plus sell 1st : {0:,.0f}".format(upbit_target_plus_up))
    print(f"---------------------------------------------------------")    
    print("▶ Coin Total : {0:,.5f}".format(coin_balance), "▶ Coin Price Avg : {0:,.0f}".format(krw_call_avg_price)) #코인수량/평단가
    print(f"---------------------------------------------------------")
    print("▶ Coin Total KRW : {0:,.0f}".format(call_total_krw_))  #코인 매수 합계
    print("▶ Jango KRW : {0:,.0f}".format(krw_balance))  #계좌 잔고

    time.sleep(3)
