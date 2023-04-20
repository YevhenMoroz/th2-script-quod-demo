import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10545(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_verifier_bs = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_4")
        self.alloc_account = self.data_set.get_account_by_name('client_counterpart_4_acc_1')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_4_venue_1")
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.mic = self.data_set.get_mic_by_name('mic_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set needed counterparts:
        client_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_secondary_account_number')[
            JavaApiFields.CounterpartID.value]
        account_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_settlement_account')[
            JavaApiFields.CounterpartID.value]

        self._set_new_counterparts_for_account_and_client(client_counterpart, account_counterpart)
        # endregion

        # region step 1: Create DMA order
        # part 1: Send DMA order
        new_order_single_rule = None
        self.order_submit.set_default_dma_limit()
        price = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        qty = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.OrdQty.value]
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.client_for_rule, self.mic, float(price))
            route = self.data_set.get_route_id_by_name("route_1")
            route_params = {JavaApiFields.RouteBlock.value: [{JavaApiFields.RouteID.value: route}]}
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {JavaApiFields.AccountGroupID.value: self.client,
                                                          JavaApiFields.PreTradeAllocationBlock.value: {
                                                              JavaApiFields.PreTradeAllocationList.value: {
                                                                  JavaApiFields.PreTradeAllocAccountBlock.value: [
                                                                      {
                                                                          JavaApiFields.AllocAccountID.value: self.alloc_account,
                                                                          JavaApiFields.AllocQty.value: qty}]}},
                                                          JavaApiFields.RouteList.value: route_params})
            self.java_api_manager.send_message_and_receive_response(self.order_submit, response_time=12000)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            order_id = order_reply[JavaApiFields.OrdID.value]
            cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                order_reply, 'Verifying that order created')
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region step 2: Check counterparts for Backoffice and BuySide
        list_ignored_field = ['Account', 'ExecID', 'GatingRuleCondName',
                              'OrderQtyData', 'LastQty', 'GatingRuleName',
                              'TransactTime', 'Side', 'AvgPx',
                              'QuodTradeQualifier', 'OrderID',
                              'BookID', 'SettlCurrency', 'SettlDate',
                              'Currency', 'TimeInForce', 'HandlInst',
                              'LeavesQty', 'CumQty', 'LastPx', 'OrdType',
                              'SecondaryOrderID', 'tag5120', 'LastMkt',
                              'Text', 'OrderCapacity', 'QtyType', 'ExecBroker',
                              'Price', 'Instrument', 'PositionEffect',
                              'ExDestination', 'MaxPriceLevels', 'M_PreAllocGrp', 'LastExecutionPolicy',
                              'TradeDate', 'SecondaryExecID', 'GrossTradeAmt', 'PartyRoleQualifier']
        list_of_counterparts = [
            self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user'),
            self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
            self.data_set.get_counterpart_id_fix('counterpart_secondary_account_number'),
            self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
            self.data_set.get_counterpart_id_fix('counterpart_settlement_account'),
            self.data_set.get_counterpart_id_fix('counterpart_java_api_user')
        ]
        parties = [{
            'NoParty': list_of_counterparts,
        },
            {
                'NoPartyIDs': list_of_counterparts[:5]
            }]
        new_order_single = FixMessageNewOrderSingleOMS(self.data_set)
        execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        new_order_single.change_parameters({'ClOrdID': order_id,
                                            "TransactTime": datetime.utcnow().isoformat(),
                                            'Parties': parties[1]})
        self.fix_verifier_bs.check_fix_message_fix_standard(new_order_single, ['ClOrdID'],
                                                            ignored_fields=list_ignored_field)
        execution_report_fix.change_parameters({"ExecType": "0", "OrdStatus": "0", "ClOrdID": cl_ord_id,
                                                'NoParty': parties[0]})
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix, ignored_fields=list_ignored_field)
        # endregion

        # region step 3: Execute DMA order
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.VenueExecID.value: bca.client_orderid(9),
                                                             JavaApiFields.LastTradedQty.value: qty,
                                                             JavaApiFields.LastPx.value: price,
                                                             JavaApiFields.Price.value: price,
                                                             JavaApiFields.CumQty.value: qty,
                                                             JavaApiFields.AvgPrice.value: price,

                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                  ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Verify that order filled')
        execution_report_fix.change_parameters({"ExecType": "F", "OrdStatus": "2", "ClOrdID": cl_ord_id})
        execution_report_fix.change_parameters({"NoParty": parties[0]})
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix, ignored_fields=list_ignored_field)
        # endregion

    def _set_new_counterparts_for_account_and_client(self, counterpart_id_client, counterpart_id_sec_account):
        self.db_manager.execute_query(
            f"UPDATE accountgroup SET counterpartid = '{counterpart_id_client}' WHERE accountgroupid = '{self.client}'")
        if counterpart_id_sec_account is 'null':
            self.db_manager.execute_query(
                f"UPDATE securityaccount SET counterpartid = 'null' WHERE accountid = '{self.alloc_account}'")
        else:
            self.db_manager.execute_query(
                f"UPDATE securityaccount SET counterpartid = '{counterpart_id_sec_account}' WHERE accountid = '{self.alloc_account}'")
        self.ssh_client.send_command("qrestart all")
        time.sleep(200)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        counterpart_id_client = self.data_set.get_counterpart_id_java_api('counterpart_agent')[
            JavaApiFields.CounterpartID.value]
        self._set_new_counterparts_for_account_and_client(counterpart_id_client, 'null')
