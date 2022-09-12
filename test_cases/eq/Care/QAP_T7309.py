import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, SecondLevelTabs, ExecSts, \
    PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7309(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        self.client_inbox.accept_order()
        # endregion
        # region manual execute
        self.order_book.manual_execution(filter_dict={OrderBookColumns.order_id.value: order_id})
        # endregion
        # region check execution
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters({"LastMkt": "*", "VenueType": "*"})
        self.exec_report.remove_parameters(['SecondaryExecID', 'SettlCurrency', 'LastExecutionPolicy', 'SecondaryOrderID'])
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion
        # region trade cancel
        exec_id = self.order_book.extract_2lvl_fields(tab=SecondLevelTabs.executions.value,
                                                       column_names=[OrderBookColumns.exec_id.value], rows=[1],
                                                       filter_dict={OrderBookColumns.order_id.value: order_id})
        self.trade_book.cancel_execution({OrderBookColumns.exec_id.value: exec_id[0]['ExecID']})
        # endregion
        # region check cancelled exec
        self.__check_exec_tab(OrderBookColumns.exec_type.value, ExecSts.trade_cancel.value, 1, {OrderBookColumns.order_id.value: order_id})
        self.__check_exec_tab(OrderBookColumns.post_trade_status_exec.value, PostTradeStatuses.not_allocable.value, 1,
                              {OrderBookColumns.order_id.value: order_id})
        # endregion

    def __check_exec_tab(self, field:str, expect:str, row:int, filtr:dict = None):
        acc_res = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                        [field], [row],
                                                        filtr)
        self.order_book.compare_values({field: expect}, {field: acc_res[0][field]}, "Check Execution tab")