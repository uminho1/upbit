import pyupbit
import requests
import pandas as pd
import time
import webbrowser
import telegram
import datetime
import numpy as np

#자동매매 설정부분
#========================================================================
access = "nehpcdrsANEdzmeHeWY5MVEElxY4Exl4Y5HymcsH"
secret = "pH5hvBYyC2wvchkGTyz8gYYGsBvSgv0ZGFMPh66Z"
upbit =  pyupbit.Upbit(access, secret)

bot = telegram.Bot(token='5007441586:AAF-TCPvcJbGYVn224m-dvlqgsePkvW_gW8')
chat_id ="849745003"

coin = "KRW-BTC"

#매수에 사용할 금액
Total_KRW = 200000
Call_KRW_1st = Total_KRW * (10.0/100)
Call_KRW_2nd = Total_KRW * (35.0/100)
Call_KRW_3rd = Total_KRW * (55.0/100)

bay_no = 1
sell_no = 1
#========================================================================
#실시간 매매
while True:
    url = "https://api.upbit.com/v1/candles/minutes/5"  
    querystring = {"market":coin,"count":"150"}    
    response = requests.request("GET", url, params=querystring)    
    data = response.json()    
    df = pd.DataFrame(data)    
    series=df['trade_price'].iloc[::-1]
    df=df.iloc[::-1]
    df=df['trade_price']
    #------------------------------------------------------------------------
    #직전봉 거래량 구하기
    inho_df = pyupbit.get_ohlcv(ticker=coin, interval='minute5', count=10)
    after_volume = inho_df['volume'].iloc[-1]      #현재봉거래량    
    before_volume = inho_df['volume'].iloc[-2]     #직전봉거래량
    before_volume_new = before_volume * 3

    after_close = inho_df['close'].iloc[-1]      #현재봉가격    
    before_close = inho_df['close'].iloc[-2]     #직전봉종가
    before_close_new = before_close - (before_close * 0.008)  #급락신호
    before_close_new_temp = before_close * 0.008  #급락신호
    #------------------------------------------------------------------------
    #MACD
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    signal = macd.ewm(span=9, adjust=False).mean()

    macd_gap = macd[0] - signal[0]
    #------------------------------------------------------------------------
    #stochrsiRSI
    period=14
    smoothK=3
    smoothD=3
     
    delta = series.diff().dropna()
    ups = delta * 0
    downs = ups.copy()
    ups[delta > 0] = delta[delta > 0]
    downs[delta < 0] = -delta[delta < 0]
    ups[ups.index[period-1]] = np.mean( ups[:period] )
    ups = ups.drop(ups.index[:(period-1)])
    downs[downs.index[period-1]] = np.mean( downs[:period] )
    downs = downs.drop(downs.index[:(period-1)])
    rs = ups.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() / \
         downs.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() 
    rsi = 100 - 100 / (1 + rs)

    stochrsi  = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
    stochrsi_K = stochrsi.rolling(smoothK).mean()
    stochrsi_D = stochrsi_K.rolling(smoothD).mean()  
    
    stochrsiRSI_K = int(stochrsi_K.iloc[-1]*100)
    stochrsiRSI_D = int(stochrsi_D.iloc[-1]*100)
    #------------------------------------------------------------------------
    coin_price = pyupbit.get_current_price(coin) #코인현재가
    jango = upbit.get_balance("KRW") #계좌잔고
    coin_jango = upbit.get_balance(coin) #코인매수수량    
    coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
    coin_total_krw = coin_avg_price * coin_jango #매수한금액
    time_min = time.strftime('%M%S', time.localtime(time.time()))
    time_hore = time.strftime('%H%M%S', time.localtime(time.time()))
    #매도에 사용할 금액    
    Sell_1st = coin_jango * (40.0/100)
    Sell_2nd = coin_jango * (60.0/100)
    #------------------------------------------------------------------------

    print('실시간MACD: ', '{0:,.0f}'.format(macd[0]))
    print('실시간Signal: ', '{0:,.0f}'.format(signal[0]))    
    print('매매신호값: ', '{0:,.0f}'.format(macd_gap))
    print('------------------------------------------')
    print('stoch_rsi_K: ', '{0:,.2f}'.format(stochrsi_K.iloc[-1]*100))
    print('stoch_rsi_D: ', '{0:,.2f}'.format(stochrsi_D.iloc[-1]*100))
    print('------------------------------------------')
    print('직전봉거래량 * 3: ', '{0:,.0f}'.format(before_volume_new))
    print('현재봉거래량: ', '{0:,.0f}'.format(after_volume))
    print('직전봉종가: ', '{0:,.0f}'.format(before_close))
    print('직전봉종가 * 0.07%: ', '{0:,.0f}'.format(before_close_new))
    print('직전봉종가(Gap): ', '{0:,.0f}'.format(before_close_new_temp))    
    print('현재봉가격: ', '{0:,.0f}'.format(after_close))
    print('------------------------------------------')
    print('코인현재가: {0:,.0f}'.format(coin_price))
    print('보유자산:', '{0:,.0f}'.format(jango))
    print('현재분초:', time_min)
    print('------------------------------------------')
    
    if coin_jango == 0 and jango > 6000 and int(stochrsiRSI_K) > 0 and int(macd[0]) < -250000 and -8000 < int(macd_gap) > 8000:
        upbit.buy_market_order(coin, Call_KRW_1st)
        coin_jango = upbit.get_balance(coin) #코인매수수량
        coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
        coin_total_krw = coin_avg_price * coin_jango #매수한금액
        
        bot.sendMessage(chat_id=chat_id, text='■ 1차매수알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="stochRSI_K : {0:,.2f}".format(stochrsi_K.iloc[-1]*100))
        bot.sendMessage(chat_id=chat_id, text='코인매수한금액: {0:,.0f}'.format(coin_total_krw))        
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text="--------------")
        bot.sendMessage(chat_id=chat_id, text="직전봉거래량 * 3: {0:,.0f}".format(before_volume_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉거래량: {0:,.0f}".format(after_volume))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가: {0:,.0f}".format(before_close))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가 * 0.07%: {0:,.0f}".format(before_close_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉가격: {0:,.0f}".format(after_close))
        bay_no = 2
        sell_no = 1

    if bay_no == 2 and int(stochrsiRSI_K) > 0 and int(macd[0]) < -300000 and -8000 < int(macd_gap) > 8000:
        upbit.buy_market_order(coin, Call_KRW_2nd)
        coin_jango = upbit.get_balance(coin) #코인매수수량    
        coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
        coin_total_krw = coin_avg_price * coin_jango #매수한금액

        bot.sendMessage(chat_id=chat_id, text='■ 2차매수알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="stochRSI_K : {0:,.2f}".format(stochrsi_K.iloc[-1]*100))
        bot.sendMessage(chat_id=chat_id, text='코인매수한금액: {0:,.0f}'.format(coin_total_krw))
        bot.sendMessage(chat_id=chat_id, text="--------------")
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text="직전봉거래량 * 3: {0:,.0f}".format(before_volume_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉거래량: {0:,.0f}".format(after_volume))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가: {0:,.0f}".format(before_close))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가 * 0.07%: {0:,.0f}".format(before_close_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉가격: {0:,.0f}".format(after_close))
        bay_no = 3
        sell_no = 1

    if bay_no == 3 and int(stochrsiRSI_K) > 0 and int(macd[0]) < -350000 and -8000 < int(macd_gap) > 8000:
        upbit.buy_market_order(coin, Call_KRW_3rd)
        coin_jango = upbit.get_balance(coin) #코인매수수량    
        coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
        coin_total_krw = coin_avg_price * coin_jango #매수한금액

        bot.sendMessage(chat_id=chat_id, text='■ 3차매수알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="stochRSI_K : {0:,.2f}".format(stochrsi_K.iloc[-1]*100))
        bot.sendMessage(chat_id=chat_id, text='코인매수한금액: {0:,.0f}'.format(coin_total_krw))
        bot.sendMessage(chat_id=chat_id, text="--------------")
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text="직전봉거래량 * 3: {0:,.0f}".format(before_volume_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉거래량: {0:,.0f}".format(after_volume))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가: {0:,.0f}".format(before_close))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가 * 0.07%: {0:,.0f}".format(before_close_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉가격: {0:,.0f}".format(after_close))
        bay_no = "end"
        sell_no = 1    
    
    elif sell_no == 1 and coin_price > coin_avg_price and coin_total_krw > 1 and int(stochrsiRSI_K) > 0 and int(macd[0]) > 200000 and int(macd_gap) > 50000:
        bot.sendMessage(chat_id=chat_id, text='■ 1차매도알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="stochRSI_K : {0:,.2f}".format(stochrsi_K.iloc[-1]*100))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text='코인매도가: {0:,.0f}'.format(coin_price))
        bot.sendMessage(chat_id=chat_id, text="--------------")        
        upbit.sell_market_order(coin, Sell_1st)
        sell_no = 2

    elif sell_no == 2 and coin_price > coin_avg_price and coin_total_krw > 1 and int(stochrsiRSI_K) > 0 and int(macd[0]) > 250000 and int(macd_gap) > 80000:
        bot.sendMessage(chat_id=chat_id, text='■ 2차매도알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="stochRSI_K : {0:,.2f}".format(stochrsi_K.iloc[-1]*100))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text='코인매도가: {0:,.0f}'.format(coin_price))
        bot.sendMessage(chat_id=chat_id, text="--------------")        
        upbit.sell_market_order(coin, Sell_2nd)
        sell_no = "end"

    elif coin_total_krw > 1 and coin_price < before_close_new and after_volume > before_volume_new:
        bot.sendMessage(chat_id=chat_id, text='■급락매도알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="stochRSI_K : {0:,.2f}".format(stochrsi_K.iloc[-1]*100))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text='코인매도가: {0:,.0f}'.format(coin_price))
        bot.sendMessage(chat_id=chat_id, text="--------------")
        bot.sendMessage(chat_id=chat_id, text="직전봉거래량 * 3: {0:,.0f}".format(before_volume_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉거래량: {0:,.0f}".format(after_volume))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가: {0:,.0f}".format(before_close))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가 * 0.07%: {0:,.0f}".format(before_close_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉가격: {0:,.0f}".format(after_close))
        bot.sendMessage(chat_id=chat_id, text="전량 매도후 30분 매매대기합니다.")
        upbit.sell_market_order(coin, coin_jango)
        time.sleep(18000) #5시간 wait

    else:
        print('■ 매매대기중')        
        print('------------------------------------------')
    
    #매시간 정각에 텔레그램 보내기
    if time_min > "0000" and time_min < "0015":
        bot.sendMessage(chat_id=chat_id, text='■ 매시간 알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="stochRSI_K : {0:,.2f}".format(stochrsi_K.iloc[-1]*100))
        bot.sendMessage(chat_id=chat_id, text="현재가격: {0:,.0f}".format(coin_price))

    if time_hore > "091000" and time_hore < "091015":
        bot.sendMessage(chat_id=chat_id, text='■ 매매조건알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="stochRSI_K : {0:,.2f}".format(stochrsi_K.iloc[-1]*100))
        bot.sendMessage(chat_id=chat_id, text="현재가격: {0:,.0f}".format(coin_price))
        bot.sendMessage(chat_id=chat_id, text='MACD값이 -250,000이하 and MACD_Gap값이 -8,000 ~ 8,000이면 1차매수')
        bot.sendMessage(chat_id=chat_id, text='MACD값이 -300,000이하 and MACD_Gap값이 -8,000 ~ 8,000이면 2차매수')
        bot.sendMessage(chat_id=chat_id, text='MACD값이 -350,000이하 and MACD_Gap값이 -8,000 ~ 8,000이면 3차매수')
        bot.sendMessage(chat_id=chat_id, text='MACD값이 +200,000이상 and MACD_Gap값이 50,000이상이면 1차매도')
        bot.sendMessage(chat_id=chat_id, text='MACD값이 +250,000이상 and MACD_Gap값이 80,000이상이면 2차매도')
    
    time.sleep(10)
