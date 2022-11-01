import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7319(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.qty = "900"
        self.qty_to_first_split = "500"
        self.qty_to_second_split = "400"
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = "10"
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.fix_message.change_parameters(
            {"Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.cur, "Price": self.price, 'OrderQtyData': {'OrderQty': self.qty}})
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_qty")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        self.exec_scope = self.data_set.get_fee_exec_scope_by_name('all_exec')
        self.contra_firm = self.data_set.get_counterpart('counterpart_cnf_1')
        self.username = self.fe_env.user_1  # JavaApiUser
        self.counterpart_id = self.data_set.get_counterpart_id('contra_firm')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.comm_profile).change_message_params(
            {'commExecScope': self.exec_scope, "orderCommissionProfileID": self.comm_profile,
             "miscFeeType": self.fee_type, "contraFirmCounterpartID": self.counterpart_id}).send_post_request()
        # endregion
        # region send order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        # endregion
        # region first split order
        self.order_submit.set_default_child_care(recipient=self.username,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value,
                                                 parent_id=order_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'OrdQty': self.qty_to_first_split,
                                                                             'ListingList': {'ListingBlock': [{
                                                                                 'ListingID': self.data_set.get_listing_id_by_name(
                                                                                     "listing_3")}]},
                                                                             'InstrID': self.data_set.get_instrument_id_by_name(
                                                                                 "instrument_3"), 'Price': self.price})
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        self.__return_result(responses, ORSMessageType.OrdReply.value)
        child_order_id_1 = self.result.get_parameter('OrdReplyBlock')['RequestID']
        # endregion
        # region second split order
        self.order_submit.set_default_child_care(recipient=self.username,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value,
                                                 parent_id=order_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'OrdQty': self.qty_to_second_split,
                                                                             'ListingList': {'ListingBlock': [{
                                                                                 'ListingID': self.data_set.get_listing_id_by_name(
                                                                                     "listing_3")}]},
                                                                             'InstrID': self.data_set.get_instrument_id_by_name(
                                                                                 "instrument_3"), 'Price': self.price})
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        self.__return_result(responses, ORSMessageType.OrdReply.value)
        child_order_id_2 = self.result.get_parameter('OrdReplyBlock')['RequestID']
        # endregion
        # region 1 order manual executions
        self.trade_entry_request.set_default_trade(child_order_id_1, exec_qty=self.qty_to_first_split)
        self.trade_entry_request.update_fields_in_component('TradeEntryRequestBlock', {
            "CounterpartList": {'CounterpartBlock':[self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')]}})
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion
        # region 2 order manual executions
        self.trade_entry_request.set_default_trade(child_order_id_2, exec_qty=self.qty_to_second_split)
        self.trade_entry_request.update_fields_in_component('TradeEntryRequestBlock', {
            "CounterpartList": {
                'CounterpartBlock': [self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')]}})
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # self.child_book.manual_execution(contra_firm=self.contra_firm,
        #                                  filter_dict={ChildOrderBookColumns.order_id.value: child_order_id1})
        # self.child_book.manual_execution(contra_firm=self.contra_firm,
        #                                  filter_dict={ChildOrderBookColumns.order_id.value: child_order_id2})
        # self.__check_feeAgent_sub_lvl_details(child_order_id1, "5")
        # self.__check_feeAgent_sub_lvl_details(child_order_id2, "4")
        # # endregion
        # # region check ExecReports on BO
        # no_misc1 = {"MiscFeeAmt": '5', "MiscFeeCurr": self.com_cur,
        #             "MiscFeeType": "12"}
        # execution_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        # execution_report.change_parameters(
        #     {'SecondaryOrderID': child_order_id1, 'OrdStatus': '1', 'QuodTradeQualifier': "*", 'Currency': self.cur,
        #      'LastMkt': "*", "VenueType": '*',
        #      "Account": self.client, "NoMiscFees": {"NoMiscFees": [no_misc1]}, "CommissionData": "*", "ExecBroker": "*",
        #      "tag5120": "*", "NoParty": "*", 'BookID': "*"})
        # execution_report.remove_parameters(
        #     ['SettlCurrency', "TradeReportingIndicator", 'Parties', 'LastExecutionPolicy'])
        # self.fix_verifier_dc.check_fix_message_fix_standard(execution_report, ['SecondaryOrderID'])
        # no_misc2 = {"MiscFeeAmt": '4', "MiscFeeCurr": self.com_cur,
        #             "MiscFeeType": "12"}
        # execution_report.change_parameters(
        #     {'SecondaryOrderID': child_order_id2, "NoMiscFees": {"NoMiscFees": [no_misc2]}, 'OrdStatus': '2'})
        # self.fix_verifier_dc.check_fix_message_fix_standard(execution_report, ['SecondaryOrderID'])
        # # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
