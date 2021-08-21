API_BINANCE_KEY="cXl8CbhhJVy2Gm8feXERfqiVivimTkM7XGLO7Z17uogZQPm1Q5R1gdQ5upG6ABAP"
API_BINANCE_SECRET = "rL2diYJ84IDD1W1cNrHMgy4I9vVvD5MbB3NJGDJmINNrkNlzXH3djSHw1KqsVdw4"


API_LINE_KEY = "cy8Vy9rQQotstI5E1rQZ08"
API_CLIENT_SECRET = "iqeoS5U8urxTHVSDHbVaCq0Ddddr2Li1XD4IWOkIje2"
LINE_NOTIFY_TOKEN = "a1O4pHRieDDBGpElsK4aAoJZhGdbsWgeWsmbbTfnUnh"

LINE_BOT_ACCESS_TOKEN = "qypXLFIvmrVha9RHwNsprpqTv0D9ZLM7MiJZnHVxMQcdgux5g7uzSfBfFT9R/37lL3Qrp5kd0r27RFFwqSXbIoYwoSJSCjqiz0tXgHQBIAqkiuiSWNN8bMUiFeGOk07FuYcUcQkPqFx3ehMivc2xJAdB04t89/1O/w1cDnyilFU="
LINE_BOT_CHANNEL_SECRET = "53dda14d2a2a334fc43228c08fefe113"

from firebase import Firebase

firebaseConfig = {
    "apiKey": "AIzaSyCX_VTmOCeQ22wgo8G7XGPBj2bontNMiz8",
    "authDomain": "bottrade-db-mybot.firebaseapp.com",
    "projectId": "bottrade-db-mybot",
    "storageBucket": "bottrade-db-mybot.appspot.com",
    "messagingSenderId": "415126488514",
    "appId": "1:415126488514:web:6964274a970b76ad38025b",
    "measurementId": "G-6NB6B7B2NP",
    "databaseURL": "https://bottrade-db-mybot-default-rtdb.asia-southeast1.firebasedatabase.app",
    "serviceAccount" : "bottrade-db-mybot-firebase-adminsdk-d1hnd-36975cb408.json" # นำไฟล์ของท่านมาใส่เองด้วย
  }

firebaseClient = Firebase(firebaseConfig)
auth = firebaseClient.auth()
#user = auth.sign_in_with_email_and_password("mybot@gmail.com","12345678")

# ทดสอบ
if __name__ == '__main__':
  db = firebaseClient.database()
  data = {
    "name":"TEST"
  }
  user = auth.refresh(user['refreshToken'])
  results = db.child("users").push(data,user['idToken'])
