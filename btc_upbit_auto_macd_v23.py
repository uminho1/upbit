import pyupbit
import requests
import pandas as pd
import time
#import webbrowser
import telegram
#import datetime
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
Total_KRW = upbit.get_balance("KRW")        #전체계좌잔고
Call_KRW_1st = Total_KRW * (15.0/100)       #1차 매수할금액
Call_KRW_2nd = Total_KRW * (35.0/100)       #2차 매수할금액    
Call_KRW_3rd = Total_KRW * (50.0/100)       #3차 매수할금액
buy_no = 1
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
    #매수에 사용할 금액    
    Total_KRW = upbit.get_balance("KRW")        #전체계좌잔고
    Call_KRW_1st = Total_KRW * (7.0/100)       #1차 매수할금액
    Call_KRW_2nd = Total_KRW * (25.0/100)       #2차 매수할금액
    Call_KRW_3rd = Total_KRW * (68.0/100)       #3차 매수할금액
    #------------------------------------------------------------------------
    #급락대비 직전봉 거래량 구하기
    inho_df = pyupbit.get_ohlcv(ticker=coin, interval='minute5', count=10)
    after_volume = inho_df['volume'].iloc[-1]      #현재봉거래량    
    before_volume = inho_df['volume'].iloc[-2]     #직전봉거래량
    before_volume_new = before_volume * 2.5

    after_close = inho_df['close'].iloc[-1]        #현재봉가격    
    before_close = inho_df['close'].iloc[-2]       #직전봉종가
    before_close_new = before_close - (before_close * 0.010)  #급락신호
    before_close_new_temp = before_close * 0.010              #급락신호
    #------------------------------------------------------------------------
    inho_df2 = pyupbit.get_ohlcv(ticker=coin, interval='minute5', count=144)
    price_12hr_average = int(inho_df2['close'].mean())
    price_12hr_average_gap = after_close - price_12hr_average

    if -650000 < price_12hr_average_gap < 650000:         #이전 12시간동안 변동성이 현재가격에서 -650,000 ~ 650,000인 경우
        macd_buy_1st = -95000
        macd_buy_2nd = -150000
        macd_buy_3rd = -230000
        macd_buy_gap = -20000
        #--------------------------------
        macd_sell_1st = 85000
        macd_sell_2nd = 140000
        macd_sell_3rd = 200000
        #--------------------------------
        macd_sell_gap_1st = 29000
        macd_sell_gap_2nd = 49000
        macd_sell_gap_3rd = 59000
    elif -1500000 < price_12hr_average_gap < 1500000:     #이전 12시간동안 변동성이 현재가격에서 -1,500,000 ~ 1,500,000인 경우
        macd_buy_1st = -130000
        macd_buy_2nd = -250000
        macd_buy_3rd = -330000
        macd_buy_gap = -20000
        #--------------------------------
        macd_sell_1st = 120000
        macd_sell_2nd = 230000
        macd_sell_3rd = 300000
        #--------------------------------
        macd_sell_gap_1st = 30000
        macd_sell_gap_2nd = 40000
        macd_sell_gap_3rd = 50000
        00000
    elif -3000000 < price_12hr_average_gap < 3000000:     #이전 12시간동안 변동성이 현재가격에서 -3,000,000 ~ 3,000,000인 경우
        macd_buy_1st = -180000
        macd_buy_2nd = -260000
        macd_buy_3rd = -350000
        macd_buy_gap = -20000
        #--------------------------------
        macd_sell_1st = 160000
        macd_sell_2nd = 240000
        macd_sell_3rd = 320000
        #--------------------------------
        macd_sell_gap_1st = 30000
        macd_sell_gap_2nd = 40000
        macd_sell_gap_3rd = 50000    
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
    coin_price = pyupbit.get_current_price(coin)                        #코인현재가
    jango = upbit.get_balance("KRW")                                    #계좌잔고
    coin_jango = upbit.get_balance(coin)                                #코인매수수량    
    coin_avg_price = round(upbit.get_avg_buy_price(coin), 0)            #매수평단가
    coin_total_krw = coin_avg_price * coin_jango                        #매수한금액
    time_min = time.strftime('%M%S', time.localtime(time.time()))
    time_hore = time.strftime('%H%M%S', time.localtime(time.time()))
    
    #매도에 사용할 금액
    Sell_1st = coin_jango * (20.0/100)      #잔고에 20%매도
    Sell_2nd = coin_jango * (50.0/100)      #1차매도후 잔고에 50%매도
    Sell_3rd = coin_jango * (100.0/100)     #2차매도후 잔고에 100%매도
    Sell_KRW_1st = (coin_avg_price * Sell_3rd) - (coin_avg_price * Sell_1st)  #1차 매도시 잔고 비교용

    if jango >= 700000:
        buy_no = 1
        sell_no = 1
    #------------------------------------------------------------------------
    print('실시간MACD: ', '{0:,.0f}'.format(macd[0]))
    print('실시간Signal: ', '{0:,.0f}'.format(signal[0]))
    print('매매신호값: ', '{0:,.0f}'.format(macd_gap))
    print('------------------------------------------')
    print('MACD_bay_1st: ', '{0:,.0f}'.format(macd_buy_1st))
    print('MACD_sell_1st: ', '{0:,.0f}'.format(macd_sell_1st))
    print('------------------------------------------')
    print('직전봉거래량 * 2.5: ', '{0:,.0f}'.format(before_volume_new))
    print('현재봉거래량: ', '{0:,.0f}'.format(after_volume))
    print('직전봉종가: ', '{0:,.0f}'.format(before_close))
    print('직전봉종가 * -0.10%: ', '{0:,.0f}'.format(before_close_new))
    print('직전봉종가(Gap): ', '{0:,.0f}'.format(before_close_new_temp))    
    print('현재봉가격: ', '{0:,.0f}'.format(after_close))
    print('12시간평균가: ', '{0:,.0f}'.format(price_12hr_average))
    print('12시간평균가(Gap): ', '{0:,.0f}'.format(price_12hr_average_gap))    
    print('------------------------------------------')
    print('코인현재가: {0:,.0f}'.format(coin_price))
    print('보유자산(잔고):', '{0:,.0f}'.format(jango))
    print('------------------------------------------')
    print('매수NO:', '{0:,.0f}'.format(buy_no))
    print('매도NO:', '{0:,.0f}'.format(sell_no))
    
    
    #1차매수
    if buy_no == 1 and int(macd[0]) < macd_buy_1st and macd_buy_gap > int(macd_gap):
        upbit.buy_market_order(coin, Call_KRW_1st)
        coin_jango = upbit.get_balance(coin) #코인매수수량
        coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
        coin_total_krw = coin_avg_price * coin_jango #매수한금액
        bot.sendMessage(chat_id=chat_id, text='■ 1차매수알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="MACD_bay_1st: {0:,.0f}".format(macd_buy_1st))
        bot.sendMessage(chat_id=chat_id, text="MACD_sell_1st: {0:,.0f}".format(macd_sell_1st))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text='코인매수한금액: {0:,.0f}'.format(coin_total_krw))        
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))        
        bot.sendMessage(chat_id=chat_id, text="현재봉가격: {0:,.0f}".format(after_close))        
        buy_no = 2
        sell_no = 1

    #2차매수
    if buy_no == 2 and int(macd[0]) < macd_buy_2nd and macd_buy_gap > int(macd_gap):
        upbit.buy_market_order(coin, Call_KRW_2nd)
        coin_jango = upbit.get_balance(coin) #코인매수수량    
        coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
        coin_total_krw = coin_avg_price * coin_jango #매수한금액
        bot.sendMessage(chat_id=chat_id, text='■ 2차매수알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="MACD_bay_2nd: {0:,.0f}".format(macd_buy_2nd))
        bot.sendMessage(chat_id=chat_id, text="MACD_sell_2nd: {0:,.0f}".format(macd_sell_2nd))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text='코인매수한금액: {0:,.0f}'.format(coin_total_krw))        
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))        
        bot.sendMessage(chat_id=chat_id, text="현재봉가격: {0:,.0f}".format(after_close))
        buy_no = 3
        sell_no = 1

    #3차매수
    if buy_no == 3 and int(macd[0]) < macd_buy_3rd and macd_buy_gap > int(macd_gap):
        upbit.buy_market_order(coin, Call_KRW_3rd)
        coin_jango = upbit.get_balance(coin) #코인매수수량    
        coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
        coin_total_krw = coin_avg_price * coin_jango #매수한금액
        bot.sendMessage(chat_id=chat_id, text='■ 3차매수알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="MACD_bay_3rd: {0:,.0f}".format(macd_buy_3rd))
        bot.sendMessage(chat_id=chat_id, text="MACD_sell_3rd: {0:,.0f}".format(macd_sell_3rd))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text='코인매수한금액: {0:,.0f}'.format(coin_total_krw))        
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))        
        bot.sendMessage(chat_id=chat_id, text="현재봉가격: {0:,.0f}".format(after_close))        
        sell_no = 1
        
    #1차매도
    if sell_no == 1  and coin_price > coin_avg_price and int(macd[0]) > macd_sell_1st and int(macd_gap) > macd_sell_gap_1st:
        bot.sendMessage(chat_id=chat_id, text='■ 1차매도알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text='코인매도가: {0:,.0f}'.format(coin_price))        
        upbit.sell_market_order(coin, Sell_1st)
        sell_no = 2

    #2차매도
    if sell_no == 2 and coin_price > coin_avg_price and coin_total_krw > 1 and int(macd[0]) > macd_sell_2nd and int(macd_gap) > macd_sell_gap_2nd:
        bot.sendMessage(chat_id=chat_id, text='■ 2차매도알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text='코인매도가: {0:,.0f}'.format(coin_price))        
        upbit.sell_market_order(coin, Sell_2nd)
        sell_no = 3

    #3차매도
    if sell_no == 3 and coin_price > coin_avg_price and coin_total_krw > 1 and int(macd[0]) > macd_sell_3rd and int(macd_gap) > macd_sell_gap_3rd:
        bot.sendMessage(chat_id=chat_id, text='■ 3차매도알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text='코인매도가: {0:,.0f}'.format(coin_price))        
        upbit.sell_market_order(coin, Sell_3rd)
        buy_no = 1

    #급락시 매도대응
    if coin_total_krw > 1 and coin_price < before_close_new and after_volume > before_volume_new:
        bot.sendMessage(chat_id=chat_id, text='■급락매도알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text='코인매도가: {0:,.0f}'.format(coin_price))
        bot.sendMessage(chat_id=chat_id, text="--------------")
        bot.sendMessage(chat_id=chat_id, text="직전봉거래량 * 2.5: {0:,.0f}".format(before_volume_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉거래량: {0:,.0f}".format(after_volume))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가: {0:,.0f}".format(before_close))
        bot.sendMessage(chat_id=chat_id, text="직전봉종가 * -0.10%: {0:,.0f}".format(before_close_new))
        bot.sendMessage(chat_id=chat_id, text="현재봉가격: {0:,.0f}".format(after_close))
        bot.sendMessage(chat_id=chat_id, text="전량 매도후 5시간 매매대기합니다.")
        upbit.sell_market_order(coin, coin_jango)
        sell_no = 1
        time.sleep(18000) #5시간 wait 매매대기

    else:
        print('■ 매매대기중')        
        print('------------------------------------------')
    
    #매시간 정각에 텔레그램 보내기
    if time_min > "0000" and time_min < "0015":
        bot.sendMessage(chat_id=chat_id, text='■ 매시간 00분 알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="MACD_bay_1st: {0:,.0f}".format(macd_buy_1st))
        bot.sendMessage(chat_id=chat_id, text="MACD_sell_1st: {0:,.0f}".format(macd_sell_1st))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text="매수NO: {0:,.0f}".format(buy_no))
        bot.sendMessage(chat_id=chat_id, text="매도NO: {0:,.0f}".format(sell_no))
        bot.sendMessage(chat_id=chat_id, text="현재가격: {0:,.0f}".format(coin_price))        
    elif time_min > "3000" and time_min < "3015":
        bot.sendMessage(chat_id=chat_id, text='■ 매시간 30분 알림:')
        bot.sendMessage(chat_id=chat_id, text='MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='MACD_Gap: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text="MACD_bay_1st: {0:,.0f}".format(macd_buy_1st))
        bot.sendMessage(chat_id=chat_id, text="MACD_sell_1st: {0:,.0f}".format(macd_sell_1st))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격: {0:,.0f}".format(price_12hr_average))
        bot.sendMessage(chat_id=chat_id, text="12시간 평균가격_Gap : {0:,.0f}".format(price_12hr_average_gap))
        bot.sendMessage(chat_id=chat_id, text="매수NO: {0:,.0f}".format(buy_no))
        bot.sendMessage(chat_id=chat_id, text="매도NO: {0:,.0f}".format(sell_no))
        bot.sendMessage(chat_id=chat_id, text="현재가격: {0:,.0f}".format(coin_price))

    time.sleep(5)
