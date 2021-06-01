import logging

from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails
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
        self.ob_act = Stubs.win_act_order_book

        # Case parameters setup
        self.case_id = bca.create_event('QAP-574', report_id)
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
        # get_opened_fe_303(self.case_id, self.session_id, work_dir, self.user, password)
        prepare_fe303(self.case_id, self.session_id, work_dir, self.user, password)

        # try:
        #     get_opened_fe_303(self.case_id, self.session_id, work_dir, self.user, password)
        # except Exception as e:
        #     logging.error('FE is not opened')
        #     prepare_fe303(self.case_id, self.session_id, work_dir, self.user, password)

    #send market data
    def send_market_data(self, qty, price):
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
                    "MDEntryPx": price,
                    "MDEntrySize": qty,
                    "MDEntryPositionNo": 1,
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": price,
                    "MDEntrySize": qty,
                    "MDEntryPositionNo": 2,
                }
            ]
        }

        act.sendMessage(
            bca.convert_to_request(
                'Send MDU EUR/USD:SPO:REG:HSBC',
                'fix-fh-fx-esp',
                self.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_hsbc, 'fix-fh-fx-esp')
            ))

    # Main method
    def execute(self):
        try:
            self.prepare_frontend()
            self.send_market_data(1000000, 500)
            # self.send_market_data(5000000)
            # self.send_market_data(7000000)
        except Exception as e:
            logging.error('Error execution', exc_info=True)
        # close_fe(self.case_id, self.session_id)

if __name__ == '__main__':
    pass
