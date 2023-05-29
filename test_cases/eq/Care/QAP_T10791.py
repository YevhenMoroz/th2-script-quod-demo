import logging
import traceback
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyAccoutGroupMessage import RestApiModifyAccountGroupMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10791(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_client_by_name("client_rest_api")
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_2')
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.new_ord_single = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.currency = self.data_set.get_currency_by_name('currency_2')
        self.rest_api_message = RestApiModifyAccountGroupMessage(self.data_set, self.environment)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(self.wa_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.qty = '10000'
        self.price = '12593'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create CO order
        self.new_ord_single.set_default_care_market('instrument_3')
        self.new_ord_single.change_parameters({"Account": self.client, 'OrderQtyData': {'OrderQty': self.qty},
                                               'Currency': self.currency})
        self.fix_manager.send_message_and_receive_response(self.new_ord_single)
        response = self.fix_manager.get_last_message('ExecutionReport', "'ExecType': '0'").get_parameters()
        self.fix_manager.compare_values({'ExecType': '0'},
                                        response, 'Verify that order created (step 1)')
        order_id = response['OrderID']
        cl_ord_id = response['ClOrdID']
        # endregion

        # region step  2: Split CO order on child DMA
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.client, self.mic, float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.fix_env.buy_side, self.client, self.mic, float(self.price), int(self.qty), 0)
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {JavaApiFields.Price.value: self.price,
                                                          JavaApiFields.AccountGroupID.value: self.client,
                                                          JavaApiFields.OrdQty.value: self.qty,
                                                          JavaApiFields.ListingList.value: {
                                                              JavaApiFields.ListingBlock.value: [{
                                                                  JavaApiFields.ListingID.value:
                                                                      self.data_set.get_listing_id_by_name(
                                                                          "listing_2")}]},
                                                          JavaApiFields.InstrID.value: self.instrument_id})
            self.ja_manager.send_message_and_receive_response(self.order_submit, filter_dict={cl_ord_id: cl_ord_id})
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region step 3 :
        list_of_ignore_fields = ['GatingRuleCondName', 'GatingRuleName',
                                 'SecondaryOrderID', 'LastMkt', 'Price', 'ReplyReceivedTime']
        execution_report = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.ja_manager.compare_values({JavaApiFields.ExecPrice.value: str(float(self.price))},
                                       execution_report, 'Verify that execution has correct price (step 3)')
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.set_default_filled(self.new_ord_single)
        execution_report.change_parameters({'AvgPx': str((float(self.price) / 100)),
                                            'Currency': self.currency})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignore_fields)
        # endregion
