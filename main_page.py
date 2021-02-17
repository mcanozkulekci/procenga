import coin_data

class Coins:
        
    def __init__(self, info, coin_type):
        self.price = info[0]
        self.volume = info[1]
        self.change = info[2]
        self.time = info[3]
        self.coin_type = coin_type

    def __str__(self):
        return "{}   --> {} TL\n24H Volume --> {} {}\n24H Change --> % {}".format(self.time, self.price, self.volume, self.coin_type, self.change)

"""
while 1:
    usr_input = input("1 - BTC Price  2- ETH Price 3- XRP Price\n")
    if usr_input == '1':
        cn = "BTC"
        BTC_values = Coins(coin_data.BTC(), cn)
        print(BTC_values)
    elif usr_input == '2':
        cn = "ETH"
        ETH_values = Coins(coin_data.ETH(), cn)
        print(ETH_values)
    elif usr_input == '3':
        cn = "XRP"
        XRP_values = Coins(coin_data.XRP(), cn)
        print(XRP_values)
    else:
        break

"""