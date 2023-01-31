import datetime
from datetime import timedelta

import pymongo

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.data_sets.constants import TradingPhases


class AlgoMongoManager:
    @staticmethod
    def get_straight_curve_for_mongo(phases: list, volume: float = 1000.0, price: float = 35.0) -> list:
        pop_start = AFM.change_datetime_from_epoch_to_normal(AFM.get_timestamp_from_list(phases=phases, phase=TradingPhases.PreOpen, start_time=True)).replace(tzinfo=None) - timedelta(days=1)
        pop_end = AFM.change_datetime_from_epoch_to_normal(AFM.get_timestamp_from_list(phases=phases, phase=TradingPhases.PreOpen, start_time=False)).replace(tzinfo=None) - timedelta(days=1)
        pcl_start = AFM.change_datetime_from_epoch_to_normal(AFM.get_timestamp_from_list(phases=phases, phase=TradingPhases.PreClosed, start_time=True)).replace(tzinfo=None) - timedelta(days=1) + timedelta(minutes=1)



        mongo_list = []
        current_time = pop_end
        now = datetime.datetime.now()
        # region add POP curve
        mongo_list.append({
            "LastTradedTime": pop_start,
            "LastAuctionPhase": "PRE",
            "LastTradedQty": volume,
            "LastAuctionVolume": volume,
            "LastTradedPrice": price,
            "MDTime": pop_start,
            "creationTime": pop_start
        })

        # region add OPN curve
        while current_time < pcl_start:
            mongo_list.append({
                "LastTradedTime": current_time,
                "LastAuctionPhase": "",
                "LastTradedQty": volume,
                "LastTradedPrice": 35.0,
                "MDTime": current_time,
                "creationTime": current_time
            })
            current_time += timedelta(minutes=1)

        # region add PCL curve
        mongo_list.append({
            "LastTradedTime": pcl_start,
            "LastAuctionPhase": "PCL",
            "LastAuctionVolume": volume,
            "LastTradedQty": volume,
            "LastTradedPrice": price,
            "MDTime": pcl_start,
            "creationTime": pcl_start
        })

        return mongo_list

    @staticmethod
    def insert_many_to_mongodb_with_drop(data, db, collection, host="localhost", port=27017):
        client = pymongo.MongoClient(host, port)
        db = client[db]
        coll = db[collection]
        if collection in db.list_collection_names():
            coll.drop()
        coll.insert_many(data)


# region Usage example
# # get list of trading phases
# trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.PreClosed)
# # get curve to insert to mongo
# curve = AlgoMongoManager.get_straight_curve_for_mongo(trading_phases)
# # insert data into mongoDB
# AlgoMongoManager.insert_many_to_mongodb_with_drop(curve, "filteredQuoteDB", "Q48", host="10.0.22.35", port=27316)
# region