import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7473(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.account = self.data_set.get_account_by_name("client_counterpart_1_acc_3")
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.confirmation = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region DMA order
        eurex_instrument = self.data_set.get_java_api_instrument('instrument_3')
        self.new_order_single.set_default_dma_limit()
        cl_ord_id = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.ClOrdID.value]
        qty = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.OrdQty.value]
        price = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.Price.value]
        self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {
                                                             'InstrumentBlock': eurex_instrument,
                                                             'ClientAccountGroupID': self.client,
                                                             'PreTradeAllocationBlock': {
                                                                 'PreTradeAllocationList': {
                                                                     'PreTradeAllocAccountBlock': [{
                                                                         'AllocClientAccountID': self.account,
                                                                         'AllocQty': qty
                                                                     }]
                                                                 }
                                                             }
                                                         })
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(price))
            trade_rele = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(price),
                                                                                            int(qty), 2)

            self.java_api_manager.send_message_and_receive_response(self.new_order_single)
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rele)
        # endregion
        # region Set-up parameters for ExecutionReports
        parties = {
            'NoParty': [
                self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa3'),
                self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user'),
                self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                self.data_set.get_counterpart_id_fix('counterpart_java_api_user')
            ]
        }
        exec_report = FixMessageExecutionReportOMS(self.data_set).change_parameters(
            {"NoParty": parties,
             "ExecType": "0",
             "OrdStatus": "0",
             'ClOrdID': cl_ord_id
             })
        exec_report.change_parameters({
            "ExecType": "F",
            "OrdStatus": "2"
        })
        # endregion
        # region Check ExecutionReports
        list_ignored_fields = ['Account', 'NoMiscFees',
                               'CommissionData', 'MiscFeesGrp', 'OrderAvgPx', 'ReplyReceivedTime',
                               'GatingRuleCondName', 'ExecID', 'OrderQtyData',
                               'LastQty', 'OrderID', 'TransactTime', 'Side',
                               'AvgPx', 'QuodTradeQualifier', 'BookID',
                               'GatingRuleName', 'SettlCurrency',
                               'SettlDate', 'Currency', 'TimeInForce',
                               'HandlInst', 'LeavesQty', 'CumQty',
                               'LastPx', 'OrdType', 'SecondaryOrderID',
                               'tag5120', 'LastMkt', 'Text', 'OrderCapacity',
                               'QtyType', 'ExecBroker', 'Price', 'Instrument',
                               'M_PreAllocGrp',
                               'LastExecutionPolicy', 'PositionEffect',
                               'TradeDate', 'SecondaryExecID', 'ExDestination',
                               'GrossTradeAmt', 'RootSettlCurrFxRateCalc',
                               'AllocID', 'NetMoney', 'BookingType', 'RootSettlCurrency',
                               'AllocInstructionMiscBlock1', 'Quantity',
                               'AllocTransType', 'ReportedPx', 'RootSettlCurrFxRate',
                               'RootSettlCurrAmt', 'tag11245', 'CpctyConfGrp', 'GrossTradeAmt',
                               'ConfirmID', 'ConfirmStatus', 'MatchStatus', 'ConfirmType',
                               'AllocQty', 'SettlCurrAmt', 'SettlCurrFxRateCalc',
                               'SettlCurrFxRate', 'NoAllocs']
        self.fix_verifier_dc.check_fix_message_fix_standard(exec_report,
                                                            ignored_fields=list_ignored_fields)
        self.fix_verifier_dc.check_fix_message_fix_standard(exec_report,
                                                            ignored_fields=list_ignored_fields)
        # endregion
        # region Set-up parameters Confirmation report
        conf_report = FixMessageConfirmationReportOMS(self.data_set).change_parameters(
            {"NoParty": parties, "Account": self.client, "tag5120": "*", "AllocAccount": self.account,
             'ConfirmTransType': "0",
             'NoOrders': [{
                 'ClOrdID': cl_ord_id
             }]
             })
        # endregion
        # region Check Book & Allocation
        del parties.get('NoParty')[len(parties.get('NoParty')) - 1]
        parties.get('NoParty').append({
            'PartyRole': '*',
            'PartyID': '*',
            'PartyIDSource': '*'
        })
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ignored_fields=list_ignored_fields)
        # endregion

        # region step 9: Amend ConfirmationReport
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClAllocID.value]
        confirmation_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value). \
            get_parameters()[JavaApiFields.ConfirmationReportBlock.value]
        confirmation_id = confirmation_report[JavaApiFields.ConfirmationID.value]
        new_price = '20'
        self.confirmation.set_default_amend_allocation(confirmation_id, alloc_id, price=new_price)
        self.confirmation.update_fields_in_component('ConfirmationBlock', {"AllocAccountID": self.account,
                                                                           'InstrID': self.data_set.get_instrument_id_by_name(
                                                                               "instrument_3")})
        self.java_api_manager.send_message_and_receive_response(self.confirmation)
        conf_report = FixMessageConfirmationReportOMS(self.data_set).change_parameters(
            {"NoParty": parties, "Account": self.client, "AllocAccount": self.account,
             "AvgPx": new_price, 'ConfirmTransType': "1",
             'NoOrders': [{'ClOrdID': cl_ord_id}]})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ignored_fields=list_ignored_fields)
        # endregion
