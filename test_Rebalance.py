

if __name__ == "__main__":
    
    # from DB.Firebasedb import GetInitialValue , WriteInitialValue
    # WriteInitialValue(symbols="XRP",initialValue=25)
    # res = GetInitialValue(symbols="ETH")
    # print(res)
    
    # from RebalanceBot.Rebalance import rebalanceAsset
    # rebalanceAsset(symbols="DOGE")

    from RebalanceBot.Rebalance import RebalanceBot
    bot = RebalanceBot(interval=5,coins_list=["XRP","DOGE","BTC","ETH"])
    import threading
    bot_bg = threading.Thread(target=bot.run,daemon=True)
    bot_bg.start()

    while True :
        if input("PRESS ENTER TO STOP"):
            bot.pause()
            if input("PRESS TO RESUME"):
                bot.resume()

        if input("X to kill bot") == "X":
            bot.kill()
        break