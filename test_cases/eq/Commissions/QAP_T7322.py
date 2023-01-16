import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import  JavaApiFields, OrderReplyConst, \
    ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7322(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.cur_fee = self.data_set.get_currency_by_name('currency_2')
        self.qty = "900"
        self.qty_to_first_split = "500"
        self.qty_to_second_split = "400"
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = "10"
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.fix_message.change_parameters(
            {"Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.cur, "Price": self.price, 'OrderQtyData': {'OrderQty': self.qty}})
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_qty")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        self.ord_scope = self.data_set.get_fee_order_scope_by_name('done_for_day')
        self.exec_scope = self.data_set.get_fee_exec_scope_by_name('all_exec')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_2")
        self.route_id = self.data_set.get_route_id_by_name('route_1')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.comm_profile).change_message_params(
            {'commExecScope': self.exec_scope, "orderCommissionProfileID": self.comm_profile,
             "miscFeeType": self.fee_type, "routeID": self.route_id,
             "commOrderScope": self.ord_scope}).send_post_request()
        # endregion
        # region send order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        cl_ord_id = response[0].get_parameter("ClOrdID")
        # endregion

        # region first split order
        responses = self.__split_order(self.qty_to_first_split, order_id)
        # endregion

        # region check first order
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        order_reply = self.result.get_parameter('OrdUpdateBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_TER.value},
            order_reply, "Check the first child order open sts")
        self.__return_result(responses, ORSMessageType.PositionReport.value)
        order_reply = self.result.get_parameter('PositionReportBlock')
        posit_block = order_reply['PositionList']['PositionBlock'][0]
        exec_id_1 = posit_block['LastPositUpdateEventID']
        ignored_list_1 = ['ReplyReceivedTime', 'Currency', 'SecondaryOrderID', 'SettlType', 'CommissionData', 'LastMkt']
        misc_fee1 = {'NoMiscFees': [{'MiscFeeAmt': '0.5', 'MiscFeeCurr': self.cur_fee, 'MiscFeeType': '12'}]}
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters({'ExecID': exec_id_1, 'OrdStatus': '1', 'MiscFeesGrp': misc_fee1})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ['ExecID'], ignored_fields=ignored_list_1)
        # endregion

        # region second split order
        responses = self.__split_order(self.qty_to_second_split, order_id)
        # endregion

        # region check first order
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        order_reply = self.result.get_parameter('OrdUpdateBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_TER.value},
            order_reply, "Check the second child order open sts")
        self.__return_result(responses, ORSMessageType.PositionReport.value)
        order_reply = self.result.get_parameter('PositionReportBlock')
        posit_block = order_reply['PositionList']['PositionBlock'][0]
        exec_id_2 = posit_block['LastPositUpdateEventID']
        misc_fee2 = {'NoMiscFees': [{'MiscFeeAmt': '0.4', 'MiscFeeCurr': self.cur_fee, 'MiscFeeType': '12'}]}
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters({'ExecID': exec_id_2, 'MiscFeesGrp': misc_fee2})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ['ExecID'], ignored_fields=ignored_list_1)
        # endregion

        # region check execution after complete parent order
        self.complete_order.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        self.__return_result(responses, ORSMessageType.ExecutionReport.value)
        exec_report_par = self.result.get_parameter('ExecutionReportBlock')
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value,
                                              JavaApiFields.ExecCommission.value: '0.9'},
                                             exec_report_par, "Check the parent order execution")
        # endregion

    def __split_order(self, qty, order_id):
        try:
            open_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                   self.client_for_rule,
                                                                                                   self.mic,
                                                                                                   int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(qty), 2)
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'OrdQty': qty,
                                                                                 'ListingList': {'ListingBlock': [{
                                                                                     'ListingID': self.data_set.get_listing_id_by_name(
                                                                                         "listing_2")}]},
                                                                                 'InstrID': self.data_set.get_instrument_id_by_name(
                                                                                     "instrument_3"),
                                                                                 'Price': self.price,
                                                                                 'AccountGroupID': self.client})
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(open_rule)
            self.rule_manager.remove_rule(trade_rule)
        return responses

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
