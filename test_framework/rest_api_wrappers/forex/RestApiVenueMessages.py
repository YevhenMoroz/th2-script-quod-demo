from test_framework.data_sets.message_types import ResAPIMessageType
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiVenueMessages(RestApiMessages):
    def set_default_params(self):
        self.parameters = {
            "GTDHolidayCheck": "false",
            "MDSource": "PRICING.1",
            "MIC": "XQFX",
            "algoIncluded": "false",
            "alive": "true",
            "clOrdIDFormat": "#20d",
            "clQuoteReqIDFormat": "#20d",
            "clientVenueID": "XQFX",
            "closeTime": "00:00:00",
            "counterpartID": 3,
            "feedSource": "QUOD",
            "generateBidOfferID": "false",
            "generateQuoteMsgID": "false",
            "holdFIXShortSell": "false",
            "openTime": "00:00:00",
            "regulatedShortSell": "false",
            "routeVenueID": "QUODFX",
            "supportBrokenDateFeed": "true",
            "supportBrokerQueue": "false",
            "supportDiscretionInst": "false",
            "supportIntradayData": "false",
            "supportMarketDepth": "true",
            "supportMarketTime": "false",
            "supportMovers": "false",
            "supportNews": "false",
            "supportOrderBook": "false",
            "supportPublicQuoteReq": "false",
            "supportQuote": "false",
            "supportQuoteBook": "true",
            "supportQuoteCancel": "true",
            "supportReverseCalSpread": "false",
            "supportSizedMDRequest": "false",
            "supportStatus": "false",
            "supportTermQuoteRequest": "true",
            "supportTickers": "false",
            "supportTimesAndSales": "false",
            "supportTrade": "true",
            "tradingPhase": "OPN",
            "tradingStatus": "T",
            "venueCategory": "SBP",
            "venueID": "QUODFX",
            "venueName": "QUODFX"
        }

    def find_venue(self, venue):
        self.clear_message_params()
        self.message_type = 'FindVenue'
        self.parameters = {
            'URI':
                {
                    'queryID': venue
                }
        }
        return self

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
