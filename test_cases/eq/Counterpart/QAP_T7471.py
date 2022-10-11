import logging
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
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
        self.client = self.data_set.get_client_by_name("client_1")
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.alloc_report = FixMessageAllocationInstructionReportOMS().set_default_ready_to_book(self.fix_message)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.order_type = OrderType.limit.value
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.lookup = self.data_set.get_lookup_by_name('lookup_2')
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.username = environment.get_list_fe_environment()[0].user_1

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create Care order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.client_inbox.accept_order(filter=filter_dict)
        parties = [
            {'PartyRole': "28",
             'PartyID': "CustodianUser",
             'PartyIDSource': "C"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"}
        ]
        # endregion
        # region Execute Order
        self.order_book.manual_execution(contra_firm=self.data_set.get_contra_firm("contra_firm_1"),
                                         filter_dict=filter_dict)
        self.order_book.complete_order(filter_list=filter_list)
        # endregion
        # region Check ExecutionReports
        exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": {"NoPartyIDs": parties}, "LastMkt": "*", "VenueType": "*", "MiscFeesGrp": "*",
             "CommissionData": "*"}).remove_parameters(
            ["SettlCurrency", "LastExecutionPolicy", "SecondaryOrderID", "SecondaryExecID"])
        self.fix_verifier.check_fix_message_fix_standard(exec_report)
        # endregion
        # region Create 2n order
        # self.order_ticket.set_order_details(recipient=self.username, partial_desk=True)
        self.order_ticket.re_order()
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        # endregion
        # region Execute Order
        self.order_book.manual_execution(contra_firm=self.data_set.get_contra_firm("contra_firm_2"),
                                         filter_dict=filter_dict)
        self.order_book.complete_order(filter_list=filter_list)
        # endregion
        # region Book orders
        self.mid_office.set_modify_ticket_details(selected_row_count=2)
        self.mid_office.book_order(filter=[OrderBookColumns.recipient.value, self.username])
        # endregion
        # region Check AllocationReport
        self.alloc_report.add_tag(
            {"NoParty": {"NoParty": parties}, "RootCommTypeClCommBasis": "*", "tag5120": "*",
             "RootOrClientCommission": "*", "RootOrClientCommissionCurrency": "*", "RootSettlCurrAmt": "*",
             "NoRootMiscFeesList": "*", "Quantity": "*"})
        self.alloc_report.remove_parameters(
            ["AllocInstructionMiscBlock1", "BookingType"])
        self.alloc_report.add_fields_into_repeating_group("NoOrders", [{"ClOrdID": order_id, "OrderID": order_id}])
        self.fix_verifier_dc.check_fix_message_fix_standard(self.alloc_report)
        # endregion
