from custom.tenor_settlement_date import spo, wk1, wk2, spo_ndf, wk1_ndf, wk2_ndf, today, tom, wk3, m1, wk3_ndf, m1_ndf
from test_framework.fix_wrappers.FixMessageMarketDataSnapshotFullRefresh import FixMessageMarketDataSnapshotFullRefresh
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX


class FixMessageMarketDataSnapshotFullRefreshSellFX(FixMessageMarketDataSnapshotFullRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_params_for_md_response(self, md_request: FixMessageMarketDataRequestFX,
                                   no_md_entries_count: list = ["*", "*", "*"],
                                   published=True, ndf=False,
                                   priced=True, band_not_pub: list = None, band_not_priced=None, response=None):
        self.prepare_params_for_md_response(md_request, response=response)
        if len(no_md_entries_count) > 0:
            band = 0
            row_pub = 0
            row_prc = 0
            check_pub = 0
            check_price = 0
            self.get_parameter("NoMDEntries").clear()
            md_entry_position = 1
            for qty in no_md_entries_count:
                md_entry_type = 0
                while md_entry_type < 2:
                    self.get_parameter("NoMDEntries").append({
                        "SettlType": md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
                        "MDEntryPx": "*",
                        "MDEntryTime": "*",
                        "MDEntryID": "*",
                        "MDEntrySize": qty,
                        "QuoteEntryID": "*",
                        "MDOriginType": "1",
                        "MDQuoteType": "1",
                        "MDEntryPositionNo": "*",
                        "MDEntryDate": "*",
                        "MDEntryType": md_entry_type
                    })
                    if md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "":
                        self.get_parameter("NoMDEntries")[band]["SettlType"] = "0"
                        self.get_parameter("NoMDEntries")[band]["SettlDate"] = spo()
                    elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "0":
                        self.get_parameter("NoMDEntries")[band]["SettlType"] = "0"
                        self.get_parameter("NoMDEntries")[band]["SettlDate"] = spo()
                    if md_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["SecurityType"] == "FXFWD":
                        self.get_parameter("NoMDEntries")[band]["MDEntryForwardPoints"] = "*"
                        self.get_parameter("NoMDEntries")[band]["MDEntrySpotRate"] = "*"
                        if md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "1":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "1"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = today()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "2":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "2"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = tom()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W1":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "W1"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk1()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W2":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "W2"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk2()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W3":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "W3"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk3()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "M1":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "M1"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = m1()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "1":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "1"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = today()
                        # TODO add more SettleType`s
                    if ndf is not False:
                        if md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "1":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "1"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = today()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "2":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "2"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = tom()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "0"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = spo_ndf()
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "0":
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "0"
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = spo_ndf()
                    if md_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["SecurityType"] == "FXNDF":
                        self.get_parameter("NoMDEntries")[band]["MDEntryForwardPoints"] = "*"
                        self.get_parameter("NoMDEntries")[band]["MDEntrySpotRate"] = "*"
                        if md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W1":
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk1_ndf()
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "W1"
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W2":
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk2_ndf()
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "W2"
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W3":
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk3_ndf()
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "W3"
                        elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "M1":
                            self.get_parameter("NoMDEntries")[band]["SettlDate"] = m1_ndf()
                            self.get_parameter("NoMDEntries")[band]["SettlType"] = "M1"

                    if published == False:
                        if band_not_pub == None:
                            self.get_parameter("NoMDEntries")[band]["MDQuoteType"] = "0"
                        else:
                            if qty != band_not_pub[row_pub]:
                                self.get_parameter("NoMDEntries")[band]["MDQuoteType"] = "1"
                            if qty == band_not_pub[row_pub]:
                                self.get_parameter("NoMDEntries")[band]["MDQuoteType"] = "0"
                                check_pub += 1

                    if priced == False:
                        if band_not_priced == None:
                            self.get_parameter("NoMDEntries")[band]["QuoteCondition"] = "B"
                        elif qty == band_not_priced[row_prc]:
                            self.get_parameter("NoMDEntries")[band]["QuoteCondition"] = "B"
                            check_price += 1

                    md_entry_type += 1
                    band += 1
                md_entry_position += 1
                row_pub += 1
                row_prc += 1

    def set_params_for_empty_md_response(self, md_request: FixMessageMarketDataRequestFX,
                                   no_md_entries_count: list = ["*", "*", "*"],
                                   published=True, ndf=False,
                                   priced=True, band_not_pub=None, band_not_priced=None, response=None):
        self.prepare_params_for_empty_md_response(md_request, response=response)
        if len(no_md_entries_count) > 0:
            # band = 0
            # row_pub = 0
            # row_prc = 0
            # check_pub = 0
            # check_price = 0
            self.remove_parameter("NoMDEntries")
            # self.get_parameter("NoMDEntries").clear()
            # md_entry_position = 1
            # for qty in no_md_entries_count:
            #     md_entry_type = 0
                # while md_entry_type < 2:
                #     self.get_parameter("NoMDEntries").append({
                #         "SettlType": md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
                #         "MDEntryTime": "*",
                #         "MDEntryID": "*",
                #         "QuoteEntryID": "*",
                #         "MDOriginType": "1",
                #         "MDQuoteType": "1",
                #         "MDEntryPositionNo": md_entry_position,
                #         "MDEntryDate": "*",
                #         "MDEntryType": md_entry_type
                #     })
                #     if md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "":
                #         self.get_parameter("NoMDEntries")[band]["SettlType"] = "0"
                #         self.get_parameter("NoMDEntries")[band]["SettlDate"] = spo()
                #     elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "0":
                #         self.get_parameter("NoMDEntries")[band]["SettlType"] = "0"
                #         self.get_parameter("NoMDEntries")[band]["SettlDate"] = spo()
                #     if md_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["SecurityType"] == "FXFWD":
                #         self.get_parameter("NoMDEntries")[band]["MDEntryForwardPoints"] = "*"
                #         self.get_parameter("NoMDEntries")[band]["MDEntrySpotRate"] = "*"
                #         if md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "1":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "1"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = today()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "2":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "2"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = tom()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W1":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "W1"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk1()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W2":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "W2"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk2()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W3":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "W3"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk3()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "M1":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "M1"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = m1()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "1":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "1"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = today()
                #         # TODO add more SettleType`s
                #     if ndf is not False:
                #         if md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "1":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "1"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = today()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "2":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "2"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = tom()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "0"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = spo_ndf()
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "0":
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "0"
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = spo_ndf()
                #     if md_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["SecurityType"] == "FXNDF":
                #         self.get_parameter("NoMDEntries")[band]["MDEntryForwardPoints"] = "*"
                #         self.get_parameter("NoMDEntries")[band]["MDEntrySpotRate"] = "*"
                #         if md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W1":
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk1_ndf()
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "W1"
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W2":
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk2_ndf()
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "W2"
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "W3":
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = wk3_ndf()
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "W3"
                #         elif md_request.get_parameter("NoRelatedSymbols")[0]["SettlType"] == "M1":
                #             self.get_parameter("NoMDEntries")[band]["SettlDate"] = m1_ndf()
                #             self.get_parameter("NoMDEntries")[band]["SettlType"] = "M1"
                #
                #     if published == False:
                #         if band_not_pub == None:
                #             self.get_parameter("NoMDEntries")[band]["MDQuoteType"] = "0"
                #         else:
                #             if qty != band_not_pub[row_pub]:
                #                 self.get_parameter("NoMDEntries")[band]["MDQuoteType"] = "1"
                #             if qty == band_not_pub[row_pub]:
                #                 self.get_parameter("NoMDEntries")[band]["MDQuoteType"] = "0"
                #                 check_pub += 1
                #
                #     if priced == False:
                #         if band_not_priced == None:
                #             self.get_parameter("NoMDEntries")[band]["QuoteCondition"] = "B"
                #         elif qty == band_not_priced[row_prc]:
                #             band_not_priced["NoMDEntries"][band]["QuoteCondition"] = "B"
                #             check_price += 1
                #
                #     md_entry_type += 1
                #     band += 1
                # md_entry_position += 1
                # if check_pub != 0:
                #     row_pub += 1
                # if check_price != 0:
                #     row_prc += 1

    def set_params_for_md_response_taker_spo(self, md_request: FixMessageMarketDataRequestFX,
                                             no_md_entries_count: list):
        self.prepare_params_for_md_response(md_request)
        if len(no_md_entries_count) > 0:
            self.get_parameter("NoMDEntries").clear()
            for qty in no_md_entries_count:
                md_entry_type = 0
                while md_entry_type < 2:
                    self.get_parameter("NoMDEntries").append({
                        "MDEntryPx": "*",
                        "MDEntrySize": qty,
                        "OrdType": "2",
                        "SettlDate": spo(),
                        "SettlType": "0",
                        "MDQuoteType": "*",
                        "MDEntryType": "*",

                    })
                    md_entry_type += 1

    def set_params_for_md_response_taker_wk1(self, md_request: FixMessageMarketDataRequestFX,
                                             no_md_entries_count: list):
        self.prepare_params_for_md_response(md_request)
        if len(no_md_entries_count) > 0:
            self.get_parameter("NoMDEntries").clear()
            for qty in no_md_entries_count:
                md_entry_type = 0
                while md_entry_type < 2:
                    self.get_parameter("NoMDEntries").append({
                        "MDEntryPx": "*",
                        "MDEntrySize": qty,
                        "OrdType": "2",
                        "SettlDate": wk1(),
                        "MDQuoteType": "*",
                        "MDEntryType": "*",

                    })
                    md_entry_type += 1

    def set_params_for_md_response_taker_bda(self, md_request: FixMessageMarketDataRequestFX,
                                             no_md_entries_count: list):
        self.prepare_params_for_md_response(md_request)
        if len(no_md_entries_count) > 0:
            self.get_parameter("NoMDEntries").clear()
            for qty in no_md_entries_count:
                md_entry_type = 0
                while md_entry_type < 2:
                    self.get_parameter("NoMDEntries").append({
                        "MDEntryPx": "*",
                        "MDEntrySize": qty,
                        "OrdType": "2",
                        "SettlType": "B",
                        "SettlDate": md_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
                        "MDQuoteType": "*",
                        "MDEntryForwardPoints": "*",
                        "MDEntrySpotRate": "*",
                        "MDEntryType": "*",

                    })
                    md_entry_type += 1

    def prepare_params_for_md_response(self, md_request: FixMessageMarketDataRequestFX, response=None):
        temp = dict(
            MDReqID=md_request.get_parameter("MDReqID"),
            OrigMDArrivalTime="*",
            LastUpdateTime="*",
            OrigClientVenueID="*",
            OrigMDTime="*",
            Instrument=dict(Symbol=md_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"]),
            NoMDEntries=[
                dict()
            ]
        )
        if response:
            if "CachedUpdate" in response.get_parameters():
                temp.update({"CachedUpdate": "Y"})
            else:
                if "CachedUpdate" in self.get_parameters():
                    self.get_parameters().pop("CachedUpdate")
        if "MarketID" in md_request.get_parameters()["NoRelatedSymbols"][0].keys():
            temp.update({"MarketID": md_request.get_parameters()["NoRelatedSymbols"][0]["MarketID"]})
            temp.update({"MDStreamID": "*"})
            temp.update({"MDBookType": "*"})
            temp['Instrument'].update({"CFICode": md_request.get_parameters()["NoRelatedSymbols"][0]["MarketID"]})
            temp.pop('OrigClientVenueID')
        super().change_parameters(temp)
        return self

    def prepare_params_for_empty_md_response(self, md_request: FixMessageMarketDataRequestFX, response=None):
        temp = dict(
            MDReqID=md_request.get_parameter("MDReqID"),
            LastUpdateTime="*",
            Instrument=dict(Symbol=md_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"]),
            NoMDEntries=[
                dict()
            ]
        )
        orig_tags_to_remove = ["OrigMDArrivalTime", "OrigClientVenueID", "OrigMDTime"]
        for i in orig_tags_to_remove:
            if i in self.get_parameters():
                self.get_parameters().pop(i)
        if response:
            if "CachedUpdate" in response.get_parameters():
                temp.update({"CachedUpdate": "Y"})
        if "MarketID" in md_request.get_parameters()["NoRelatedSymbols"][0].keys():
            temp.update({"MarketID": md_request.get_parameters()["NoRelatedSymbols"][0]["MarketID"]})
            temp.update({"MDStreamID": "*"})
            temp.update({"MDBookType": "*"})
            temp['Instrument'].update({"CFICode": md_request.get_parameters()["NoRelatedSymbols"][0]["MarketID"]})
        super().change_parameters(temp)
        return self
