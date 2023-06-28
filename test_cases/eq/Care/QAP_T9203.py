import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T9203(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.trade_request = TradeEntryOMS(self.data_set)
        self.fix_verifier_back_office = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.dfd_manage = DFDManagementBatchOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create Care order (step 1)
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        ord_id = response[0].get_parameter("OrderID")
        cl_ord_id = response[0].get_parameter("ClOrdID")
        # endregion

        # region manual execute order (step 2)
        contra_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        executing_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm')
        self.trade_request.set_default_trade(ord_id)
        self.trade_request.update_fields_in_component('TradeEntryRequestBlock',
                                                      {"CounterpartList": {'CounterpartBlock': [contra_firm_counterpart,
                                                                                                executing_firm_counterpart]}})
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion

        # region check  35=8 (39 = 2) message on the Back Office (step 3)
        params = {"ExecType": "F",
                  "OrdStatus": "2", "ClOrdID": cl_ord_id, 'OrderID': ord_id}
        list_of_ignored_fields = ['Account', 'ExecID', 'OrderQtyData', 'LastQty',
                                  'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier', 'BookID',
                                  'SettlDate', 'TimeInForce', 'Currency', 'PositionEffect',
                                  'TradeDate', 'HandlInst', 'LeavesQty', 'CumQty', 'LastPx',
                                  'OrdType', 'tag5120', 'LastMkt', 'OrderCapacity',
                                  'QtyType', 'ExecBroker', 'Price', 'VenueType',
                                  'Instrument', 'NoParty', 'ExDestination', 'GrossTradeAmt',
                                  'AllocInstructionMiscBlock2', 'CommissionData', 'GatingRuleName',
                                  'GatingRuleCondName']
        fix_exec_report = FixMessageExecutionReportOMS(self.data_set, params)
        self.fix_verifier_back_office.check_fix_message_fix_standard(fix_exec_report,
                                                                     ignored_fields=list_of_ignored_fields)
        # endregion

        # region complete order (step 4)
        self.dfd_manage.set_default_complete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_manage)
        # endregion

        # region check  35=8 (39 = B) message on the Back Office (step 5)
        params = {"ExecType": "B",
                  "OrdStatus": "B", "ClOrdID": cl_ord_id, 'OrderID': ord_id}
        fix_exec_report = FixMessageExecutionReportOMS(self.data_set, params)
        self.fix_verifier_back_office.check_fix_message_fix_standard(fix_exec_report,
                                                                     ignored_fields=list_of_ignored_fields)
        # endregion
