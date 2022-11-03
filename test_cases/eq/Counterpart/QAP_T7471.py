import logging
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


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
        self.client = self.data_set.get_client_by_name("client_counterpart_2")
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.alloc_report = FixMessageAllocationInstructionReportOMS().set_default_ready_to_book(self.fix_message)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.fix_message.change_parameter('Account', self.client)
        self.price = self.fix_message.get_parameter("Price")
        self.order_type = OrderType.limit.value
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.lookup = self.data_set.get_lookup_by_name('lookup_2')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.manual_execution = TradeEntryOMS(data_set=self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.username = environment.get_list_fe_environment()[0].user_1

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create Care order
        class_name = QAP_T7471
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        instr_id = self.data_set.get_instrument_id_by_name("instrument_2")
        parties = [
            {'PartyRole': "28",
             'PartyID': "CustodianUser",
             'PartyIDSource': "C"},
            self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm'),
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
        ]
        # endregion
        # region Execute Order
        self.manual_execution.set_default_trade(order_id, self.price)
        self.manual_execution.update_fields_in_component('TradeEntryRequestBlock',
                                                         {'CounterpartList': {'CounterpartBlock':
                                                             [self.data_set.get_counterpart_id_java_api(
                                                                 'counterpart_contra_firm')]
                                                         }})
        responses = self.java_api_manager.send_message_and_receive_response(self.manual_execution)
        class_name.__print_message('Manual Execute First Order', responses)
        exec_id = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ExecID.value]
        responses = self.java_api_manager.send_message_and_receive_response(
            self.complete_order.set_default_complete(order_id))
        class_name.__print_message('Complete First Order', responses)
        # endregion
        # region Check ExecutionReports
        list_of_ignored_fields = ['SecurityDesc', 'CommissionData', 'RootSettlCurrAmt', 'AllocInstructionMiscBlock1',
                                  'MiscFeesGrp', 'BookingType', 'RootOrClientCommission',
                                  'RootOrClientCommissionCurrency', 'RootCommTypeClCommBasis', 'Account',
                                  'NoRootMiscFeesList']
        exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": {"NoPartyIDs": parties}, "LastMkt": "*", "VenueType": "*", "MiscFeesGrp": "*",
             "CommissionData": "*"}).remove_parameters(
            ["SettlCurrency", "LastExecutionPolicy", "SecondaryOrderID", "SecondaryExecID"])
        self.fix_verifier.check_fix_message_fix_standard(exec_report, ignored_fields=list_of_ignored_fields)
        # endregion
        # region Create 2n order
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                       {'OrdCapacity': SubmitRequestConst.OrdCapacity_Agency.value,
                                                        'OrdQty': self.qty,
                                                        'AccountGroupID': self.client,
                                                        'Price': self.price,
                                                        'InstrID': instr_id,
                                                        'ListingList': {'ListingBlock': [{
                                                            'ListingID': self.data_set.get_listing_id_by_name(
                                                                "listing_3")}]}})

        self.submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        class_name.__print_message('New Second Order ', responses)
        order_id_second = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]
        # endregion
        # region Execute Order
        self.manual_execution.set_default_trade(order_id_second, self.price)
        self.manual_execution.update_fields_in_component('TradeEntryRequestBlock',
                                                         {'CounterpartList': {'CounterpartBlock':
                                                             [self.data_set.get_counterpart_id_java_api(
                                                                 'counterpart_contra_firm_2')]
                                                         }})
        responses = self.java_api_manager.send_message_and_receive_response(self.manual_execution)
        exec_id_second = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ExecID.value]
        class_name.__print_message('Manual Execute Second Order', responses)
        responses = self.java_api_manager.send_message_and_receive_response(
            self.complete_order.set_default_complete(order_id_second))
        class_name.__print_message('Complete Second Order', responses)
        # endregion
        # region Book orders
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component("AllocationInstructionBlock", {
            "OrdAllocList": {"OrdAllocBlock": [{"OrdID": order_id}, {"OrdID": order_id_second}]}})
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            'Qty': str(int(int(self.qty) * 2)),
            "InstrID": instr_id,
            'AllocInstructionID': 0,
            "AccountGroupID": self.client,
            'AvgPx': self.price,
            'ExecAllocList': {
                'ExecAllocBlock': [{'ExecQty': self.qty, 'ExecID': exec_id_second, 'ExecPrice': self.price},
                                   {'ExecQty': self.qty, 'ExecID': exec_id,
                                    'ExecPrice': self.price}]}
        })
        self.java_api_manager.send_message(self.allocation_instruction)
        # endregion

        # region Check AllocationReport
        parties[1] = self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm_2')
        self.alloc_report.add_tag(
            {"NoParty": {"NoParty": parties}, "RootCommTypeClCommBasis": "*", "tag5120": "*",
             "RootOrClientCommission": "*", "RootOrClientCommissionCurrency": "*", "Quantity": "*", })
        self.alloc_report.add_fields_into_repeating_group("NoOrders",
                                                          [{"ClOrdID": '*', "OrderID": order_id_second}])
        self.fix_verifier_dc.check_fix_message_fix_standard(self.alloc_report, ignored_fields=list_of_ignored_fields)
        # endregion

    @staticmethod
    def __print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
