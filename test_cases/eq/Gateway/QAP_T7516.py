import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7516(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.price = '10'
        self.qty = '100'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order with algo param execute it:Step 1
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            float(self.price),
                                                                                            int(self.qty), 2)
            self.submit_request.set_default_dma_limit(with_external_algo=True)
            cl_ord_id = self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
                JavaApiFields.ClOrdID.value]
            route_params = {'RouteBlock': [{'RouteID': self.data_set.get_route_id_by_name("route_1")}]}
            self.submit_request.update_fields_in_component('NewOrderSingleBlock', {
                JavaApiFields.OrdQty.value: self.qty,
                JavaApiFields.RouteList.value: route_params,
                JavaApiFields.AccountGroupID.value: self.client, JavaApiFields.Price.value: self.price
            })
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                                 OrderReplyConst.TransStatus_SEN.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values({
                JavaApiFields.OrdQty.value:  str(float(self.qty)),
                JavaApiFields.Price.value: str(float(self.price)),
                JavaApiFields.Side.value: SubmitRequestConst.Side_B_aka_Buy.value,
                JavaApiFields.AccountGroupID.value: self.client,
                JavaApiFields.ExternalAlgoParametersBlock.value:
                    self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
                        JavaApiFields.ExternalAlgoParametersBlock.value],
                JavaApiFields.InstrID.value:
                    self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
                        JavaApiFields.InstrID.value]
            },
                order_reply, 'Verifying that Order has needed parameters (step 1)')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region check exec report: step 2-3
        change_parameters = {
            'ClOrdID': cl_ord_id,
        }
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
                                  'SecondaryExecID', 'NoParty', 'Text', 'NoStrategyParameters',
                                  'SettlCurrency'
                                  ]
        execution_report = FixMessageExecutionReportOMS(self.data_set, change_parameters)
        execution_report.change_parameters({'ExecType': 'F', "OrdStatus": "2",
                                            'StrategyName': '1025'})
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion
