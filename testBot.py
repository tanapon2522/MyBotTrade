from flask.scaffold import F
from BinanceTrade.Trade import client
import json
from BinanceTrade.Trade import ReceiveSignals
from line.notify import sendmsg
import time
import math
from DB.Firebasedb import GetDataSettingBot , UpdateSettingBot

# info = client.get_account()
# USDT_balance = client.get_asset_balance("USDT")
# print(USDT_balance)
# sym = 'BTCUSDT'
# prices = client.get_all_tickers()
# for p in prices :    
#     if p['symbol'] == sym:
#         print(p['symbol'],float(p['price']))
#         pricetmp = float(p['price'])
#         break

#ทดลอง รับค่ามา
# time.sleep(5)
# prices = client.get_all_tickers()
# for p in prices :    
#     if p['symbol'] == sym:
#         print(p['symbol'],float(p['price']))
#         pricecheck = float(p['price'])
#         break
# if pricetmp < pricecheck :
#     pricetmp = pricecheck
#     print(p['symbol'],pricetmp)
# elif pricetmp >= pricecheck :
#     pricetmp = pricecheck
#     print(p['symbol'],pricetmp)


# def BUY(symbol,position_size):
#     USDT_balance = client.get_asset_balance("USDT")

#     POS_SIZE = str(position_size)
#     sym = symbol.split("USDT")[0] #BTCUSDT --> BTC
#     #0.00223445 --> [0 , 00223445]
#     Interger = POS_SIZE.split(".")[0]
#     decimal = POS_SIZE.split(".")[1]
#     dec_count = -1

#     while True:
#         position_size = Interger + "." + decimal[:dec_count]    
#         if float(position_size) > 0 :
#             try:
#                 if float(USDT_balance['free']) > 10:
#                     order = client.order_market_buy(
#                         symbol=symbol,
#                         quantity=position_size
                        
#                     )
#                     print("BUY SUCCESS")
#                     return order
#             except Exception as e:
#                 if e.code == -1013:
#                     dec_count = dec_count -1
#                 else :
#                     print(e.args)
#                     return "เกิดข้อผิดพลาด"

# def SELL(symbol):
    
#     sym = symbol.split("USDT")[0] #BTCUSDT --> BTC
#     # 0.00223445 --> [0 , 00223445]
#     Interger = client.get_asset_balance(sym)['free'].split(".")[0]
#     decimal = client.get_asset_balance(sym)['free'].split(".")[1]
#     dec_count = -1
#     print(Interger)
#     print(decimal)
#     while True:
#         position_size = Interger + "." + decimal[:dec_count]
#         if float(position_size) > 0:
#             try:
#                 order = client.order_market_sell(
#                     symbol=symbol,
#                     quantity=position_size
#                 )
#                 return order
#             except Exception as e:
#                 if e.code == -1013:
#                     dec_count = dec_count -1
#                 else :
#                     print(e.args)
#                     return "เกิดข้อผิดพลาด"
               
# def ReceiveSignals(signal_data_dict):
#     if signal_data_dict["SIGNALS"] == "buy":
#        BUY(symbol=signal_data_dict["SYMBOL"],position_size=signal_data_dict["POSITION_SIZE"])
        
#        return "BUY {} SUCCESS! \nSIZE : {}".format(signal_data_dict["SYMBOL"],signal_data_dict["POSITION_SIZE"])

#     elif signal_data_dict["SIGNALS"] == "sell":
#        SELL(symbol=signal_data_dict["SYMBOL"])
#        return "SELL {} SUCCESS".format(signal_data_dict["SYMBOL"])

if __name__ == "__main__":

    #data = {"SYMBOL": "SOLUSDT", "SIGNALS": "buy"}#{"SYMBOL":"{{ticker}}","SIGNALS":"buy","Price":"{{close}}"}
    
    #msg = ReceiveSignals(signal_data_dict=data)

    #sendmsg(msg=msg)

    # if data["SIGNALS"] == "sell":
    #    print(data["SYMBOL"])
    #    print("\n" + "SELL NOW")
    # else:
    #    print(data["SYMBOL"])
    #    print("\n" + "BUY NOW")


    # order = BUY(symbol="DOGEUSDT",position_size=71.428)
    #order = SELL(symbol="BTCUSDT")
    #print(order)

    #ทดลอง รับค่า


    data = {"SYMBOL": "BTCUSDT", "SIGNALS": "buy"}
    sym = data["SYMBOL"]    
    prices = client.get_all_tickers()
    for p in prices :    
        if p['symbol'] == sym:
            print(p['symbol'],float(p['price']))
            pricetmp = float(p['price'])
            break


    # UpdateSettingBot(key="CBuy",value = True)
    # UpdateSettingBot(key="CSell",value = True)
    # msg = ReceiveSignals(signal_data_dict= data)
    # sendmsg(msg=str(data))
    # sendmsg(msg=msg)
    # if (data["SIGNALS"]=="buy"):
    #     UpdateSettingBot(key="CBuy",value = False)
    #     UpdateSettingBot(key="CSell",value = True)
    # elif (data["SIGNALS"]=="sell"):
    #     UpdateSettingBot(key="CBuy",value = True)
    #     UpdateSettingBot(key="CSell",value = False)

    while GetDataSettingBot(key="run") == True:
        # ตรวจ จุด เข้า buy
        checkbuy = False
        while checkbuy == False :
            time.sleep(5)
            prices = client.get_all_tickers()
            for p in prices :    
                if p['symbol'] == sym:
                    print(p['symbol'],float(p['price']))
                    pricecheck = float(p['price'])
                    break
            if pricetmp < pricecheck :                    
                data["SIGNALS"] = "buy"
                UpdateSettingBot(key="CBuy",value = True)
                pricetmp = pricecheck
                checkbuy = True                
            else :
                pricetmp = pricecheck

        cbuy = GetDataSettingBot(key="CBuy")                  
        if (data["SIGNALS"]=="buy") and cbuy:                                 
            msg = ReceiveSignals(signal_data_dict= data)
            pricetmp = data["Price"]
            print(pricetmp)
            #print(pricetmp*(1+(1/1000)))
            pricetmp = pricetmp*(1+(1/1000))
            sendmsg(msg=str(data))
            sendmsg(msg=msg)                               
            UpdateSettingBot(key="CBuy",value = False)
            UpdateSettingBot(key="CSell",value = True)
            
        # ตรวจ จุด เข้า sell
        checksell = False
        while checksell == False :
            time.sleep(5)
            prices = client.get_all_tickers()
            for p in prices :    
                if p['symbol'] == sym:
                    print(p['symbol'],float(p['price']))
                    pricecheck = float(p['price'])
                    break        
            if (pricetmp < pricecheck) :                
                data["SIGNALS"] = "sell"
                UpdateSettingBot(key="CSell",value = True)
                pricetmp = pricecheck
                checksell = True 
            else :
                print(pricecheck)
            
        csell = GetDataSettingBot(key="CSell")            
        if (data["SIGNALS"]=="sell") and csell:                                               
            msg = ReceiveSignals(signal_data_dict= data)
            pricetmp = data["Price"]
            print(pricetmp)                
            sendmsg(msg=str(data))
            sendmsg(msg=msg)                      
            UpdateSettingBot(key="CBuy",value = True)
            UpdateSettingBot(key="CSell",value = False)
                               
            #break


