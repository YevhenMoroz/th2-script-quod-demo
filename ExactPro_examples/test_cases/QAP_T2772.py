import logging
import time

from th2_grpc_act_gui_quod.act_ui_win_pb2 import VenueStatusesRequest
from th2_grpc_act_gui_quod.ar_operations_pb2 import ExtractOrderTicketValuesRequest, ExtractDirectVenueExecutionRequest

from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, ContextActionType
from win_gui_modules.application_wrappers import CloseApplicationRequest
from win_gui_modules.wrappers import set_base
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ExtractRatesTileTableValuesRequest
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import set_session_id, get_base_request, call, close_fe, prepare_fe303


class TestCase:
    def __init__(self, report_id, session_id):
        # Logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.common_act = Stubs.win_act
        self.ar_service = Stubs.win_act_aggregated_rates_service
        self.cp_service = Stubs.win_act_cp_service
        self.ob_act = Stubs.win_act_order_book

        # Case parameters setup
        self.case_id = bca.create_event('QAP_T2772', report_id)
        self.session_id = session_id
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.tile_1 = BaseTileDetails(base=self.base_request, window_index=0)
        self.tile_2 = BaseTileDetails(base=self.base_request, window_index=1)

        self.venue = 'BARX'
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
        self.api.sendMessage(
            request=SubmitMessageRequest(message=bca.message_to_grpc('ModifyVenue', modify_params, 'rest_wa314luna'),
                                         parent_event_id=self.case_id))

        modify_venue_params = {
            "venueID": "BARX",
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
            request=SubmitMessageRequest(
                message=bca.message_to_grpc('ModifyVenueStatus', modify_venue_params, 'rest_wa314luna'),
                parent_event_id=self.case_id)
        )
        # print(bca.message_to_grpc('ModifyVenueStatus', modify_venue_params,'rest_wa303'))

    # # FE open method
    # def prepare_frontend(self):
    #     work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
    #     password = Stubs.custom_config['qf_trading_fe_password_303']
    #     prepare_fe303(self.case_id, self.session_id, work_dir, self.user, password)

    def check_venue_status(self, venue, status):
        request = VenueStatusesRequest(base=self.base_request, filter={"Name": venue})
        result = call(self.common_act.checkVenueStatuses, request)
        if '#E23642' in result['colors']:
            result = 'unhealthy'
        elif '#E2E9E5' in result['colors']:
            result = 'healthy'
        verifier = Verifier(self.case_id)
        verifier.set_event_name(f"Check {venue} in Venue Status")
        verifier.compare_values("Checked", result, status)
        verifier.verify()
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

    # extract rates tile table values
    def check_venues_in_order_ticket(self, tile, venue, status):
        order_ticket_checking = ExtractOrderTicketValuesRequest(data=tile.build())
        order_ticket_checking.side = ExtractOrderTicketValuesRequest.Side.BID
        order_ticket_checking.venueToExtract = venue
        result = call(self.ar_service.extractRatesOrderTicketValues, order_ticket_checking)

        verifier = Verifier(self.case_id)
        verifier.set_event_name(f"Check {venue} in order ticket")
        verifier.compare_values("Checked", result[f'{venue}_checked'], status)
        verifier.verify()

    # extract rates tile table values
    def check_venues_in_dve(self, tile, venue, method):
        dve = ExtractDirectVenueExecutionRequest(data=tile.build())
        dve.extractBidSide = True
        dve.extractAskSide = True
        dve.venueToExtract = venue
        result = call(self.ar_service.extractDirectVenueExecutionValues, dve)

        verifier = Verifier(self.case_id)
        verifier.set_event_name(f"Check {venue} in DVE")
        verifier.compare_values("Bid Price", result['bid_price'], "", verification_method=method)
        verifier.compare_values("Ask Price", result['ask_price'], "", verification_method=method)
        verifier.verify()

    # extract rates tile table values
    def check_venues_in_esp_table(self, tile, venue, status):
        extract_table_request = ExtractRatesTileTableValuesRequest(details=tile)
        extract_table_request.set_extraction_id("ExtractionId1")
        extract_table_request.check_venue_to_present(venue)
        result = call(self.ar_service.extractESPAggrRatesTableValues, extract_table_request.build())

        verifier = Verifier(self.case_id)
        verifier.set_event_name(f"Check {venue} in ESP table")
        verifier.compare_values(f"{venue} exists", result[f'{venue}_exists'], status)
        verifier.verify()

    def save_and_close_fe_workspace(self):
        # Close the FrontEnd and safe workspace
        close_app_request = CloseApplicationRequest()
        close_app_request.set_default_params(self.base_request)
        close_app_request.save_workspace()
        self.common_act.closeApplication(close_app_request.build())

    # Main method
    def execute(self):
        try:
            self.set_venue_unhealthy("true")
            # self.prepare_frontend()
            self.check_venue_status(self.venue, 'unhealthy')
            self.create_or_get_rates_tile(self.tile_1)
            self.check_unhealthy_venues(self.tile_1)
            self.check_unhealthy_venues(self.tile_2)

            self.check_venues_in_order_ticket(self.tile_1, self.venue + 'C', 'false')
            self.check_venues_in_dve(self.tile_2, self.venue, VerificationMethod.EQUALS)
            self.check_venues_in_esp_table(self.tile_1, self.venue, 'false')

            self.check_unhealthy_venues(self.tile_1)
            self.check_unhealthy_venues(self.tile_2)

            self.check_venues_in_order_ticket(self.tile_1, self.venue + 'C', 'true')
            self.check_venues_in_dve(self.tile_2, self.venue, VerificationMethod.NOT_EQUALS)
            self.check_venues_in_esp_table(self.tile_1, self.venue, 'true')

            self.save_and_close_fe_workspace()
            self.prepare_frontend()

            self.check_venues_in_order_ticket(self.tile_1, self.venue + 'C', 'true')
            self.check_venues_in_dve(self.tile_2, self.venue, VerificationMethod.NOT_EQUALS)
            self.check_venues_in_esp_table(self.tile_1, self.venue, 'true')

            self.set_venue_unhealthy("false")
            self.check_venue_status(self.venue, 'healthy')

        except Exception as e:
            logging.error('Error execution', exc_info=True)
        # close_fe(self.case_id, self.session_id)
