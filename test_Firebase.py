try :
    from config_dev import API_BINANCE_KEY , API_BINANCE_SECRET
except Exception:
    from config_prod import API_BINANCE_KEY , API_BINANCE_SECRET

from DB.Firebasedb import GetDataSettingBot

from BinanceTrade.Trade import ReceiveSignals
from line.notify import sendmsg


if __name__ == "__main__":

    data = {"SYMBOL": "SOLUSDT", "SIGNALS": "sell"}
    
    msg = ReceiveSignals(signal_data_dict=data)

    sendmsg(msg=msg)