import pyupbit
import requests
import pandas as pd
import time
import webbrowser
import telegram
import datetime

#자동매매 설정부분
#========================================================================
access = "nehpcdrsANEdzmeHeWY5MVEElxY4Exl4Y5HymcsH"
secret = "pH5hvBYyC2wvchkGTyz8gYYGsBvSgv0ZGFMPh66Z"
upbit =  pyupbit.Upbit(access, secret)

bot = telegram.Bot(token='5007441586:AAF-TCPvcJbGYVn224m-dvlqgsePkvW_gW8')
chat_id ="849745003"

coin = "KRW-BTC"

#1차매수에 사용할 금액
Total_KRW = 30000
Call_KRW_1st = Total_KRW * (50.0/100)
Call_KRW_2nd = Total_KRW * (50.0/100)

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
    df=df.iloc[::-1]    
    df=df['trade_price']    

    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    signal = macd.ewm(span=9, adjust=False).mean()

    macd_gap = abs(macd[0]) - abs(signal[0])    
    #------------------------------------------------------------------------
    coin_price = pyupbit.get_current_price(coin) #코인현재가
    jango = upbit.get_balance("KRW") #계좌잔고
    coin_jango = upbit.get_balance(coin) #코인매수수량    
    coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
    coin_total_krw = coin_avg_price * coin_jango #매수한금액
    time_min = time.strftime('%M%S', time.localtime(time.time()))


    print('실시간MACD: ', '{0:,.0f}'.format(macd[0]))
    print('실시간Signal: ', '{0:,.0f}'.format(signal[0]))
    print('')
    print('매매신호값: ', '{0:,.0f}'.format(macd_gap))    
    print('------------------------------------------')    
    print('코인현재가: {0:,.0f}'.format(coin_price))
    print('보유자산:', '{0:,.0f}'.format(jango))
    print(time_min)
    print('------------------------------------------')

    if bay_no == 1 and macd[0] < -100000 and macd_gap < 7000:
        upbit.buy_market_order(coin, Call_KRW_1st)
        coin_jango = upbit.get_balance(coin) #코인매수수량    
        coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
        coin_total_krw = coin_avg_price * coin_jango #매수한금액
        
        bot.sendMessage(chat_id=chat_id, text='■ 1차매수알림:')
        bot.sendMessage(chat_id=chat_id, text='1차실시간MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='1차매매신호값: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text='코인매수한금액: {0:,.0f}'.format(coin_total_krw))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bay_no = 2
        sell_no = 1

    if bay_no == 2 and macd[0] < -150000 and macd_gap < 3000:
        upbit.buy_market_order(coin, Call_KRW_2nd)
        coin_jango = upbit.get_balance(coin) #코인매수수량    
        coin_avg_price = round(upbit.get_avg_buy_price(coin), 0) #매수평단가
        coin_total_krw = coin_avg_price * coin_jango #매수한금액

        bot.sendMessage(chat_id=chat_id, text='■ 2차매수알림:')
        bot.sendMessage(chat_id=chat_id, text='2차실시간MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='2차매매신호값: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text='코인매수한금액: {0:,.0f}'.format(coin_total_krw))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bay_no = "end"
        sell_no = 1

    elif sell_no == 1 and macd[0] > 130000 and macd_gap < 12000:
        upbit.sell_market_order(coin, coin_jango)
        
        bot.sendMessage(chat_id=chat_id, text='■ 매도알림:')
        bot.sendMessage(chat_id=chat_id, text='실시간MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='매매신호값: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text='코인평단가: {0:,.0f}'.format(coin_avg_price))
        bot.sendMessage(chat_id=chat_id, text='코인매도가: {0:,.0f}'.format(coin_price))
        sell_no = "end"
        bay_no = 1

    else:
        print('매매대기중')        
        print('------------------------------------------')
    
    #매시간 정각에 텔레그램 보내기
    if time_min > "0000" and time_min < "0015":
        bot.sendMessage(chat_id=chat_id, text='실시간MACD: {0:,.0f}'.format(macd[0]))
        bot.sendMessage(chat_id=chat_id, text='매매신호값: {0:,.0f}'.format(macd_gap))
        bot.sendMessage(chat_id=chat_id, text='MACD값이 -100000이하 and 신호값이 7000보다 작을때 1차매수')
        bot.sendMessage(chat_id=chat_id, text='MACD값이 -150000이하 and 신호값이 3000보다 작을때 2차매수')
        bot.sendMessage(chat_id=chat_id, text='MACD값이 +130000이상 and 신호값이 12000보다 작을때 전량매도')
    
    time.sleep(10)
