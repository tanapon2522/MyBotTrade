from flask import Flask , request
from BinanceTrade.Trade import client
import json , time

from BinanceTrade.Trade import ReceiveSignals
from line.notify import sendmsg

app = Flask(__name__)

#@app.rout("/START/REBALANCEBOT/SYMBOL")

#@app.rout("/STOP/REBALANCEBOT/SYMBOL")

@app.route("/SIGNALS" , methods=['POST'] )
def SIGNALS_RECEIVER():
    if request.method == "POST":
        msg = request.data.decode("utf-8")
        json_msg = json.loads(msg) # <== dictionary
        print(json_msg['SYMBOL']) # <== dictionary

        prices = client.get_all_tickers()
        for p in prices:     
            if p["symbol"] == json_msg["SYMBOL"]:
               print(p['symbol'],float(p['price']))
               json_msg['POSITION_SIZE'] = round(float(json_msg['POSITION_SIZE'])/(float(p['price'])),6)
        
        json_msg['TIME'] = str(time.asctime())
        print(json_msg)

        # get data firebase เพื่อดูว่า Autotrading == true ??
        msg = ReceiveSignals(signal_data_dict= json_msg)

        sendmsg(msg=str(json_msg))
        sendmsg(msg=msg)

        # สร้างฟังก์ชั่น ในการจัดการข้อมูล

        """
        {"SYMBOL":"{{ticker}}",
        "TIME":{{timenow}},
        "SIGNALS":"{{strategy.order.action}}",
        "POSITION_SIZE":{{strategy.order.contracts}} }

        example data

        {"SYMBOL":"BTCUSDT",
        "TIME":{{TIMESTAMP}},
        "SIGNALS":"buy",
        "POSITION_SIZE":0.34 }
        
        """
    return "200"

from line.LineBot import handler

@app.route("/linebot", methods=['POST'])

def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

if __name__== "__main__":
    app.run(debug=True,port=8088)
