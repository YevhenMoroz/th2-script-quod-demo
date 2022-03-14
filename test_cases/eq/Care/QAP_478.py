import logging
from pathlib import Path
from rule_management import RuleManager
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_478(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_market()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.qty_per = "100"
        self.rule_manager = RuleManager()
        self.route = self.data_set.get_route('route_1')
        self.qty_type = self.data_set.get_qty_type('qty_type_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Create Market CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region Accept CO order
        self.client_inbox.accept_order()
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region DirectMoc order
        try:
            self.nos_rule = self.rule_manager.add_NewOrdSingle_Market_FIXStandard(
                self.fix_env.sell_side,
                self.venue_client_names, self.venue,
                False, int(self.qty), 0)
            self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).direct_moc_order(self.qty_per, self.route, self.qty_type)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            self.rule_manager.remove_rule(self.nos_rule)
        # endregion
        # region check child order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.qty.value: self.qty})
        # endregion



        # endregion

        # # region open FE
        # base_window.open_fe(self.report_id, work_dir, username, password, True)
        # # endregion
        # # region create CO order
        # fix_manager.send_message_fix_standard(fix_message)
        # order_id_first = order_book.extract_field('Order ID')
        # # endregion

        # # region accept CO order
        # order_inbox = OMSClientInbox(self.case_id, self.session_id)
        # order_inbox.accept_order('O', 'M', 'S')
        # # endregion
        # rule_manager = RuleManager()
        # # region directLoc order
        # try:
        #     nos_rule = rule_manager.add_NewOrdSingle_Market_FIXStandard(self.bs_connectivity,
        #                                                                 'XPAR_' + client,
        #                                                                 'XPAR', False, int(qty),
        #                                                                 float(fix_message.get_parameter('Price')))
        #
        #     order_book.direct_moc_order_correct(qty, route)
        # except Exception:
        #     logger.setLevel(logging.DEBUG)
        #     logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        # finally:
        #     time.sleep(3)
        #     rule_manager.remove_rule(nos_rule)
        # # endregion
        #
        # # region extraction_value
        # result = order_book.extract_2lvl_fields('Child Orders', ['Sts', 'Qty'], rows=[1],
        #                                         filter_dict={'Order ID': order_id_first})
        #
        # base_window.compare_values({'Sts': 'Eliminated', 'Qty': '100'}, result[0], 'Equals value')
        #
