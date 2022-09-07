import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7506(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.fix_message.change_parameters({"Account": self.client})
        self.price = self.fix_message.get_parameter('Price')
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.mic = self.fix_message.get_parameter('ExDestination')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        # endregion
        # region Accept CO
        self.client_inbox.accept_order()
        # endregion
        # region split order
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty), int(self.qty), 1)
            self.order_ticket.split_order([OrderBookColumns.order_id.value, order_id])
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
        # region send exec report
        exec_id = \
        self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value, [OrderBookColumns.exec_id.value], [1],
                                            {OrderBookColumns.order_id.value: order_id})[0][
            OrderBookColumns.exec_id.value]
        execution_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        execution_report.change_parameters(
            {'OrderID': order_id, 'LastMkt': "*", 'BookID': "*",
             "QuodTradeQualifier": "*", "ExecID": exec_id, "SecondaryExecID": "1", 'NoParty': "*", 'tag5120': "*",
             "ExecBroker": "*", "NoMiscFees": "*", "CommissionData": "*"})
        execution_report.remove_parameters(['SettlCurrency', 'Parties', 'TradeReportingIndicator', 'SecondaryOrderID'])
        self.fix_verifier.check_fix_message_fix_standard(execution_report)
        # endregion
