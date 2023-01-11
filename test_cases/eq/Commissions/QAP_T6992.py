import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T6992(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_message.change_parameters(
            {"Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.cur})
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.price = self.fix_message.get_parameter('Price')
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.trade_entry_request = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        # endregion
        # region send order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        # endregion
        # region manual execute order
        self.trade_entry_request.set_default_trade(order_id, exec_qty=self.qty, exec_price=self.price)
        self.trade_entry_request.update_fields_in_component('TradeEntryRequestBlock',
                                                            {'LastMkt': self.data_set.get_mic_by_name("mic_2")})
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        self.__return_result(responses, ORSMessageType.ExecutionReport.value)
        exec_report = self.result.get_parameter('ExecutionReportBlock')
        # endregion
        # region check ManualDayCumAmt and ManualDayCumQty
        qty_exp = self.qty +'.0'
        amt_exp = str(int(self.qty) * int(self.price))+'.0'
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value,
                                              JavaApiFields.ManualDayCumQty.value: qty_exp,
                                              JavaApiFields.ManualDayCumAmt.value: amt_exp},
                                             exec_report, 'Check ManualDayCumAmt and ManualDayCumQty')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
