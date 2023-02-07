import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst, OrderReplyConst, \
    ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7049(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.manual_cross = ManualOrderCrossRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition: Create 2 CO orders:
        orders_ids = []
        cl_ord_ids = []
        recipient = self.environment.get_list_fe_environment()[0].user_1
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        role = SubmitRequestConst.USER_ROLE_1.value
        list_of_qty = ['100', '200']
        list_of_sides = ['Buy', 'Sell']
        self.order_submit.set_default_care_limit(recipient=recipient, desk=desk, role=role)
        price = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.Price.value]
        for counter in range(2):
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
                JavaApiFields.OrdQty.value: list_of_qty[counter],
                JavaApiFields.Side.value: list_of_sides[counter],
                JavaApiFields.ClOrdID.value: bca.client_orderid(9)
            })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            orders_ids.append(order_reply[JavaApiFields.OrdID.value])
            cl_ord_ids.append(order_reply[JavaApiFields.ClOrdID.value])
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, f'Verify that order {orders_ids[counter]} has Sts = Open')
        # endregion

        # region step 1-2: Manual Cross CO orders
        self.manual_cross.set_default(self.data_set, orders_ids[0], orders_ids[1], price, exec_qty=list_of_qty[0])
        self.manual_cross.update_fields_in_component('ManualOrderCrossRequestBlock', {
            'LastMkt': 'XOSE'
        })
        list_unmatched_qty = ['0.0', str(float(list_of_qty[0]))]
        list_exec_status = [ExecutionReportConst.TransExecStatus_FIL.value, ExecutionReportConst.TransExecStatus_PFL.value]
        self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        for counter in range(2):
            execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, orders_ids[counter]).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.UnmatchedQty.value: list_unmatched_qty[counter],
                                                  JavaApiFields.TransExecStatus.value:list_exec_status[counter]}, execution_report,
                                                 f'Verify that {orders_ids[counter]} has correct results (step 2)')
        # endregion

        # region step 3: Check 35 = 8 message
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        list_ignored_fields = [
            'Account', 'ExecID', 'GatingRuleCondName', 'OrderQtyData', 'LastQty', 'GatingRuleName', 'TransactTime',
            'Side','PartyRoleQualifier'
            'AvgPx', 'QuodTradeQualifier', 'BookID', 'SettlCurrency', 'TrdSubType', 'SettlDate', 'Currency',
            'TimeInForce',
            'PositionEffect', 'TradeDate', 'HandlInst', 'TrdType', 'LeavesQty', 'CumQty',
            'LastPx', 'LastCapacity', 'OrdType', 'tag5120', 'LastMkt',
            'OrderCapacity', 'QtyType', 'ExecBroker', 'Price',
            'VenueType', 'Instrument', 'ExDestination',
            'NoMiscFees', 'GrossTradeAmt', 'CommissionData'
        ]
        list_ord_status = ['1', '2']
        for counter in range(2):
            execution_report.change_parameters({
                "ExecType": "F",
                "OrdStatus": list_ord_status[counter],
                "ClOrdID": cl_ord_ids[counter],
                'OrderID': orders_ids[counter],
                'NoParty': [
                    self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                    self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user'),
                    self.data_set.get_counterpart_id_fix('counterpart_java_api_user'),
                    self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris')]
            })
            self.fix_verifier.check_fix_message_fix_standard(execution_report, ['ClOrdID', 'OrdStatus', 'ExecType'],
                                                             ignored_fields=list_ignored_fields)
        # endregion
