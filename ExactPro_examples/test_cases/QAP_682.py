import logging
import time

from custom.verifier import Verifier
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRFQTileRequest, \
    ContextAction, ExtractRFQTileValues, TableActionsRequest, TableAction
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe_2, close_fe, \
    get_opened_fe, prepare_fe303, get_opened_fe_303
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
        self.case_id = bca.create_event('QAP-682', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.rfq_1 = BaseTileDetails(base=self.base_request, window_index=0)
        self.rfq_2 = BaseTileDetails(base=self.base_request, window_index=1)

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
        prepare_fe303(self.case_id, self.session_id, work_dir, self.user, password)

    # Remove case rules method
    def remove_rules(self):
        self.rule_manager.remove_rule(self.RFQ)
        self.rule_manager.remove_rule(self.TRFQ)
        self.rule_manager.print_active_rules()

    # Set near date method
    def modify_tile(self, details, near, far, cur_from, cur_to):
        modify_request = ModifyRFQTileRequest(details=details)
        modify_request.set_from_currency(cur_from)
        modify_request.set_to_currency(cur_to)
        modify_request.set_near_tenor(near)
        modify_request.set_far_leg_tenor(far)
        call(self.ar_service.modifyRFQTile, modify_request.build())

    # Set venue filter method
    def set_venue_filter(self, details):
        modify_request = ModifyRFQTileRequest(details=details)
        action = ContextAction.create_venue_filter("MGS")
        modify_request.add_context_action(action)
        call(self.ar_service.modifyRFQTile, modify_request.build())

    # extracting rfq value method
    def check_rfq_values(self, details, c_pair, n_tenor, f_tenor):
        cur_pair = "aggrRfqTile.currencyPair"
        near_tenor = "aggrRfqTile.nearSettlement"
        far_tenor = "aggrRfqTile.farLegTenor"
        extract_values_request = ExtractRFQTileValues(details=details)
        extract_values_request.extract_currency_pair(cur_pair)
        extract_values_request.extract_tenor(near_tenor)
        extract_values_request.extract_far_leg_tenor(far_tenor)
        response = call(self.ar_service.extractRFQTileValues, extract_values_request.build())
        verifier = Verifier(self.case_id)
        verifier.set_event_name("Checking RFQ_Tile_2 Details")
        verifier.compare_values("Currency Pair", response[cur_pair], c_pair)
        verifier.compare_values("Near Settlement Date", response[near_tenor], n_tenor)
        verifier.compare_values("Far Leg Tenor", response[far_tenor], f_tenor)
        verifier.verify()

    # check venues in table method
    def check_venues(self, details):
        table_actions_request = TableActionsRequest(details=details)
        check1 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.hsbVenue", "HSB"))
        check2 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.mgsVenue", "MGS"))
        table_actions_request.set_extraction_id("extrId")
        table_actions_request.add_actions([check1, check2])
        response = call(self.ar_service.processTableActions, table_actions_request.build())
        verifier = Verifier(self.case_id)
        verifier.set_event_name("Checking RFQ_Tile_2 Venue tables")
        verifier.compare_values("HSB", response["aggrRfqTile.hsbVenue"], "found")
        verifier.compare_values("MGS", response["aggrRfqTile.mgsVenue"], "not found")
        verifier.verify()

    def maximize_ar_window(self):
        call(self.ar_service.maximizeWindow, self.base_request)

    def minimize_ar_window(self):
        call(self.ar_service.minimizeWindow, self.base_request)

    def close_tile(self, details):
        call(self.ar_service.closeRFQTile, details.build())

    # Create or get RFQ method
    def create_or_get_rfq(self):
        call(self.ar_service.createRFQTile, self.base_details.build())

    # Create or get RFQ method
    def create_rfq_tile(self, rfq):
        call(self.ar_service.createRFQTile, rfq.build())

    # Main method. Must call in demo.py by "QAP_682.TestCase(report_id).execute()" command
    def execute(self):
        try:
            self.prepare_frontend()
            #
            # # Step 1
            # self.create_or_get_rfq()
            self.maximize_ar_window()
            self.create_rfq_tile(self.rfq_1)
            self.modify_tile(self.rfq_1, "Spot", "Mar IMM", "EUR", "USD")
            self.set_venue_filter(self.rfq_1)
            # Step 2
            self.create_rfq_tile(self.rfq_2)
            self.check_rfq_values(self.rfq_2, "EUR/USD", "Spot", "Mar IMM")
            self.check_venues(self.rfq_2)
            # Step 3
            self.close_tile(self.rfq_1)
            self.close_tile(self.rfq_2)
            # Step 4
            self.create_rfq_tile(self.rfq_1)
            self.modify_tile(self.rfq_1, "7M", "8M", "EUR", "USD")
            self.set_venue_filter(self.rfq_1)
            # Step 2
            self.create_rfq_tile(self.rfq_2)
            self.check_rfq_values(self.rfq_2, "EUR/USD", "7M", "8M")
            self.check_venues(self.rfq_2)
        except Exception as e:
            logging.error('Error execution', exc_info=True)

        # close_fe(self.case_id, self.session_id)


if __name__ == '__main__':
    pass
