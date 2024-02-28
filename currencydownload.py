from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import matplotlib.pyplot as plt

import threading
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)      
        self.ask = [] 
        self.bid = [] 
    def historicalData(self, reqId, bar):
        if reqId == 1:
                 self.ask.append([bar.date, bar.close])
        if reqId == 1:
                 self.bid.append([bar.date, bar.close])

def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 123)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
var1_contract = Contract()
var1_contract.symbol = 'EUR'
var1_contract.secType = 'CASH'
var1_contract.currency = 'USD'
var1_contract.exchange = 'IDEALPRO'

#Request historical candles
app.reqHistoricalData(1, var1_contract, '', '5 y', '1 hour', 'ASK', 0, 1, False, [])
#app.reqHistoricalData(2, var1_contract, '', '1 M', '1 hour', 'BID', 0, 1, False, [])

time.sleep(200) #sleep to allow enough time for data to be returned


#Working with Pandas DataFrames
import pandas

df_bid = pandas.DataFrame(app.bid, columns=['DateTime', 'Bid'])
df_ask = pandas.DataFrame(app.ask, columns=['DateTime', 'Ask'])

df=df_ask
df["Bid"] = df_bid["Bid"]

df.head(10)

df.plot()
plt.show()

df.to_csv('eurusd.csv')  

print(df)


app.disconnect()