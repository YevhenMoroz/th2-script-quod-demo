import logging

from custom.verifier import Verifier
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRatesTileRequest, \
    ExtractRatesTileDataRequest, PlaceESPOrder, ESPTileOrderSide, ContextActionRatesTile, ContextActionType
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ExtractRatesTileTableValuesRequest, \
    ExtractRatesTileValues
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe, get_opened_fe, \
    prepare_fe303, get_opened_fe_303


class TestCase:
    def __init__(self, report_id):
        # Logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.common_act = Stubs.win_act
        self.ar_service = Stubs.win_act_aggregated_rates_service
        self.cp_service = Stubs.win_act_cp_service
        self.ob_act = Stubs.win_act_order_book

        # Case parameters setup
        self.case_id = bca.create_event('QAP-2715', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.tile_1 = BaseTileDetails(base=self.base_request, window_index=0)
        self.tile_2 = BaseTileDetails(base=self.base_request, window_index=1)

        self.venue = 'HSB'
        self.user = Stubs.custom_config['qf_trading_fe_user_303']
        self.quote_id = None
        self.api = Stubs.api_service

    def set_venue_unhealthy(self, health):
        modify_params = {
            "tradingStatus": "T",
            "GTDHolidayCheck": "false",
            "algoIncluded": "true",
            "supportBrokerQueue": "false",
            "supportStatus": "false",
            "supportQuoteBook": "false",
            "MIC": "HSBC",
            "supportOrderBook": "false",
            "supportReverseCalSpread": "false",
            "timeZone": "Eastern Standard Time",
            "venueName": "HSBC",
            "venueShortName": "HSB",
            "MDSource": "TEST",
            "shortTimeZone": "EST",
            "quoteTTL": 90,
            "tradingPhase": "OPN",
            "clOrdIDFormat": "#20d",
            "supportIntradayData": "false",
            "tradingPhaseProfileID": 123,
            "supportPublicQuoteReq": "true",
            "venueID": "HSBC",
            "supportMarketDepth": "true",
            "supportTrade": "false",
            "venueVeryShortName": "H",
            "settlementRank": 7,
            "feedSource": "QUOD",
            "quoteReqTTL": 90,
            "clientVenueID": "HSBC",
            "supportMovers": "false",
            "supportQuote": "false",
            "defaultMDSymbol": "HSBC",
            "supportTimesAndSales": "false",
            "supportTickers": "false",
            "routeVenueID": "HSBC",
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
        nos_response = self.api.sendMessage(
            request=SubmitMessageRequest(message=bca.message_to_grpc('ModifyVenue', modify_params, 'rest_wa303'),
                                         parent_event_id=self.case_id)
            )
        # print(bca.message_to_grpc('ModifyVenueStatus', modify_params,'rest_wa303'))

        modify_venue_params = {
            "venueID": "HSBC",
            "alive": 'true',
            "venueStatusMetric": [
                {
                    "venueMetricType": "LUP",
                    "enableMetric": health,
                    "metricErrorThreshold": -1,
                    "metricWarningThreshold": -1
                }
            ]
        }
        nos_response = self.api.sendMessage(
            request=SubmitMessageRequest(message=bca.message_to_grpc('ModifyVenueStatus', modify_venue_params, 'rest_wa303'),
                                         parent_event_id=self.case_id)
            )
        # print(bca.message_to_grpc('ModifyVenueStatus', modify_venue_params,'rest_wa303'))

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        # get_opened_fe_303(self.case_id, self.session_id)
        prepare_fe303(self.case_id, self.session_id, work_dir, self.user, password)

    def create_or_get_rates_tile(self, tile):
        call(self.ar_service.createRatesTile, tile.build())

    def check_unhealthy_venues(self, tile):
        modify_request = ModifyRatesTileRequest(details=tile)
        action = ContextActionRatesTile().add_context_action_type(
            [ContextActionType.CHECK_EXCLUDE_UNHEALTHY_VENUES.value], tile)
        modify_request.add_context_action(action)
        call(self.ar_service.modifyRatesTile, modify_request.build())

    def modify_rates_tile(self, qty):
        modify_request = ModifyRatesTileRequest(details=self.base_details)
        modify_request.set_quantity(qty)
        call(self.ar_service.modifyRatesTile, modify_request.build())

    def Check_rates_tile_table_values(self, row, bid, ask):
        extract_table_request = ExtractRatesTileTableValuesRequest(details=self.base_details)
        extract_table_request.set_extraction_id("extrId1")
        extract_table_request.set_row_number(row)
        extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.AskPx", "Px"))
        extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.BidPx", "Px"))
        data_table = call(self.ar_service.extractESPAggrRatesTableValues, extract_table_request.build())
        verifier = Verifier(self.case_id)
        verifier.set_event_name("Checking RatesTile Details")
        verifier.compare_values("best bid", data_table["rateTile.BidPx"], bid)
        verifier.compare_values("best ask", data_table["rateTile.AskPx"], ask)
        verifier.verify()

        return data_table

    def check_order_ticket(self, qty, side, check):
        ticket = 'OrderTicket'
        esp_request = PlaceESPOrder(details=self.base_details)
        if side == 'buy':
            esp_request.set_action(ESPTileOrderSide.BUY)
        else:
            esp_request.set_action(ESPTileOrderSide.SELL)
        esp_request.top_of_book(True)
        esp_request.close_ticket(True)
        esp_request.extract_quantity(f'{ticket}.qty')
        esp_request.extract_pips(f'{ticket}.pips')
        result = call(self.ar_service.placeESPOrder, esp_request.build())
        for k in result:
            print(f'{k} = {result[k]}')

    # Main method
    def execute(self):
        try:
            self.set_venue_unhealthy("true")
            # self.prepare_frontend()
            # # self.create_or_get_rates_tile(self.tile_1)
            # self.check_unhealthy_venues(self.tile_1)
            # self.check_unhealthy_venues(self.tile_2)

        except Exception as e:
            logging.error('Error execution', exc_info=True)
        # close_fe(self.case_id, self.session_id)

# if __name__ == '__main__':
#     pass
