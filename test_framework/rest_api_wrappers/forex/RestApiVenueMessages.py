from test_framework.data_sets.message_types import ResAPIMessageType
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiAutoHedgerMessages(RestApiMessages):
    def set_default_params(self):
        self.parameters = {
            "tradingStatus": "T",
            "GTDHolidayCheck": "false",
            "algoIncluded": "true",
            "supportBrokerQueue": "false",
            "supportStatus": "false",
            "supportQuoteBook": "false",
            "MIC": "BARX",
            "supportOrderBook": "false",
            "supportReverseCalSpread": "false",
            "timeZone": "Eastern Standard Time",
            "venueName": "BARX",
            "venueShortName": "BARX",
            "MDSource": "TEST",
            "shortTimeZone": "EST",
            "quoteTTL": 90,
            "tradingPhase": "OPN",
            "clOrdIDFormat": "#20d",
            "supportIntradayData": "false",
            "tradingPhaseProfileID": 123,
            "supportPublicQuoteReq": "true",
            "venueID": "BARX",
            "supportMarketDepth": "true",
            "supportTrade": "false",
            "venueVeryShortName": "H",
            "settlementRank": 7,
            "feedSource": "QUOD",
            "quoteReqTTL": 90,
            "clientVenueID": "BARX",
            "supportMovers": "false",
            "supportQuote": "false",
            "defaultMDSymbol": "BARX",
            "supportTimesAndSales": "false",
            "supportTickers": "false",
            "routeVenueID": "BARX",
            "venueType": "LIT",
            "supportNews": "false",
            "supportMarketTime": "false",
            "holdFIXShortSell": "false",
            "regulatedShortSell": "false",
            "generateBidOfferID": "false",
            "generateQuoteMsgID": "false",
            "supportTermQuoteRequest": "false",
            "supportQuoteCancel": "true",
            "supportSizedMDRequest": "false",
            "venueQualifier": "ESP",
            "supportDiscretionInst": "false",
            "supportBrokenDateFeed": "false",
            "venueOrdCapacity": [
                {
                    "ordCapacity": "A"
                },
                {
                    "ordCapacity": "W"
                },
                {
                    "ordCapacity": "O"
                },
                {
                    "ordCapacity": "I"
                },
                {
                    "ordCapacity": "P"
                },
                {
                    "ordCapacity": "G"
                },
                {
                    "ordCapacity": "R"
                }
            ],
            "venuePhaseSession": [
                {
                    "supportMinQty": "false",
                    "tradingPhase": "OPN",
                    "tradingSession": "NotD",
                    "venuePhaseSessionTypeTIF": [
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "FOK",
                            "ordType": "LMT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "GTD",
                            "ordType": "LMT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "ATC",
                            "ordType": "LMT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "GTC",
                            "ordType": "LMT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "DAY",
                            "ordType": "LMT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "ATO",
                            "ordType": "LMT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "IOC",
                            "ordType": "LMT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "GTX",
                            "ordType": "LMT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "IOC",
                            "ordType": "MKT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "ATO",
                            "ordType": "MKT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "DAY",
                            "ordType": "MKT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "GTC",
                            "ordType": "MKT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "ATC",
                            "ordType": "MKT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "GTD",
                            "ordType": "MKT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "FOK",
                            "ordType": "MKT"
                        },
                        {
                            "supportDisplayQty": "false",
                            "timeInForce": "GTX",
                            "ordType": "MKT"
                        }
                    ],
                    "venuePhaseSessionPegPriceType": []
                }
            ]
        }

    def find_all_venue(self):
        self.clear_message_params()
        self.message_type = ResAPIMessageType.FindAllVenue.value
        return self

    def create_venue(self):
        self.message_type = ResAPIMessageType.CreateVenue.value
        return self

    def modify_venue(self):
        self.message_type = ResAPIMessageType.ModifyVenue.value
        return self
