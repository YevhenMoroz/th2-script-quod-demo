import time
from rule_management import RuleManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageCancelRejectReportOMS import FixMessageOrderCancelRejectReportOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import  OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True



class QAP_T7524(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.rule_manager = RuleManager()
        self.new_qty = "4444"
        self.cancel_reject_report = FixMessageOrderCancelRejectReportOMS()


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region check out order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_out_order()
        # endregion
        # region check order check out status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.is_locked.value: "Yes"})
        # endregion
        # region amend order via FIX
        try:
            cancel_replace_rule  = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                              self.data_set.get_venue_client_names_by_name(
                                                                                  "client_pt_1_venue_1"),
                                                                              self.data_set.get_mic_by_name("mic_1"))
            cancel_replace_request = FixMessageOrderCancelReplaceRequestOMS(self.data_set, self.fix_message.get_parameters()).set_default(
                self.fix_message)
            cancel_replace_request.change_parameter('OrderQtyData', {'OrderQty': self.new_qty})
            self.fix_manager.send_message_fix_standard(cancel_replace_request)
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            self.rule_manager.remove_rule(cancel_replace_rule)

        self.cancel_reject_report.set_default(self.fix_message)
        self.cancel_reject_report.change_parameter("Text", "11629 Order is in locked state")
        self.fix_verifier.check_fix_message_fix_standard(self.cancel_reject_report)
        # endregion
        # region check out order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_in_order()
        # endregion
        # region check order check in status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
                {OrderBookColumns.is_locked.value: ""})
        # endregion
        # region amend order via FIX
        try:
            cancel_replace_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                              self.data_set.get_venue_client_names_by_name(
                                                                                  "client_pt_1_venue_1"),
                                                                              self.data_set.get_mic_by_name("mic_1"))
            cancel_replace_request = FixMessageOrderCancelReplaceRequestOMS(self.data_set).set_default(
                self.fix_message).change_parameter('OrderQtyData', {'OrderQty': self.new_qty})
            self.fix_manager.send_message_fix_standard(cancel_replace_request)
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            self.rule_manager.remove_rule(cancel_replace_rule)
        # endregion
        # region accept order
        self.client_inbox.accept_modify_plus_child()
        # endregion
        # ckeck new values
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.qty.value: self.new_qty})
        # endregion






