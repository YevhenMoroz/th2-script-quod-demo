import logging
from datetime import datetime, timedelta
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7502(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = "300"
        self.price = "10"
        self.exec_qty = "150"
        self.contra_firm = "Manual Execution"
        self.last_capacity = "Agency"
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter("Price", self.price)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.settl_date = int(str(datetime.now().date() + timedelta(days=1)).replace('-', ''))
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set, self.fix_message.get_parameters()).set_default_filled(self.fix_message)
        self.exec_report.change_parameter('OrdStatus', '2')
        self.base_request = get_base_request(self.session_id, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        # endregion
        # region manual execution
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).manual_execution(qty=self.exec_qty,
                                                                                                 price=self.price,
                                                                                                 settl_date=1)
        # endregion
        # region check partially fill exec status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        exec_report.change_parameters({'SettlDate': self.settl_date, "LastMkt": "XPAR", "VenueType": "O", "OrdStatus": "1",
                                       "LastCapacity" :"1"})
        exec_report.remove_parameters(["SecondaryOrderID", "LastExecutionPolicy", "SettlCurrency", "SecondaryExecID"])
        self.fix_verifier.check_fix_message(exec_report)
        # endregion
        # region manual execution
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).manual_execution(qty=self.exec_qty, price=self.price,
                                         execution_firm="TAVIRA",settl_date=1, contra_firm=self.contra_firm,
                                         last_capacity=self.last_capacity)
        # endregion
        # region check filled exec status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        exec_report.change_parameters(
            {'SettlDate': self.settl_date, "LastMkt": "XPAR", "VenueType": "O", "OrdStatus": "2",
             "LastCapacity": "1"})
        exec_report.remove_parameters(["SecondaryOrderID", "LastExecutionPolicy", "SettlCurrency", "SecondaryExecID"])
        self.fix_verifier.check_fix_message(exec_report)
        # endregion

