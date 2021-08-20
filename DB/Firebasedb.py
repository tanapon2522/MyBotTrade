try:
    from config_dev import firebaseClient

except:
    from config_prod import firebaseClient

db = firebaseClient.database()

def WriteInitialValue(symbols,initialValue):
    data = { "initialValue" : initialValue }
    db.child(symbols).update(data)

def GetInitialValue(symbols):

    # res = db.get().val()[symbols]
    # lastest_data = list(res.keys())[-1]
    # res_data = res[lastest_data]
    # print(res_data)

    # Value เริ่มต้น
    try:
        res = db.get().val()[symbols]["initialValue"]
        return res
    
    except KeyError:
        WriteInitialValue(symbols=symbols, initialValue=0)
        res = db.get().val()[symbols]["initialValue"]
        return res
