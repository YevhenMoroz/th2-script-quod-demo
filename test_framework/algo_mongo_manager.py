import datetime
from datetime import timedelta

import pymongo

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.data_sets.constants import TradingPhases


class AlgoMongoManager:
    @staticmethod
    def get_straight_curve_for_mongo(phases: list, volume: float = 1000.0, price: float = 35.0) -> list:
        if type(volume) != float:
            raise ValueError("Volume should be float type")
        if type(price) != float:
            raise ValueError("Price should be float type")

        pop_end = AFM.change_datetime_from_epoch_to_normal(AFM.get_timestamp_from_list(phases=phases, phase=TradingPhases.PreOpen, start_time=False)).replace(tzinfo=None) - timedelta(days=1)
        pcl_start = AFM.change_datetime_from_epoch_to_normal(AFM.get_timestamp_from_list(phases=phases, phase=TradingPhases.PreClosed, start_time=True)).replace(tzinfo=None) - timedelta(days=1)



        mongo_list = []
        current_time = pop_end
        # region add POP curve
        mongo_list.append({
            "LastTradedTime": pop_end,
            "LastAuctionPhase": "PRE",
            "LastTradedQty": volume,
            "LastAuctionVolume": volume,
            "LastTradedPrice": price,
            "MDTime": pop_end,
            "creationTime": pop_end
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
    def get_repeated_curve_for_mongo(phases: list, volume_list: list, price: float = 35.0) -> list:
        if type(price) != float:
            raise ValueError("Price should be float type")

        pop_end = AFM.change_datetime_from_epoch_to_normal(AFM.get_timestamp_from_list(phases=phases, phase=TradingPhases.PreOpen, start_time=False)).replace(tzinfo=None) - timedelta(days=1)
        pcl_start = AFM.change_datetime_from_epoch_to_normal(AFM.get_timestamp_from_list(phases=phases, phase=TradingPhases.PreClosed, start_time=True)).replace(tzinfo=None) - timedelta(days=1)

        mongo_list = []
        current_time = pop_end

        # region add OPN curve
        n = 0
        while current_time < pcl_start:
            a = {
                "LastTradedTime": current_time,
                "LastAuctionPhase": "",
                "LastTradedPrice": 35.0,
                "MDTime": current_time,
                "creationTime": current_time
            }
            a["LastTradedQty"] = volume_list[n]
            mongo_list.append(a)
            current_time += timedelta(minutes=1)
            n += 1
            n %= len(volume_list)

        return mongo_list


    @staticmethod
    def connect_to_mongo(host="localhost", port=27017):
        return pymongo.MongoClient(host, port)

    @staticmethod
    def get_database(client, db):
        return client[db]

    @staticmethod
    def get_collection(db, collection_name):
        return db[collection_name]

    @staticmethod
    def drop_collection(db, collection_name):
        coll = AlgoMongoManager.get_collection(db, collection_name)
        if collection_name in db.list_collection_names():
            coll.drop()

    @staticmethod
    def insert_many(collection, data):
        collection.insert_many(data)

    @staticmethod
    def insert_one(collection, data):
        collection.insert_one(data)

    @staticmethod
    def insert_many_to_mongodb_with_drop(data, db, collection_name, host="localhost", port=27017):
        client = AlgoMongoManager.connect_to_mongo(host, port)
        database = AlgoMongoManager.get_database(client, db)
        collection = AlgoMongoManager.get_collection(database, collection_name)
        AlgoMongoManager.drop_collection(database, collection_name)
        AlgoMongoManager.insert_many(collection, data)


    @staticmethod
    def insert_one_to_mongodb_with_drop(data, db, collection_name, host="localhost", port=27017):
        client = AlgoMongoManager.connect_to_mongo(host, port)
        database = AlgoMongoManager.get_database(client, db)
        collection = AlgoMongoManager.get_collection(database, collection_name)
        AlgoMongoManager.drop_collection(database, collection_name)
        AlgoMongoManager.insert_one(collection, data)

    @staticmethod
    def create_empty_collection(db, collection_name, host="localhost", port=27017):
        AlgoMongoManager.insert_one_to_mongodb_with_drop({}, db, collection_name, host, port)

# region Usage example
# # get list of trading phases
# trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.PreClosed)
# # get curve to insert to mongo
# curve = AlgoMongoManager.get_straight_curve_for_mongo(trading_phases, volume=100.0)
# # insert data into mongoDB
# AlgoMongoManager.insert_many_to_mongodb_with_drop(curve, "filteredQuoteDB", "Q48", host="10.0.22.35", port=27316)
# region