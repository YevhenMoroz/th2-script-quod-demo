import logging
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, TimeInForce, OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7471(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.account = self.data_set.get_account_by_name("client_counterpart_1_acc_1")
        self.client_2 = self.data_set.get_client_by_name("client_counterpart_2")
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.order_type = OrderType.limit.value
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.lookup = "DNX"
        self.change_params = {'Account': self.client,
                              'ExDestination': self.mic,
                              'PreAllocGrp': {
                                  'NoAllocs': [{
                                      'AllocAccount': self.account,
                                      'AllocQty': "100"}]}}
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.client_id = self.fix_message.get_parameter('ClOrdID')

        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.username = environment.get_list_fe_environment()[0].user_1

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region care order
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        self.client_inbox.accept_order()
        parties = {
            'NoPartyIDs': [
                {'PartyRole': "*",
                 'PartyID': "*",
                 'PartyIDSource': "*"},
                {'PartyRole': "*",
                 'PartyID': "*",
                 'PartyIDSource': "*"},
                {'PartyRole': "*",
                 'PartyRoleQualifier': "1011",
                 'PartyID': "*",
                 'PartyIDSource': "*"}
            ]
        }
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message).change_parameters(
            {"Parties": parties, "ReplyReceivedTime": "*", "SecondaryOrderID": "*", "LastMkt": "*", "Text": "*"})
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1)
        self.order_book.manual_execution()
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message).change_parameters(
            {"Parties": parties, "ReplyReceivedTime": "*", "SecondaryOrderID": "*", "LastMkt": "*", "Text": "*"})
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report2)

        # endregion
        self.order_ticket.set_order_details(client=self.self.client_2, limit=self.price, qty=self.qty, order_type=self.order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup, recipient=self.username)
        self.order_ticket.create_order(lookup=self.lookup)
        self.client_inbox.accept_order()
        self.order_book.manual_execution()
        # endregion
        # region Check ExecutionReports
        self.order_book.complete_order()
        # endregion
        # region Check ExecutionReports

