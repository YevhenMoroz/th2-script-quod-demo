import logging
from stubs import Stubs
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe_2
from win_gui_modules.wrappers import set_base
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ModifyRatesTileRequest, \
    ExtractRatesTileTableValuesRequest, ExtractRatesTileValues


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
        self.cp_service = Stubs.win_act_cp_service

        # Case parameters setup
        self.case_id = bca.create_event('QAP-1560', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.md_req_id_fe = bca.client_orderid(10)
        self.client = 'fix-qsesp-303'
        self.provider = 'fix-fh-fx-esp'
        self.settl_date = tsd.spo()
        self.case_instrument = {
            'Symbol': 'EUR/USD',
            'Product': '4',
            'SecurityType': 'FXSPOT'
        }

        # Last checkpoint. Need in the future for check MD via FIX
        self.last_checkpoint = None

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        username = Stubs.custom_config['qf_trading_fe_user_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        if not Stubs.frontend_is_open:
            prepare_fe(self.case_id, self.session_id, work_dir, username, password)
            call(self.cp_service.createRatesTile, self.base_details.build())

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
            'NoMDEntries': [
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
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
                    'MDEntrySize': '*',
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

    # Send MarketDataRequest unsubscribe method
    def send_md_unsubscribe(self, md_params):
        # Change MarketDataRequest from 'Subscribe' to 'Unsubscribe'
        md_params['SubscriptionRequestType'] = '2'
        # Send MarketDataRequest via FIX
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send MDR (unsubscribe)',
                self.client,
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', md_params, self.client)
            ))

    # Extract prices from GUI
    def extract_prices(self):
        extract_request = ExtractRatesTileValues(details=self.base_details)
        extract_request.extract_ask_large_value("ratesTile.askLargeValue")
        extract_request.extract_bid_large_value("ratesTile.bidLargeValue")
        extract_request.set_extraction_id("extrId0")
        data_tile = call(self.cp_service.extractRateTileValues, extract_request.build())

        extract_table_request = ExtractRatesTileTableValuesRequest(details=self.base_details)
        extract_table_request.set_extraction_id("extrId1")
        extract_table_request.set_row_number(1)
        extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.AskPx", "Px"))
        extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.BidPx", "Px"))
        data_table = call(self.cp_service.extractRatesTileTableValues, extract_table_request.build())

        return float(data_tile["ratesTile.askLargeValue"] + data_table["rateTile.AskPx"]), \
               float(data_tile["ratesTile.bidLargeValue"] + data_table["rateTile.BidPx"])

    # Update last checkpoint method
    def get_last_checkpoint(self):
        self.last_checkpoint = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(self.case_id)).checkpoint

    # Decrease bid method
    def decrease_bid(self):
        self.get_last_checkpoint()
        modify_request = ModifyRatesTileRequest(details=self.base_details)
        modify_request.decrease_bid()
        call(self.cp_service.modifyRatesTile, modify_request.build())

    # Press defaults button method
    def use_defaults(self):
        self.get_last_checkpoint()
        modify_request = ModifyRatesTileRequest(details=self.base_details)
        modify_request.press_use_defaults()
        call(self.cp_service.modifyRatesTile, modify_request.build())

    # Check prices via Fix method
    def check_fix_prices(self, ask_px, bid_px):
        # MarketDataSnapshot response parameters
        md_response = {
            'MDReqID': self.md_req_id_fe,
            'Instrument': {
                'Symbol': self.case_instrument['Symbol']
            },
            'LastUpdateTime': '*',
            'NoMDEntries': [
                {
                    'SettlType': 0,
                    'MDEntryPx': bid_px,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
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
                    'MDEntryPx': ask_px,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
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
                self.last_checkpoint,
                self.client,
                self.case_id
            )
        )

    def execute(self):
        try:
            # Step 1
            market_data_params = self.send_md_subscribe()
            self.prepare_frontend()
            # Step 2
            self.decrease_bid()
            # Steps 3-5
            ask, bid = self.extract_prices()
            self.check_fix_prices(ask, bid)
            # Step 6
            self.use_defaults()
            # Steps 7-9
            ask, bid = self.extract_prices()
            self.check_fix_prices(ask, bid)

            self.send_md_unsubscribe(market_data_params)
            close_fe_2(self.case_id, self.session_id)

        except Exception as e:
            logging.error('Error execution', exc_info=True)


if __name__ == '__main__':
    pass
