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
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7304(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "15"
        self.qty_to_exec = '50'
        self.price_to_exec = '11.4'
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit('instrument_3')
        self.fix_message.change_parameters(
            {'Price': self.price, 'OrderQtyData': {'OrderQty': self.qty}, "Currency": self.currency})
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region create first CO
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region manual exec
        self.trade_entry_request.set_default_trade(order_id, self.price_to_exec, self.qty_to_exec)
        self.trade_entry_request.update_fields_in_component('TradeEntryRequestBlock',
                                                            {'LastMkt': self.data_set.get_mic_by_name("mic_2")})
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # region check values after execution
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.DayCumAmt.value: str(float(self.price_to_exec) * int(self.qty_to_exec)),
             JavaApiFields.AvgPrice.value: self.price_to_exec}, exec_report_block,
            'Check execution of order')
        # endregion

        # region check execution report
        self.exec_report.set_default_filled(self.fix_message)
        ignore_list = ['GatingRuleCondName', 'GatingRuleName', 'SettlCurrency', 'LastExecutionPolicy', 'Currency',
                       'SecondaryOrderID', 'LastMkt', 'VenueType', 'SecondaryExecID']
        self.exec_report.change_parameters(
            {"OrdStatus": "1", 'Price': self.price, 'AvgPx': self.price_to_exec, 'LastPx': self.price_to_exec})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignore_list)
        # endregion
