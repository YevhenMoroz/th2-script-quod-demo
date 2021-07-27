import logging

from custom.verifier import Verifier
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRatesTileRequest, \
    ExtractRatesTileDataRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ExtractRatesTileTableValuesRequest, \
    ExtractRatesTileValues
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
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
        self.case_id = bca.create_event('QAP-2761', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.venue = 'HSB'
        self.user = Stubs.custom_config['qf_trading_fe_user_303']
        self.quote_id = None

        # Case rules
        self.rule_manager = RuleManager()
        self.RFQ = None
        self.TRFQ = None

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        # get_opened_fe_303(self.case_id, self.session_id)
        prepare_fe303(self.case_id, self.session_id, work_dir, self.user, password)

        # try:
        #     get_opened_fe_303(self.case_id, self.session_id, work_dir, self.user, password)
        # except Exception as e:
        #     logging.error('FE is not opened')
        #     prepare_fe303(self.case_id, self.session_id, work_dir, self.user, password)

    # send market data
    def send_market_data(self, qty):
        act = Stubs.fix_act
        event_store = Stubs.event_store
        simulator = Stubs.simulator

        mdu_params_hsbc = {
            "MDReqID": simulator.getMDRefIDForConnection303(
                request=RequestMDRefID(
                    symbol='EUR/USD:SPO:REG:HSBC',
                    connection_id=ConnectionID(session_alias="fix-fh-fx-esp"))).MDRefID,
            # "MDReportID": "1",
            # "MDTime": "TBU",
            # "MDArrivalTime": "TBU",
            # "OrigMDTime": "TBU",
            # "OrigMDArrivalTime": "TBU",
            # "ReplyReceivedTime": "TBU",
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT'
            },
            # "LastUpdateTime": "TBU",
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.12734,
                    "MDEntrySize": qty,
                    "MDEntryPositionNo": 1,
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.12618,
                    "MDEntrySize": qty + 2000000,
                    "MDEntryPositionNo": 2,
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.12592,
                    "MDEntrySize": qty + 8000000,
                    "MDEntryPositionNo": 3,
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.12784,
                    "MDEntrySize": qty,
                    "MDEntryPositionNo": 1,
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.12795,
                    "MDEntrySize": qty + 2000000,
                    "MDEntryPositionNo": 2,
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.12827,
                    "MDEntrySize": qty + 8000000,
                    "MDEntryPositionNo": 3,
                },
            ]
        }

        act.sendMessage(
            bca.convert_to_request(
                'Send MDU EUR/USD:SPO:REG:HSBC',
                'fix-fh-fx-esp',
                self.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_hsbc, 'fix-fh-fx-esp')
            ))

    def create_or_get_rates_tile(self):
        call(self.ar_service.createRatesTile, self.base_details.build())

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
        #esp_request.extract_large(f'{ticket}.large')
        esp_request.extract_pips(f'{ticket}.pips')
        result = call(self.ar_service.placeESPOrder, esp_request.build())

        cust_verifier = Verifier(self.case_id)
        cust_verifier.set_event_name('Checking OrderTicket for ' + side + ' side and Qty: ' + qty)
        cust_verifier.compare_values('OrderTicket pips', check, result[f'{ticket}.pips'])
        qty = qty[:-6] + ',' + qty[-6:-3] + ',' + qty[-3:]
        cust_verifier.compare_values('OrderTicket Qty', qty, result[f'{ticket}.qty'])
        cust_verifier.verify()
        for k in result:
            print(f'{k} = {result[k]}')

    # Main method
    def execute(self):
        try:
            qty_1 = '2000000'
            qty_2 = '7000000'
            self.prepare_frontend()
            self.create_or_get_rates_tile()
            self.send_market_data(1000000)
            self.Check_rates_tile_table_values(1, "734", "784")
            ask = self.Check_rates_tile_table_values(2, "618", "795")["rateTile.AskPx"]
            bid = self.Check_rates_tile_table_values(3, "592", "827")["rateTile.BidPx"]
            self.modify_rates_tile(qty_1)
            self.check_order_ticket(qty_1, 'buy', ask)
            self.modify_rates_tile(qty_2)
            self.check_order_ticket(qty_2, 'sell', bid)

        except Exception as e:
            logging.error('Error execution', exc_info=True)
        close_fe(self.case_id, self.session_id)

# if __name__ == '__main__':
#     pass
