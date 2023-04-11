import logging
import time
from pathlib import Path
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst, \
    BasketMessagesConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderListOMS import FixNewOrderListOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()

def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())

class QAP_T7365(TestCase):
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
        self.fix_orderlist_submit = FixNewOrderListOMS(self.data_set)
        self.price = '10'
        self.qty = '100'
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create basket: Step 1
        self.fix_orderlist_submit.set_default_order_list()
        responses = self.java_api_manager.send_message_and_receive_response(self.fix_orderlist_submit, response_time=15000)
        print_message("Create Basket", responses)

        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value
        ).get_parameter(JavaApiFields.OrdListNotificationBlock.value)

        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            list_notify_block,
            "Step 1 - Checking Status for created Basket",
        )
        # endregion

        # region
        # try:
        #     nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
        #                                                                                           self.rule_client,
        #                                                                                           self.mic,
        #                                                                                           float(self.price))
        #
        #     response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        #     # endregion
        # finally:
        #     time.sleep(1)
        #     self.rule_manager.remove_rule(nos_rule)
            # self.rule_manager.remove_rule(trade_rule)
            # region check exec report

        # co_orders_id = []
        # co_orders_id.append(self.params1['ClOrdID'])
        # co_orders_id.append(self.params2['ClOrdID'])
        # orders_id = []
        # for counter in response:
        #     orders_id.append(response[counter].get_parameters()['OrderID'])


        # list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
        #                           'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
        #                           'QuodTradeQualifier', 'BookID', 'SettlDate',
        #                           'AllocID', 'Currency', 'NetMoney',
        #                           'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
        #                           'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
        #                           'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
        #                           'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
        #                           'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
        #                           'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
        #                           'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
        #                           'SecondaryExecID', 'NoParty', 'Text', 'NoStrategyParameters',
        #                           'SettlCurrency', 'StrategyName'
        #                           ]
        #
        #
        # execution_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.fix_message)
        # execution_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.fix_message, 1)
        # execution_report1.change_parameters({'ExecType': '4', "OrdStatus": "4", 'ClOrdID':co_orders_id[0]})
        # execution_report2.change_parameters({'ExecType': '4', "OrdStatus": "4", 'ClOrdID':co_orders_id[1]})
        # self.fix_verifier_dc.check_fix_message_fix_standard(execution_report1, ignored_fields=list_of_ignored_fields)
        # self.fix_verifier_dc.check_fix_message_fix_standard(execution_report2, ignored_fields=list_of_ignored_fields)
