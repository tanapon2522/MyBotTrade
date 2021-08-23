from binance.client import Client
import time

try :
    from config_dev import API_BINANCE_KEY , API_BINANCE_SECRET
except Exception:
    from config_prod import API_BINANCE_KEY , API_BINANCE_SECRET

from DB.Firebasedb import GetDataSettingBot

client = Client( API_BINANCE_KEY , API_BINANCE_SECRET )

def BUY(symbol,position_size):
    USDT_balance = client.get_asset_balance("USDT")

    POS_SIZE = str(position_size)
    sym = symbol.split("USDT")[0] #BTCUSDT --> BTC
    #0.00223445 --> [0 , 00223445]
    Interger = POS_SIZE.split(".")[0]
    decimal = POS_SIZE.split(".")[1]
    dec_count = -1
    while True:  
        if float(position_size) > 0 :
            try:
                if float(USDT_balance['free']) > 10:
                    order = client.order_market_buy(
                        symbol=symbol,
                        quantity=position_size
                        
                    )
                    print("BUY SUCCESS")
                    return order
            except Exception as e:
                if ((e.code== -1013) or (e.code == -1111)):                    
                    position_size = Interger + "." + decimal[:dec_count]
                    if decimal[:dec_count] == "":
                        position_size = int(interger)
                    dec_count = dec_count -1
                else :
                    print(e.args)
                    return "เกิดข้อผิดพลาด"

def SELL(symbol,position_size=0,sell_all=True):
    POS_SIZE = str(position_size)
    sym = symbol.split("USDT")[0] #BTCUSDT --> BTC
    #0.00223445 --> [0 , 00223445]
    if sell_all:
        POS_SIZE = client.get_asset_balance(sym)['free']
    Interger = POS_SIZE.split(".")[0]
    decimal = POS_SIZE.split(".")[1]
    dec_count = -1

    while True:
        position_size = Interger + "." + decimal[:dec_count]
        if float(position_size) > 0:
            try:
                order = client.order_market_sell(
                    symbol=symbol,
                    quantity=position_size
                )
                print("SELL SUCCESS")
                return order
            except Exception as e:
                if ((e.code== -1013) or (e.code == -1111)):                    
                    position_size = Interger + "." + decimal[:dec_count]
                    if decimal[:dec_count] == "":
                        position_size = int(interger)
                    dec_count = dec_count -1
                else :
                    print(e.args)
                    return "เกิดข้อผิดพลาด"
               
def ReceiveSignals(signal_data_dict):

    signal_data_dict['POSITION_SIZE'] = float(GetDataSettingBot(key="Positionsize"))
    prices = client.get_all_tickers()
    for p in prices:     
        if p["symbol"] == signal_data_dict["SYMBOL"]:
            print(p['symbol'],float(p['price']))
            signal_data_dict['POSITION_SIZE'] = signal_data_dict['POSITION_SIZE']/float(p['price'])
        
    signal_data_dict['TIME'] = str(time.asctime())

    if signal_data_dict["SIGNALS"] == "buy":
        try :   
            BUY(symbol=signal_data_dict["SYMBOL"],position_size=signal_data_dict["POSITION_SIZE"])
            return "BUY {} SUCCESS! \nSIZE : {}".format(signal_data_dict["SYMBOL"],signal_data_dict["POSITION_SIZE"])
        except Exception as e:
            return "เกิดข้อผิดพลาด {}".format(e.args)

    elif signal_data_dict["SIGNALS"] == "sell":
        try :
            SELL(symbol=signal_data_dict["SYMBOL"])
            return "SELL {} SUCCESS".format(signal_data_dict["SYMBOL"])
        except Exception as e:
            return "เกิดข้อผิดพลาด {}".format(e.args)