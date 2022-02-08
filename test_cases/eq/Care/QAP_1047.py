import logging
from pathlib import Path
from rule_management import RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.DataSet import Connectivity
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_1047(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.bs_connectivity = Connectivity.Ganymede_317_bs.value
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.route = self.data_set.get_route("route_1")
        self.venue = self.data_set.get_mic_by_name("mic_1")
        self.qty_percentage = "100"
        self.qty_type = self.data_set.get_qty_type("qty_type_1")
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.fix_manager = FixManager(self.ss_connectivity)
        self.rule_manager = RuleManager()
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # endregion
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        price = self.fix_message.get_parameter('Price')
        # endregion
        # region accept CO order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingle_Market_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                                self.venue, True,
                                                                                                int(qty), float(price))
            self.client_inbox.client_inbox_direct_moc(self.qty_type, self.qty_percentage, self.route)

        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        # endregion
        # region check filled child status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
                {OrderBookColumns.ord_type.value: OrderType.market.value, OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion

