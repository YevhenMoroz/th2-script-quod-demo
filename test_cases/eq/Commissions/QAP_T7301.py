import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7301(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bo_connectivity = self.fix_env.drop_copy
        self.fix_verifier_dc = FixVerifier(self.bo_connectivity, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.submit_request.set_default_care_limit(
            self.data_set.get_recipient_by_name("recipient_user_1"), "1")
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        cl_ord_id = ord_notif.get_parameter("OrdNotificationBlock")["ClOrdID"]
        client = ord_notif.get_parameter("OrdNotificationBlock")["AccountGroupID"]
        # endregion
        # region Step 2
        self.trade_request.set_default_trade(ord_id)
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {
            "MiscFeesList": {"MiscFeesBlock": [{"MiscFeeType": "AGE", "MiscFeeAmt": "10", "MiscFeeBasis": "A"}]}})
        self.java_api_manager.send_message(self.trade_request)
        # endregion
        # region check exec report
        list_of_ignore_fields = ['SecondaryOrderID', 'LastExecutionPolicy', 'TradeDate', 'SecondaryExecID', 'OrderID',
                                 'ExDestination', 'GrossTradeAmt', 'SettlCurrency', 'Instrument', 'TimeInForce',
                                 'OrdType', "TradeReportingIndicator", 'SettlDate', 'Side', 'HandlInst', 'OrderQtyData',
                                 'SecondaryExecID', 'ExecID', 'LastQty', 'TransactTime', 'AvgPx', 'QuodTradeQualifier',
                                 'BookID', 'Currency', 'PositionEffect', 'TrdType', 'LeavesQty', 'NoParty', 'CumQty',
                                 'LastPx', 'LastCapacity', 'tag5120', 'LastMkt', 'OrderCapacity''QtyType', 'ExecBroker',
                                 'QtyType', 'Price', 'OrderCapacity', 'VenueType', 'CommissionData']
        change_parameters = {
            "ExecType": "F", "OrdStatus": "2", "Account": client, "ClOrdID": cl_ord_id,
            'NoMiscFees': [{'MiscFeeAmt': "10", 'MiscFeeCurr': '*', 'MiscFeeType': "12"}]
        }
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set, change_parameters)
        self.fix_verifier_dc.check_fix_message_fix_standard(fix_execution_report, ignored_fields=list_of_ignore_fields)
        # endregion
