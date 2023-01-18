import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T8320(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ord_sub_message = OrderSubmitOMS(self.data_set)
        self.ord_sub_message2 = OrderSubmitOMS(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order
        self.ord_sub_message.set_default_care_limit(self.environment.get_list_fe_environment()[0].user_1,
                                                    self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                    SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.ord_sub_message)
        cl_order_id = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)["ClOrdID"]
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)["OrdID"]
        # endregion
        # region create child
        self.ord_sub_message2.set_default_child_care(self.environment.get_list_fe_environment()[0].user_1,
                                                     self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                     SubmitRequestConst.USER_ROLE_1.value, order_id)
        self.java_api_manager.send_message_and_receive_response(self.ord_sub_message2)
        child_order_id = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)["OrdID"]
        # endregion
        # region execute child
        self.trade_entry.set_default_trade(child_order_id)
        self.java_api_manager.send_message(self.trade_entry)
        # endregion
        execution_params = {"ClOrdID": cl_order_id, "SecondaryOrderID": child_order_id}
        self.exec_report.set_default_filled(self.fix_message).change_parameters(execution_params)
        ignored_fields = ["GatingRuleCondName", "GatingRuleName", "Parties", "QuodTradeQualifier", "BookID",
                          "LastExecutionPolicy", "PositionEffect", "TradeReportingIndicator", "NoParty", "tag5120",
                          "LastMkt", "ExecBroker", "VenueType", "Instrument"]
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_fields)
