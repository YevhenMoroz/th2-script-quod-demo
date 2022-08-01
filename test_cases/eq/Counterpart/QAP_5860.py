import logging
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_5860(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.fix_message.change_parameters({'Account': self.client})
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.client_id = self.fix_message.get_parameter('ClOrdID')


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region send and accept first order
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        self.client_inbox.accept_order()
        # region Declaration
        # region send and accept second order
        self.fix_message.change_parameter("Side", "2")
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        self.client_inbox.accept_order()
        # endregion
        # region manual cross orders
        self.order_book.set_filter([OrderBookColumns.client_id.value, self.client_id]).manual_cross_orders([1, 2],
                                                                                                           self.qty,
                                                                                                           self.price,
                                                                                                           last_mkt="CHIX")
        # endregion
        # region send exec report
        self.execution_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report1)
        self.execution_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report2)
        # endregion
