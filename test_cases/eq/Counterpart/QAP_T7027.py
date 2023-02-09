import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
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
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7027(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.rule_manager = RuleManager(Simulators.equity)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.manual_executing = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        contra_firm = self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm')
        self.fix_message.change_parameters({
            'Parties': {'NoPartyIDs': [
                contra_firm
            ]}})
        responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.set_default_new(self.fix_message)
        order_id = responses[0].get_parameters()['OrderID']
        list_ignored_fields = ['GatingRuleCondName',
                               'GatingRuleName', 'PartyRoleQualifier',
                               'Parties', 'QuodTradeQualifier', 'BookID',
                               'SettlCurrency', 'LastExecutionPolicy',
                               'TradeReportingIndicator', 'SecondaryOrderID',
                               'LastMkt', 'ExecBroker', 'VenueType', 'SecondaryExecID', 'tag5120']
        route_counterpart = self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route')
        custodian_user_2 = self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2')
        custodian_user = self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user')
        gtw_quod4 = self.data_set.get_counterpart_id_fix('counterpart_id_gtwquod4')
        regulatory = self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris')
        party = {'NoParty': [
            route_counterpart,
            custodian_user_2,
            gtw_quod4,
            contra_firm,
            regulatory]}
        execution_report.change_parameters(
            {'NoParty': party})
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report, ignored_fields=list_ignored_fields)
        # endregion

        # region step 1 -4:
        self.manual_executing.set_default_trade(order_id, self.price, self.qty)
        self.manual_executing.update_fields_in_component('TradeEntryRequestBlock', {
            'SourceAccountID': self.data_set.get_account_by_name('client_pos_3_acc_1')
        })
        self.java_api_manager.send_message_and_receive_response(self.manual_executing)
        order_notifications_counterparts = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value). \
            get_parameters()[JavaApiFields.OrderNotificationBlock.value][JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        contra_firm_java_api = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        contra_firm_is_present = False
        for counterpart in order_notifications_counterparts:
            if counterpart == contra_firm_java_api:
                contra_firm_is_present = True
                break
        self.java_api_manager.compare_values({'ContraFirmIsPresent': 'True'},
                                             {'ContraFirmIsPresent': str(contra_firm_is_present)},
                                             'Verifying that Counterpart(ContraFirm) is present (step 3)',
                                             VerificationMethod.CONTAINS)

        execution_report.set_default_filled(self.fix_message)
        contra_firm_fix_java_api = self.data_set.get_counterpart_id_fix('counterpart_java_api_user')
        party = {'NoParty': [
            route_counterpart,
            custodian_user,
            regulatory,
            contra_firm_fix_java_api]}
        execution_report.change_parameters(
            {'NoParty': party})
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report, ignored_fields=list_ignored_fields)
        # endregion
