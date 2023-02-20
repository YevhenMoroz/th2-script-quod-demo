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
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9012(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.trd_request = TradeEntryOMS(self.data_set)
        self.dfd_batch_request = DFDManagementBatchOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.qty = '1000'
        self.price = '10'
        self.exe_price1 = '10'
        self.exe_price2 = '3'
        self.exe_price3 = '5'
        self.exe_price4 = '4'
        self.exe_qty1 = '300'
        self.exe_qty3 = '400'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters({'OrderQtyData': {'OrderQty': self.qty}, 'Price': self.price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # step 1
        # region first manual execute order
        self.trd_request.set_default_trade(order_id, exec_qty=self.exe_qty1)
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        exec_id1 = exec_report_block[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value,
                                              JavaApiFields.ExecPrice.value: self.exe_price1 + '.0',
                                              JavaApiFields.ExecQty.value: self.exe_qty1 + '.0'},
                                             exec_report_block, 'Check first execution')
        # endregion

        # region second manual execute order
        self.trd_request.set_default_trade(order_id, self.exe_price2, self.exe_qty1)
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value,
                                              JavaApiFields.ExecPrice.value: self.exe_price2 + '.0',
                                              JavaApiFields.ExecQty.value: self.exe_qty1 + '.0'},
                                             exec_report_block, 'Check second execution')
        # endregion

        # region third manual execute order
        self.trd_request.set_default_trade(order_id, self.exe_price3, self.exe_qty3)
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value,
                                              JavaApiFields.ExecPrice.value: self.exe_price3 + '.0',
                                              JavaApiFields.ExecQty.value: self.exe_qty3 + '.0'},
                                             exec_report_block, 'Check second execution')
        # endregion

        # step 2
        # region complete order
        self.dfd_batch_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
                                             exec_report_block, 'Check dfd status execution after complete')
        # endregion

        # region 35=8 (39=B) message
        ignored_list_calc = ['GatingRuleCondName', 'GatingRuleName', 'Parties', 'QuodTradeQualifier', 'BookID',
                             'TradeReportingIndicator', 'NoParty', 'tag5120', 'ExecBroker']
        self.exec_report.set_default_calculated(self.fix_message)
        self.exec_report.change_parameters({'LastQty': self.qty, 'AvgPx': '5.9'})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list_calc)
        # endregion

        # step 3
        # region uncomplete order
        self.dfd_batch_request.set_default_uncomplete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch_request)
        # endregion

        # step 4
        # region cancel execution
        self.trd_request.set_default_cancel_execution(order_id, exec_id1)
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value,
                                              JavaApiFields.ExecPrice.value: '0.0',
                                              JavaApiFields.ExecQty.value: '0.0'},
                                             exec_report_block, 'Check first execution')
        # endregion

        # step 5
        # region fourth manual execute order
        self.trd_request = TradeEntryOMS(self.data_set)
        self.trd_request.set_default_trade(order_id, self.exe_price4, self.exe_qty1)
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value,
                                              JavaApiFields.ExecPrice.value: self.exe_price4 + '.0',
                                              JavaApiFields.ExecQty.value: self.exe_qty1 + '.0'},
                                             exec_report_block, 'Check forth execution')
        # endregion

        # step 6
        # region complete order
        self.dfd_batch_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
                                             exec_report_block, 'Check dfd status execution after complete')
        # endregion

        # region 35=8 (150=H) message
        ignored_list_canc = ['GatingRuleCondName', 'GatingRuleName', 'Parties', 'QuodTradeQualifier', 'BookID',
                             'SettlCurrency', 'LastExecutionPolicy', 'TradeDate', 'TradeReportingIndicator', 'NoParty',
                             'tag5120', 'SecondaryOrderID', 'ExecBroker', 'SecondaryExecID']
        self.exec_report.set_default_trade_cancel(self.fix_message)
        self.exec_report.change_parameters({"OrdStatus": "2"})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list_canc)
        # endregion

        # region 35=8 (39=B) message
        ignored_list_calc.extend(
            ['ExecRefID', 'SettlCurrency', 'LastExecutionPolicy', 'SecondaryOrderID', 'TradeDate', 'SecondaryExecID'])
        self.exec_report.set_default_calculated(self.fix_message)
        self.exec_report.change_parameters({'LastQty': self.qty, 'AvgPx': '4.1'})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ['AvgPx', 'ExecType'],
                                                         ignored_fields=ignored_list_calc)
        # endregion
