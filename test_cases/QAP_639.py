import logging
import time

# from demo import timeouts
from rule_management import RuleManager
from stubs import Stubs
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
        self.case_id = bca.create_event('QAP-639', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)

        self.rfq_1 = BaseTileDetails(base=self.base_request, window_index=0)
        self.rfq_2 = BaseTileDetails(base=self.base_request, window_index=1)
        self.rfq_3 = BaseTileDetails(base=self.base_request, window_index=2)

        self.venue = 'HSB'
        self.user = Stubs.custom_config['qf_trading_fe_user_303']

        # Case rules
        self.rule_manager = RuleManager()
        self.RFQ = None
        self.TRFQ = None

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        prepare_fe(self.case_id, self.session_id, work_dir, self.user, password)
        # try:
        #     get_opened_fe(self.case_id, self.session_id)
        # except Exception as e:
        #     logging.error('FE is not opened')
        #     prepare_fe(self.case_id, self.session_id, work_dir, self.user, password)

    # Add case rules method
    def add_rules(self):
        self.RFQ = self.rule_manager.add_RFQ('fix-fh-fx-rfq')
        self.TRFQ = self.rule_manager.add_TRFQ('fix-fh-fx-rfq')

    # Remove case rules method
    def remove_rules(self):
        self.rule_manager.remove_rule(self.RFQ)
        self.rule_manager.remove_rule(self.TRFQ)
        self.rule_manager.print_active_rules()

    # Set near date method
    def modify_tile(self, details, near_tenor, far_tenor, currency_from, currency_to):
        modify_request = ModifyRFQTileRequest(details=details)
        modify_request.set_from_currency(currency_from)
        modify_request.set_to_currency(currency_to)
        modify_request.set_near_tenor(near_tenor)
        modify_request.set_far_leg_tenor(far_tenor)
        call(self.ar_service.modifyRFQTile, modify_request.build())

    def maximize_ar_window(self):
        call(self.ar_service.maximizeWindow, self.base_request)

    def minimize_ar_window(self):
        call(self.ar_service.minimizeWindow, self.base_request)

    # Create or get RFQ method
    def create_rfq_tile(self, details):
        call(self.ar_service.createRFQTile, details.build())

    # Send RFQ method
    def send_rfq(self, details):
        call(self.ar_service.sendRFQOrder, details.build())

    # Cancel RFQ method
    def cancel_rfq(self, details):
        call(self.ar_service.cancelRFQ, details.build())

    # Send an order by clicking price in a venue method
    def send_order_by_venue_price(self, details):
        rfq_request = PlaceRFQRequest(details=details)
        rfq_request.set_venue(self.venue)
        rfq_request.set_action(RFQTileOrderSide.BUY)
        call(self.ar_service.placeRFQOrder, rfq_request.build())

    # Check QuoteRequestBook method
    def check_qrb(self, row_index, instrument_symbol):
        execution_id = bca.client_orderid(4)
        qrb = QuoteDetailsRequest(base=self.base_request)
        qrb.set_row_number(row_index)
        qrb.set_extraction_id(execution_id)
        qrb_instrument_symbol = ExtractionDetail('quoteRequestBook.instrumentsymbol', 'InstrSymbol')
        qrb_user = ExtractionDetail('quoteRequestBook.user', 'User')
        qrb_status = ExtractionDetail('quoteRequestBook.status', 'Status')
        qrb_quote_status = ExtractionDetail('quoteRequestBook.qoutestatus', 'QuoteStatus')
        qrb.add_extraction_details([qrb_instrument_symbol, qrb_user, qrb_status, qrb_quote_status])
        call(self.ar_service.getQuoteRequestBookDetails, qrb.request())
        call(self.common_act.verifyEntities, verification(execution_id, 'checking QRB',
                                                          [verify_ent('QRB InstrSymbol', qrb_instrument_symbol.name,
                                                                      instrument_symbol),
                                                           verify_ent('QRB User', qrb_user.name, self.user),
                                                           verify_ent('QRB Status', qrb_status.name, 'New'),
                                                           verify_ent('QRB QuoteStatus', qrb_quote_status.name,
                                                                      'Accepted')]))

    # Check QuoteBook method
    def check_qb(self, row_index, security_id):
        execution_id = bca.client_orderid(4)
        qb = QuoteDetailsRequest(base=self.base_request)
        qb.set_row_number(row_index)
        qb.set_extraction_id(execution_id)
        qb_owner = ExtractionDetail('quoteBook.owner', 'Owner')
        qb_quote_status = ExtractionDetail('quoteBook.quotestatus', 'QuoteStatus')
        qb_id = ExtractionDetail('quoteBook.id', 'Id')
        qb_security_id = ExtractionDetail('quoteBook.securityid', 'SecurityID')
        qb.add_extraction_details([qb_owner, qb_quote_status, qb_id, qb_security_id])
        quote_id = call(self.ar_service.getQuoteBookDetails, qb.request())[qb_id.name]
        call(self.common_act.verifyEntities, verification(execution_id, 'checking QB',
                                                          [verify_ent('QB Owner', qb_owner.name, self.user),
                                                           verify_ent('QB QuoteStatus', qb_quote_status.name,
                                                                      'Accepted'),
                                                           verify_ent('SecurityID', qb_security_id.name,
                                                                      security_id)]))
        return quote_id

    # Check OrderBook method
    def check_ob(self, row_index, quote_id):
        execution_id = bca.client_orderid(4)
        ob = OrdersDetails()
        ob.set_default_params(self.base_request)
        ob.set_extraction_id(execution_id)
        ob_exec_sts = ExtractionDetail('orderBook.execsts', 'ExecSts')
        ob_id = ExtractionDetail('orderBook.quoteid', 'QuoteID')
        order_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_exec_sts, ob_id]))
        order_info.set_number(row_index)
        ob.add_single_order_info(
            order_info)
        call(self.ob_act.getOrdersDetails, ob.request())
        call(self.common_act.verifyEntities, verification(execution_id, 'checking OB',
                                                          [verify_ent('OB ExecSts', ob_exec_sts.name, 'Filled'),
                                                           verify_ent('OB ID vs QB ID', ob_id.name, quote_id)]))

    # Main method. Must call in demo.py by "QAP_639.TestCase(report_id).execute()" command
    def execute(self):
        try:
            self.prepare_frontend()
            # self.add_rules()

            # Step 1
            self.maximize_ar_window()

            self.create_rfq_tile(self.rfq_1)
            self.modify_tile(self.rfq_1, 'Spot', '1W', 'EUR', 'USD')

            self.create_rfq_tile(self.rfq_2)
            self.modify_tile(self.rfq_2, '2W', '3W', 'AUD', 'BRL')

            self.create_rfq_tile(self.rfq_3)
            self.modify_tile(self.rfq_3, '1M', '2M', 'EUR', 'GBP')

            # Step 2
            self.send_rfq(self.rfq_1)
            self.send_rfq(self.rfq_2)
            self.send_rfq(self.rfq_3)

            self.minimize_ar_window()

            quote_id_1 = self.check_qb(1, 'EUR/GBP')
            quote_id_2 = self.check_qb(2, 'AUD/BRL')
            quote_id_3 = self.check_qb(3, 'EUR/USD')

            # Step 3
            self.maximize_ar_window()

            self.send_order_by_venue_price(self.rfq_1)
            self.send_order_by_venue_price(self.rfq_2)
            self.send_order_by_venue_price(self.rfq_3)

            self.minimize_ar_window()

            self.check_ob(1, quote_id_1)
            self.check_ob(2, quote_id_2)
            self.check_ob(3, quote_id_3)

            # Step 4
            self.maximize_ar_window()

            self.send_rfq(self.rfq_1)
            self.send_rfq(self.rfq_2)
            self.send_rfq(self.rfq_3)

            self.minimize_ar_window()

            quote_id_1 = self.check_qb(1, 'EUR/GBP')
            quote_id_2 = self.check_qb(2, 'AUD/BRL')
            quote_id_3 = self.check_qb(3, 'EUR/USD')

            # Step 5
            self.maximize_ar_window()

            self.send_order_by_venue_price(self.rfq_1)
            self.send_order_by_venue_price(self.rfq_2)
            self.send_order_by_venue_price(self.rfq_3)

            self.minimize_ar_window()

            self.check_ob(1, quote_id_1)
            self.check_ob(2, quote_id_2)
            self.check_ob(3, quote_id_3)

            # Step 6
            self.maximize_ar_window()

            self.send_rfq(self.rfq_1)
            self.send_rfq(self.rfq_2)
            self.send_rfq(self.rfq_3)

            self.minimize_ar_window()

            quote_id_1 = self.check_qb(1, 'EUR/GBP')
            quote_id_2 = self.check_qb(2, 'AUD/BRL')
            quote_id_3 = self.check_qb(3, 'EUR/USD')

            # Step 7
            self.maximize_ar_window()

            self.cancel_rfq(self.rfq_1)

            # TODO add Send button check

            # Step 8
            self.send_order_by_venue_price(self.rfq_2)

            self.minimize_ar_window()

            self.check_ob(2, quote_id_2)

            # # Step 9
            # self.minimize_ar_window()
            # time.sleep(30)

        except Exception as e:
            logging.error('Error execution', exc_info=True)

        # self.remove_rules()
        close_fe(self.case_id, self.session_id)


if __name__ == '__main__':
    pass
