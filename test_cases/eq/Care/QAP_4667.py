import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, OrderType, TimeInForce
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_4667(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.price = self.fix_message.get_parameter("Price")
        self.fix_message.change_parameters({"TimeInForce": "1", "OrdType": "4"})
        self.fix_message.add_tag({'StopPx': self.price})
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message_cancel_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # endregion
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        self.client_inbox.accept_order()
        # endregion
        # region send Cancel Replace Request
        self.fix_message_cancel_replace.set_default(self.fix_message)
        self.fix_message_cancel_replace.change_parameters({'StopPx': "10", "TimeInForce": "0"})
        self.fix_manager.send_message_fix_standard(self.fix_message_cancel_replace)
        # endregion
        # region accept modify
        self.client_inbox.reject_order()
        # endregion
        # region check exec report
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.ord_type.value: OrderType.stop_limit.value,
             OrderBookColumns.tif.value: TimeInForce.GTC.value, OrderBookColumns.stop_price.value: self.price})
        # endregion
        # region check exec report
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set).set_default_new(
            self.fix_message)
        fix_execution_report.change_parameters(
            {"OrdType": "4", 'StopPx': self.price, "TimeInForce": "1", "SettlDate": "*"})
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report)
        # endregion
