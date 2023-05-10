import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7674(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.qty = '100'
        self.qty2 = '240'
        self.price = '10'
        self.price2 = '50'
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message_cancel_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.fix_message_cancel = FixMessageOrderCancelRequestOMS()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send Fix Message
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        exec_report_new = response[1].get_parameters()
        # endregion

        # region check order has open status
        self.order_book.compare_values({'ExecType': '0'}, exec_report_new, 'Check Order sts')
        # endregion

        # region amend order by Fix
        self.fix_message_cancel_replace.set_default(self.fix_message)
        self.fix_message_cancel_replace.change_parameters({'OrderQtyData': {'OrderQty': self.qty2}, "Price":
            self.price2})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_cancel_replace)
        # endregion

        # region check changed values
        exec_report_replaced = response[0].get_parameters()
        self.order_book.compare_values({'ExecType': '5', 'Price': self.price2, 'OrderQtyData': {'OrderQty': self.qty2}},
                                       exec_report_replaced, 'Check replaced values ')
        # endregion

        # region cancel order by Fix
        self.fix_message_cancel.set_default(self.fix_message)
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_cancel)
        # endregion

        # region check cancelled status
        exec_report_cancelled = response[0].get_parameters()
        self.order_book.compare_values({'ExecType': '4'},
                                       exec_report_cancelled, 'Check replaced values ')
        # endregion
