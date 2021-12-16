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
coin = "KRW-ETH"     #거래할 코인 설정
total_krw = 300000   #사용할 자금 금액 설정
# -----------------------------------------------------------------
call_count = 1
sell_count = 0
plus_count = 0
call_total_krw = 0
call_1st = "매수대기"
call_2nd = "매수대기"
call_3rd = "매수대기"
call_4st = "매수대기"
# -----------------------------------------------------------------
while True:
    now = datetime.datetime.now()
    upbit_target = price_ma()    
    krw_balance = round(upbit.get_balance("KRW"), 0)             #잔고조회
    coin_balance = upbit.get_balance(coin)
    krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
    price = round(pyupbit.get_current_price(coin), 0)            #현재가
    call_total_krw_ = krw_call_avg_price * coin_balance
    #====================================================================================================
    #Setting Value
    call_KRW_1st = total_krw * (2.0/100)
    call_KRW_2nd = total_krw * (13.0/100)
    call_KRW_3rd = total_krw * (35.0/100)
    call_KRW_4st = total_krw * (50.0/100)
    #====================================================================================================
    # 1st_price_value    
    upbit_target_call_1st = upbit_target - (upbit_target * (0.30/100))    
    upbit_target_call_2nd = upbit_target - (upbit_target * (0.43/100))
    upbit_target_call_3rd = upbit_target - (upbit_target * (0.65/100))
    upbit_target_call_4st = upbit_target - (upbit_target * (0.90/100))

    Gap1st = abs(upbit_target - upbit_target_call_1st)
    Gap2nd = abs(upbit_target_call_1st - upbit_target_call_2nd)
    Gap3rd = abs(upbit_target_call_2nd - upbit_target_call_3rd)
    Gap4st = abs(upbit_target_call_3rd - upbit_target_call_4st)
    #====================================================================================================    
    # - sell value
    upbit_target_down = krw_call_avg_price - (krw_call_avg_price * (1.1/100))
    #====================================================================================================
    # + sell value
    upbit_target_plus_up = krw_call_avg_price + (krw_call_avg_price * (2.9/100))  #익절설정
    upbit_target_plus_up_telegram = krw_call_avg_price + (krw_call_avg_price * (0.7/100))  #익절텔레그램알림
    #====================================================================================================        
    # 1st_price_value 
    if coin_balance == 0 or call_count == 1:
        if price is not None and price < upbit_target and price < upbit_target_call_1st:
            upbit.buy_market_order(coin, call_KRW_1st)
            time.sleep(0.5) #1sec wait
            call_1st = "1차매수 완료"
            call_count = 2
            sell_count = 1
            plus_count = 1
            #telegram-------------------------------------------------
            coin_balance = upbit.get_balance(coin)
            krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
            call_total_krw_ = call_total_krw_ + call_KRW_1st
            krw_balance = round(upbit.get_balance("KRW"), 0) #잔고조회
            bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
            bot.sendMessage(chat_id=chat_id, text="현재가 (-0.28% 하락단가) : {0:,.0f}".format(price))        
            bot.sendMessage(chat_id=chat_id, text="매수금액_1st : {0:,.0f}".format(call_KRW_1st))
            bot.sendMessage(chat_id=chat_id, text="매수코인수량_1st : {0:,.5f}".format(coin_balance))
            bot.sendMessage(chat_id=chat_id, text="매수금액(누적) : {0:,.0f}".format(call_total_krw_))
            bot.sendMessage(chat_id=chat_id, text="계좌잔액 : {0:,.0f}".format(krw_balance))            
            bot.sendMessage(chat_id=chat_id, text="●1차매수단가: {0:,.0f}".format(upbit_target_call_1st))
            bot.sendMessage(chat_id=chat_id, text="●2차매수단가: {0:,.0f}".format(upbit_target_call_2nd))
            bot.sendMessage(chat_id=chat_id, text="●3차매수단가: {0:,.0f}".format(upbit_target_call_3rd))
            bot.sendMessage(chat_id=chat_id, text="●4차매수단가: {0:,.0f}".format(upbit_target_call_4st))
            bot.sendMessage(chat_id=chat_id, text="=============================")

    # 2nd_price_value 
    if price is not None and call_count == 2 and price < upbit_target and price < upbit_target_call_2nd:
        upbit.buy_market_order(coin, call_KRW_2nd)
        time.sleep(0.5) #1sec wait        
        call_2nd = "2차매수 완료"
        call_count = 3
        sell_count = 1
        plus_count = 1
        #telegram-------------------------------------------------
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
        call_total_krw_ = call_total_krw_ + call_KRW_2nd
        krw_balance = round(upbit.get_balance("KRW"), 0) #잔고조회
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (-0.43% 하락단가) : {0:,.0f}".format(price))        
        bot.sendMessage(chat_id=chat_id, text="매수금액_2nd : {0:,.0f}".format(call_KRW_2nd))
        bot.sendMessage(chat_id=chat_id, text="매수코인수량_2nd : {0:,.5f}".format(coin_balance))
        bot.sendMessage(chat_id=chat_id, text="매수금액(누적) : {0:,.0f}".format(call_total_krw_))
        bot.sendMessage(chat_id=chat_id, text="계좌잔액 : {0:,.0f}".format(krw_balance))
        bot.sendMessage(chat_id=chat_id, text="●1차매수단가: {0:,.0f}".format(upbit_target_call_1st))
        bot.sendMessage(chat_id=chat_id, text="●2차매수단가: {0:,.0f}".format(upbit_target_call_2nd))
        bot.sendMessage(chat_id=chat_id, text="●3차매수단가: {0:,.0f}".format(upbit_target_call_3rd))
        bot.sendMessage(chat_id=chat_id, text="●4차매수단가: {0:,.0f}".format(upbit_target_call_4st))
        bot.sendMessage(chat_id=chat_id, text="=============================")

    # 3rd_price_value 
    if price is not None and call_count == 3 and price < upbit_target and price < upbit_target_call_3rd:
        upbit.buy_market_order(coin, call_KRW_3rd)
        time.sleep(0.5) #1sec wait        
        call_2nd = "3차매수 완료"
        call_count = 4
        sell_count = 1
        plus_count = 1
        #telegram-------------------------------------------------
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
        call_total_krw_ = call_total_krw_ + call_KRW_3rd
        krw_balance = round(upbit.get_balance("KRW"), 0) #잔고조회
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (-0.65% 하락단가) : {0:,.0f}".format(price))        
        bot.sendMessage(chat_id=chat_id, text="매수금액_3rd : {0:,.0f}".format(call_KRW_3rd))
        bot.sendMessage(chat_id=chat_id, text="매수코인수량_3rd : {0:,.5f}".format(coin_balance))
        bot.sendMessage(chat_id=chat_id, text="매수금액(누적) : {0:,.0f}".format(call_total_krw_))
        bot.sendMessage(chat_id=chat_id, text="계좌잔액 : {0:,.0f}".format(krw_balance))
        bot.sendMessage(chat_id=chat_id, text="●1차매수단가: {0:,.0f}".format(upbit_target_call_1st))
        bot.sendMessage(chat_id=chat_id, text="●2차매수단가: {0:,.0f}".format(upbit_target_call_2nd))
        bot.sendMessage(chat_id=chat_id, text="●3차매수단가: {0:,.0f}".format(upbit_target_call_3rd))
        bot.sendMessage(chat_id=chat_id, text="●4차매수단가: {0:,.0f}".format(upbit_target_call_4st))
        bot.sendMessage(chat_id=chat_id, text="=============================")

    # 4st_price_value 
    if price is not None and call_count == 4 and price < upbit_target and price < upbit_target_call_4st:
        upbit.buy_market_order(coin, call_KRW_4st)
        time.sleep(0.5) #1sec wait
        call_4st = "4차매수 완료"
        sell_count = 1
        plus_count = 1
        #telegram-------------------------------------------------
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
        call_total_krw_ = call_total_krw_ + call_KRW_4st
        krw_balance = round(upbit.get_balance("KRW"), 0) #잔고조회
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text="현재가(-0.90% 하락단가) : {0:,.0f}".format(price))
        bot.sendMessage(chat_id=chat_id, text="매수금액_4st : {0:,.0f}".format(call_KRW_4st))
        bot.sendMessage(chat_id=chat_id, text="매수코인수량_4st : {0:,.5f}".format(coin_balance))
        bot.sendMessage(chat_id=chat_id, text="매수금액(누적) : {0:,.0f}".format(call_total_krw_))
        bot.sendMessage(chat_id=chat_id, text="계좌잔액 : {0:,.0f}".format(krw_balance))

    # - sell (손절)
    if sell_count == 1 and price < upbit_target and price < upbit_target_down:        
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)
        upbit.sell_market_order(coin, coin_balance)
        call_count = 1
        sell_count = 0
        plus_count = 0
        call_total_krw = 0
        #telegram-------------------------------------------------                
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (-1.1%): {0:,.0f}".format(price))
        bot.sendMessage(chat_id=chat_id, text="손절코인수량 : {0:,.5f}".format(coin_balance))
        #telegram-------------------------------------------------
        time.sleep(3600) #1Hr wait
        price = round(pyupbit.get_current_price(coin), 0) #현재가
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text=" 손절 1시간후 현재가 : {0:,.0f}".format(price))
        time.sleep(3600) #1Hr wait
        price = round(pyupbit.get_current_price(coin), 0) #현재가
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text=" 손절 2시간후 현재가 : {0:,.0f}".format(price))
        time.sleep(3600) #1Hr wait
        price = round(pyupbit.get_current_price(coin), 0) #현재가
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text=" 손절 3시간후 현재가 : {0:,.0f}".format(price))
        bot.sendMessage(chat_id=chat_id, text=" 자동매매 재시작합니다.")        

    # + sell (익절)
    if plus_count == 1 and price > upbit_target and price > upbit_target_plus_up:
        coin_balance = upbit.get_balance(coin)
        krw_call_avg_price = round(upbit.get_avg_buy_price(coin), 0)        
        upbit.sell_market_order(coin, coin_balance)
        call_count = 1
        plus_count = 0
        call_total_krw = 0
        #telegram-------------------------------------------------                
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (+2.9%): {0:,.0f}".format(price))
        bot.sendMessage(chat_id=chat_id, text="익절코인수량 : {0:,.5f}".format(coin_balance))
        #telegram-------------------------------------------------
    
    # 익절시 텔레그램 알림
    if plus_count == 1 and price > upbit_target and price > upbit_target_plus_up_telegram:
        price = round(pyupbit.get_current_price(coin), 0) #현재가
        #telegram-------------------------------------------------                
        bot.sendMessage(chat_id=chat_id, text=now.strftime('■ 거래시간: %y/%m/%d'))
        bot.sendMessage(chat_id=chat_id, text="현재가 (+0.7%) 도달: {0:,.0f}".format(price))
        bot.sendMessage(chat_id=chat_id, text="매수금액(누적) : {0:,.0f}".format(call_total_krw_))
        #telegram-------------------------------------------------
        
        
    print(f"=========================================================")
    print(now.strftime('▶ Time: %y/%m/%d %H:%M:%S'))    
    print("▶ 20일 이동평균선: {0:,.0f}".format(upbit_target))
    print("▶ 현재가 : {0:,.0f}".format(price))
    print(f"---------------------------------------------------------")
    print("▶ call_count: {0:,.0f}".format(call_count))    
    print("▶ call Target 1st : {0:,.0f}".format(upbit_target_call_1st), "▶ Gap 1st : {0:,.0f}".format(Gap1st), "▶ 매수예정금액 : {0:,.0f}".format(call_KRW_1st), "▶", call_1st)
    print("▶ call Target 2nd : {0:,.0f}".format(upbit_target_call_2nd), "▶ Gap 2nd : {0:,.0f}".format(Gap2nd), "▶ 매수예정금액 : {0:,.0f}".format(call_KRW_2nd), "▶", call_2nd)
    print("▶ call Target 3rd : {0:,.0f}".format(upbit_target_call_3rd), "▶ Gap 3rd : {0:,.0f}".format(Gap3rd), "▶ 매수예정금액 : {0:,.0f}".format(call_KRW_3rd), "▶", call_3rd)
    print("▶ call Target 4st : {0:,.0f}".format(upbit_target_call_4st), "▶ Gap 3rd : {0:,.0f}".format(Gap4st), "▶ 매수예정금액 : {0:,.0f}".format(call_KRW_4st), "▶", call_4st)
    print(f"---------------------------------------------------------")    
    print("▶ 손절 예정 단가 : {0:,.0f}".format(upbit_target_down))
    print(f"---------------------------------------------------------")    
    print("▶ 익절 예정 단가 : {0:,.0f}".format(upbit_target_plus_up))
    print(f"---------------------------------------------------------")    
    print("▶ 코인 수량 : {0:,.5f}".format(coin_balance), "▶ 코인 평단가 : {0:,.0f}".format(krw_call_avg_price)) #코인수량/평단가
    print(f"---------------------------------------------------------")
    print("▶ 코인 매수 금액 : {0:,.0f}".format(call_total_krw_))
    print("▶ 계좌잔고 : {0:,.0f}".format(krw_balance))
    print("▶ 사용할 자금 : {0:,.0f}".format(total_krw))

    time.sleep(3)
