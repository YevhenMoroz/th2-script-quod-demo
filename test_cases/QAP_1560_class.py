import logging
from datetime import datetime
from stubs import Stubs
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe_2
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ModifyRatesTileRequest,\
    ExtractRatesTileTableValuesRequest, ExtractRatesTileValues

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID


class TestCase:
    # Initialization
    def __init__(self, report_id):
        # Logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.common_act = Stubs.win_act
        self.fix_act = Stubs.fix_act
        self.verifier = Stubs.verifier
        self.simulator = Stubs.simulator
        self.cp_service = Stubs.win_act_cp_service

        # Case parameters setup
        self.case_id = bca.create_event('QAP-1560', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.case_base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.case_base_request)

        self.md_req_id_fe = bca.client_orderid(10)
        self.client = 'fix-qsesp-303'
        self.provider = 'fix-fh-fx-esp'
        self.settl_date = tsd.spo()
        self.case_instrument = {
            'Symbol': 'EUR/USD',
            'Product': '4',
            'SecurityType': 'FXSPOT'
        }

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        username = Stubs.custom_config['qf_trading_fe_user_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        try:
            if not Stubs.frontend_is_open:
                prepare_fe(self.case_id, self.session_id, work_dir, username, password)
                call(self.cp_service.createRatesTile, self.base_details.build())
        except Exception as e:
            logging.error('Error execution', exc_info=True)

    # Send MarketData precondition method
    def send_md_precondition(self):
        # MarketData parameters
        md_params = {
            'MDReqID':
                self.simulator.getMDRefIDForConnection303(request=
                                                          RequestMDRefID(symbol=
                                                                         'EUR/USD:SPO:REG:HSBC',
                                                                         connection_id=
                                                                         ConnectionID(session_alias=
                                                                                      self.provider))).MDRefID,
            'Instrument': {
                'Symbol': self.case_instrument['Symbol'],
                'SecurityType': self.case_instrument['SecurityType']
            },
            'NoMDEntries': [
                {
                    'MDEntryType': '1',
                    'MDEntryPx': 35.0,
                    'MDEntrySize': 1000000,
                    'MDEntryPositionNo': 1,
                    'MDEntrySpotRate': 1.18,
                    'MDEntryForwardPoints': 0.0002,
                    'SettlDate': self.settl_date,
                    'MDEntryDate': datetime.utcnow().strftime('%Y-%m-%d'),
                    'MDEntryTime': datetime.utcnow().strftime('%H:%M:%S'),
                },
                {
                    'MDEntryType': '0',
                    'MDEntryPx': 35.5,
                    'MDEntrySize': 1000000,
                    'MDEntryPositionNo': 1,
                    'MDEntrySpotRate': 1.17,
                    'MDEntryForwardPoints': 0.0002,
                    'SettlDate': self.settl_date,
                    'MDEntryDate': datetime.utcnow().strftime('%Y-%m-%d'),
                    'MDEntryTime': datetime.utcnow().strftime('%H:%M:%S'),
                }
            ]
        }

        # Send MarketData via FIX
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send MDU (Precondition)',
                self.provider,
                self.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', md_params, self.provider)
            ))

    # Send MarketDataRequest subscribe method
    def send_md_subscribe(self):
        # MarketDataRequest parameters
        md_params = {
            'SenderSubID': 'MMCLIENT1',
            'MDReqID': self.md_req_id_fe,
            'SubscriptionRequestType': '1',
            'MarketDepth': '0',
            'MDUpdateType': '0',
            'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
            'NoRelatedSymbols': [
                {
                    'Instrument': self.case_instrument,
                    'SettlDate': self.settl_date
                }
            ]
        }

        # Send MarketDataRequest via FIX
        subscribe = self.fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                'Send MDR (subscribe)',
                self.client,
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', md_params, self.client)
            ))

        # MarketDataRequest response parameters
        md_subscribe_response = {
            'MDReqID': md_params['MDReqID'],
            'Instrument': {
                'Symbol': self.case_instrument['Symbol']
            },
            'LastUpdateTime': '*',
            'OrigMDArrivalTime': '*',
            'OrigMDTime': '*',
            'MDTime': '*',
            'NoMDEntries': [
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': 1000000,
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': 1000000,
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 2,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 2,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 3,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 3,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                }
            ]
        }

        # Check MarketDataRequest response via FIX
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive MarketDataSnapshotFullRefresh (pending)',
                bca.filter_to_grpc('MarketDataSnapshotFullRefresh', md_subscribe_response, ['MDReqID']),
                subscribe.checkpoint_id,
                self.client,
                self.case_id
            )
        )

        # Return MarketDataRequest params for unsubscribe in future
        return md_params

    # Send MarketDataSnapshot method
    def send_md_update(self, bid_price, ack_price):
        # MarketDataSnapshot parameters
        md_params = {
            'MDReqID':
                self.simulator.getMDRefIDForConnection303(request=
                                                          RequestMDRefID(symbol=
                                                                         'EUR/USD:SPO:REG:HSBC',
                                                                         connection_id=
                                                                         ConnectionID(
                                                                             session_alias=
                                                                             self.provider))).MDRefID,
            'Instrument': {
                'Symbol': self.case_instrument['Symbol'],
                'SecurityType': self.case_instrument['SecurityType']
            },
            'NoMDEntries': [
                {
                    'MDEntryType': '1',
                    'MDEntryPx': ack_price,
                    'MDEntrySize': 1000000,
                    'MDEntryPositionNo': 1,
                    'MDEntrySpotRate': 1.18,
                    'MDEntryForwardPoints': 0.0002,
                    'SettlDate': self.settl_date,
                    'MDEntryDate': datetime.utcnow().strftime('%Y-%m-%d'),
                    'MDEntryTime': datetime.utcnow().strftime('%H:%M:%S'),
                },
                {
                    'MDEntryType': '0',
                    'MDEntryPx': bid_price,
                    'MDEntrySize': 1000000,
                    'MDEntryPositionNo': 1,
                    'MDEntrySpotRate': 1.17,
                    'MDEntryForwardPoints': 0.0002,
                    'SettlDate': self.settl_date,
                    'MDEntryDate': datetime.utcnow().strftime('%Y-%m-%d'),
                    'MDEntryTime': datetime.utcnow().strftime('%H:%M:%S'),
                }
            ]
        }

        # Send MarketDataSnapshot via FIX
        md_update = self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send MDU',
                self.provider,
                self.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', md_params, self.provider)
            ))

        # MarketDataSnapshot response parameters
        md_response = {
            'MDReqID': self.md_req_id_fe,
            'Instrument': {
                'Symbol': self.case_instrument['Symbol']
            },
            'LastUpdateTime': '*',
            'OrigMDArrivalTime': '*',
            'OrigMDTime': '*',
            'MDTime': '*',
            'NoMDEntries': [
                {
                    'SettlType': 0,
                    'MDEntryPx': bid_price,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': 1000000,
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryPx': ack_price,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': 1000000,
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 2,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 2,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 3,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.settl_date,
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 3,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                }
            ]
        }

        # Check MarketDataSnapshot response via FIX
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive MarketDataSnapshotFullRefresh (pending)',
                bca.filter_to_grpc('MarketDataSnapshotFullRefresh', md_response, ['MDReqID']),
                md_update.checkpoint_id,
                self.client,
                self.case_id
            )
        )

    # Send MarketDataRequest unsubscribe method
    def send_md_unsubscribe(self, md_params):
        # Change MarketDataRequest from 'Subscribe' to 'Unsubscribe'
        md_params['SubscriptionRequestType'] = '2'
        # Send MarketDataRequest via FIX
        self.fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                'Send MDR (unsubscribe)',
                self.client,
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', md_params, self.client)
            ))

    # Widen spread method. NOT TESTED
    def widen_spread(self, ex_id1, ex_id2):
        # Extract current values
        extract_table_request = ExtractRatesTileTableValuesRequest(details=self.base_details)
        extract_table_request.set_extraction_id(ex_id1)
        extract_table_request.set_row_number(1)
        ask_field_start = ExtractionDetail('rateTile.Px', 'Px')
        extract_table_request.set_ask_extraction_field(ask_field_start)
        bid_field_start = ExtractionDetail('rateTile.Px', 'Px')
        extract_table_request.set_bid_extraction_field(bid_field_start)
        call(self.cp_service.extractRatesTileTableValues, extract_table_request.build())

        # Widen spread
        modify_request = ModifyRatesTileRequest(details=self.base_details)
        modify_request.widen_spread()
        call(self.cp_service.modifyRatesTile, modify_request.build())

        # Extract new values
        extract_table_request = ExtractRatesTileTableValuesRequest(details=self.base_details)
        extract_table_request.set_extraction_id(ex_id2)
        extract_table_request.set_row_number(1)
        ask_field_end = ExtractionDetail('rateTile.Px', 'Px')
        extract_table_request.set_ask_extraction_field(ask_field_end)
        bid_field_end = ExtractionDetail('rateTile.Px', 'Px')
        extract_table_request.set_bid_extraction_field(bid_field_end)
        call(self.cp_service.extractRatesTileTableValues, extract_table_request.build())

        # Verify values
        # Setup verify!!!
        call(self.common_act.verifyEntities, verification(ex_id2, 'checking prices (GUI. Before vs After)',
                                                     [verify_ent('Ask field', ask_field_end.name, ask_field_start.name),
                                                      verify_ent('Bid field', bid_field_end.name, bid_field_end.name)]))

    # Check GUI changes method. NOT TESTED
    def check_fe_prices(self, ex_id, bid_price, ack_price):
        extract_request = ExtractRatesTileValues(details=self.base_details)
        ask_gui = extract_request.extract_ask_large_value('ratesTile.askLargeValue')
        bid_gui = extract_request.extract_bid_large_value('ratesTile.bidLargeValue')
        extract_request.set_extraction_id(ex_id)
        call(self.cp_service.extractRateTileValues, extract_request.build())

        call(self.common_act.verifyEntities, verification(ex_id, 'checking prices (GUI vs FIX)',
                                                          [verify_ent('Ask field', ask_gui.name, bid_price),
                                                           verify_ent('Bid field', bid_gui.name, ack_price)]))

    # Reset spread method. NOT TESTED
    def set_default_spread(self):
        modify_request = ModifyRatesTileRequest(details=self.base_details)
        modify_request.press_use_defaults()
        call(self.cp_service.modifyRatesTile, modify_request.build())

    def execute(self):
        try:
            bid, ack = 45.0, 46.2
            # Step 0
            self.send_md_precondition()
            # Step 1
            market_data_params = self.send_md_subscribe()
            ## Step 2
            # self.prepare_frontend()
            # self.widen_spread('WS1_0', 'WS1_1')
            # Steps 3-5
            self.send_md_update(bid, ack)
            # # self.check_fe_prices('CP1', bid, ack)
            # ## Step 6
            # # self.set_default_spread()
            # ## Steps 7-9
            bid, ack = 32.1, 33.4
            self.send_md_update(bid, ack)
            # # self.check_fe_prices('CP2', bid, ack)
            self.send_md_unsubscribe(market_data_params)
            close_fe_2(self.case_id, self.session_id)

        except Exception as e:
            logging.error('Error execution', exc_info=True)


if __name__ == '__main__':
    pass
