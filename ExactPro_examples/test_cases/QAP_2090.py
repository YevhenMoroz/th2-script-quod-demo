import logging
import time

# from demo import timeouts
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from custom import basic_custom_actions as bca

from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRFQTileRequest, \
    ContextAction
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe_2, close_fe, \
    get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails
from win_gui_modules.quote_wrappers import QuoteDetailsRequest

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
        self.case_id = bca.create_event('QAP-2090', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.venue = 'HSB'
        self.user = Stubs.custom_config['qf_trading_fe_user_303']
        self.quote_id = None
        self.case_params = {
            'Connectivity': 'fix-qsesp-303',
            'MDReqID': bca.client_orderid(10),
            'Account': 'MMCLIENT1',
            'HandlInst': '1',
            'Side': '1',
            'OrderQty': 1000000,
            'OrdType': '2',
            'Price': 35.002,
            'TimeInForce': '3',
            'SettlType': 0,
            'SettlDate': tsd.spo(),
            'Instrument': {
                'Symbol': 'EUR/USD',
                'Product': '4',
                'SecurityType': 'FXSPOT'
            }
        }

        # This parameters can be used for ExecutionReport message
        self.reusable_order_params = {
            'Account': self.case_params['Account'],
            'HandlInst': self.case_params['HandlInst'],
            'Side': self.case_params['Side'],
            'TimeInForce': self.case_params['TimeInForce'],
            'OrdType': self.case_params['OrdType'],
            'OrderCapacity': 'A',
            'Currency': 'EUR'
        }
        self.case_params = {
            'Connectivity': 'fix-qsesp-303',
            'MDReqID': bca.client_orderid(10),
            'Account': 'MMCLIENT1',
            'HandlInst': '1',
            'Side': '1',
            'OrderQty': 1000000,
            'OrdType': '2',
            'Price': 35.002,
            'TimeInForce': '3',
            'SettlType': 0,
            'SettlDate': tsd.spo(),
            'Instrument': {
                'Symbol': 'EUR/USD',
                'Product': '4',
                'SecurityType': 'FXSPOT'
            }
        }

        # This parameters can be used for ExecutionReport message
        self.reusable_order_params = {
            'Account': self.case_params['Account'],
            'HandlInst': self.case_params['HandlInst'],
            'Side': self.case_params['Side'],
            'TimeInForce': self.case_params['TimeInForce'],
            'OrdType': self.case_params['OrdType'],
            'OrderCapacity': 'A',
            'Currency': 'EUR'
        }

        # Case rules
        self.rule_manager = RuleManager()
        self.NOS = None
        self.RFQ = None
        self.TRFQ = None

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        try:
            get_opened_fe(self.case_id, self.session_id)
        except Exception as e:
            logging.error('FE is not opened')
            prepare_fe(self.case_id, self.session_id, work_dir, self.user, password)

    # Add case rules method
    def add_rules(self):
        self.NOS = self.rule_manager.add_NOS('fix-qsesp-303')
        self.RFQ = self.rule_manager.add_RFQ('fix-fh-fx-rfq')
        self.TRFQ = self.rule_manager.add_TRFQ('fix-fh-fx-rfq')

    # Remove case rules method
    def remove_rules(self):
        self.rule_manager.remove_rule(self.NOS)
        self.rule_manager.remove_rule(self.RFQ)
        self.rule_manager.remove_rule(self.TRFQ)
        self.rule_manager.print_active_rules()

    # Set near date method
    def modify_tile(self, near, far, cur_from, cur_to):
        modify_request = ModifyRFQTileRequest(details=self.base_details)
        modify_request.set_from_currency(cur_from)
        modify_request.set_to_currency(cur_to)
        modify_request.set_near_tenor(near)
        modify_request.set_far_leg_tenor(far)
        call(self.ar_service.modifyRFQTile, modify_request.build())

    def maximize_ar_window(self):
        call(self.ar_service.maximizeWindow, self.base_request)

    def minimize_ar_window(self):
        call(self.ar_service.minimizeWindow, self.base_request)

    # Create or get RFQ method
    def create_rfq_tile(self):
        call(self.ar_service.createRFQTile, self.base_details.build())

    # Send RFQ method
    def send_rfq(self):
        call(self.ar_service.sendRFQOrder, self.base_details.build())
    #
    # # Cancel RFQ method
    # def cancel_rfq(self):
    #     call(self.ar_service.cancelRFQ, self.rfq_1.build())
    #
    # # Send an order by clicking from Top Of Book button method
    # def send_order_by_tob(self):
    #     rfq_request = PlaceRFQRequest(details=self.rfq_1)
    #     rfq_request.set_action(RFQTileOrderSide.BUY)
    #     call(self.ar_service.placeRFQOrder, rfq_request.build())
    #
    # # Send an order by clicking price in a venue method
    # def send_order_by_venue_price(self):
    #     rfq_request = PlaceRFQRequest(details=self.rfq_1)
    #     rfq_request.set_venue(self.venue)
    #     rfq_request.set_action(RFQTileOrderSide.BUY)
    #     call(self.ar_service.placeRFQOrder, rfq_request.build())

    # Check QuoteRequestBook method
    def check_qrb(self, cur):
        execution_id = bca.client_orderid(4)
        qrb = QuoteDetailsRequest(base=self.base_request)
        qrb.set_extraction_id(execution_id)
        qrb.set_filter(["Currency", cur])
        qrb_user = ExtractionDetail('quoteRequestBook.user', 'User')
        qrb_status = ExtractionDetail('quoteRequestBook.status', 'Status')
        qrb_quote_status = ExtractionDetail('quoteRequestBook.qoutestatus', 'QuoteStatus')
        qrb.add_extraction_details([qrb_user, qrb_status, qrb_quote_status])
        call(self.common_act.verifyEntities, verification(execution_id, 'checking QRB',
                                                          [verify_ent('QRB User', qrb_user.name, self.user),
                                                           verify_ent('QRB Status', qrb_status.name, 'New'),
                                                           verify_ent('QRB QuoteStatus', qrb_quote_status.name,
                                                                      'Accepted')]))

    # Check QuoteBook method
    def check_qb(self):
        execution_id = bca.client_orderid(4)
        qb = QuoteDetailsRequest(base=self.base_request)
        qb.set_extraction_id(execution_id)
        qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
        qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
        qb_id = ExtractionDetail("quoteBook.id", "Id")
        qb.add_extraction_details([qb_owner, qb_quote_status, qb_id])
        self.quote_id = call(self.ar_service.getQuoteBookDetails, qb.request())[qb_id.name]
        call(self.common_act.verifyEntities, verification(execution_id, "checking QB",
                                                          [verify_ent("QB Owner", qb_owner.name, self.user),
                                                           verify_ent("QB QuoteStatus", qb_quote_status.name,
                                                                      "Accepted")]))

    # Check OrderBook method
    def check_ob(self):
        execution_id = bca.client_orderid(4)
        ob = OrdersDetails()
        ob.set_default_params(self.base_request)
        ob.set_extraction_id(execution_id)
        ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
        ob_id = ExtractionDetail("orderBook.quoteid", "QuoteID")
        ob.add_single_order_info(
            OrderInfo.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[ob_exec_sts, ob_id])))
        call(self.ob_act.getOrdersDetails, ob.request())
        call(self.common_act.verifyEntities, verification(execution_id, "checking OB",
                                                          [verify_ent("OB ExecSts", ob_exec_sts.name, "Filled"),
                                                           verify_ent("OB ID vs QB ID", ob_id.name, self.quote_id)]))

    # Main method. Must call in demo.py by "QAP_574.TestCase(report_id).execute()" command
    def execute(self):
        try:
            self.prepare_frontend()
            self.add_rules()
            #
            # # Step 1
            self.create_rfq_tile()
            self.modify_tile("Spot", "1W", "EUR", "USD")
            self.send_rfq()
            # Step 2
            self.check_qrb("EUR")
            # self.check_qb()
            # # Step 2
            # self.send_order_by_tob()
            # self.check_ob()
            # self.cancel_rfq()
            # # Step 3
            # self.send_rfq()
            # self.check_qrb()
            # self.check_qb()
            # # Step 4
            # self.send_order_by_venue_price()
            # self.check_ob()
            # self.cancel_rfq()

        except Exception as e:
            logging.error('Error execution', exc_info=True)

        self.remove_rules()
        # close_fe(self.case_id, self.session_id)


if __name__ == '__main__':
    pass
