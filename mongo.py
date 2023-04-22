from datetime import datetime

import pymongo

# myclient = pymongo.MongoClient("mongodb://10.0.22.31:27310/")
myclient = pymongo.MongoClient("mongodb://10.0.22.35:27316/")

mydb = myclient["filteredQuoteDB"]

mycol = mydb["QTest"]

date = datetime(year=2023, month=1, day=29, hour=10, minute=30, second=45)
opn = {
  "LastTradedTime": date,
  "LastAuctionPhase": "",
  "LastTradedQty": 1000.0,
  "LastTradedPrice": 35.0,
  "MDTime": date,
  "creationTime": date
}
pop = {
  "LastTradedTime": date,
  "LastAuctionPhase": "POP",
  "LastTradedQty": 1000.0,
  "LastAuctionVolume": 1000.0,
  "LastTradedPrice": 35.0,
  "MDTime": date,
  "creationTime": date
}
clo = {
  "LastTradedTime": date,
  "LastAuctionPhase": "",
  "LastTradedQty": 1000.0,
  "LastAuctionVolume": 1000.0,
  "LastTradedPrice": 35.0,
  "MDTime": date,
  "creationTime": date
}



x = mycol.insert_many([opn, pop, clo])