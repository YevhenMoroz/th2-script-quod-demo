import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import TradeBookColumns, OrderBookColumns, SecondLevelTabs, \
    CommissionType, CommissionBasis
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7123(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.price = self.fix_message.get_parameter('Price')
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fee = self.data_set.get_fee_by_name('fee1')
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        self.fee_route_id = self.data_set.get_route_id_by_name('route_1')
        self.exec_scope = self.data_set.get_fee_exec_scope_by_name('all_exec')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.comm_profile,
                                                            fee_type=self.fee_type).change_message_params(
            {'venueID': self.venue, "routeID": self.fee_route_id, 'commExecScope': self.exec_scope}).send_post_request()
        # endregion
        # region send order
        self.__send_fix_orders()
        order_id = self.response[0].get_parameter("OrderID")
        # endregion
        # region check order ExecutionReports
        self.exec_report.set_default_filled(self.fix_message)
        no_misc = {"MiscFeeAmt": '1', "MiscFeeCurr": self.com_cur,
                   "MiscFeeType": "12"}
        self.exec_report.change_parameters(
            {'Side': "1", 'Currency': self.cur, 'SecondaryOrderID': '*', 'Text': '*', 'LastMkt': '*',
             "ReplyReceivedTime": "*", "Account": self.client, "MiscFeesGrp": {"NoMiscFees": [no_misc]},
             "CommissionData": '*'})
        self.exec_report.remove_parameter('SettlCurrency')
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion
        # region extract execution id
        exec_id = self.order_book.extract_sub_lvl_fields([OrderBookColumns.exec_id.value],
                                                         [SecondLevelTabs.executions.value],
                                                         {OrderBookColumns.order_id.value: order_id})
        # endregion
        # region check execution fields
        self.__check_misc_tab_execution(
            {TradeBookColumns.fee_type.value: CommissionType.agent.value,
             TradeBookColumns.fee_basis.value: CommissionBasis.persentage.value,
             TradeBookColumns.fee_rate.value: "5", TradeBookColumns.fee_currency.value: self.com_cur}, exec_id)
        # endregion

    def __send_fix_orders(self):
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty), int(self.qty), 1)
            self.fix_message.change_parameters(
                {"Account": self.client,
                 "ExDestination": self.mic,
                 "Currency": self.data_set.get_currency_by_name("currency_3")})
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

    def __check_misc_tab_execution(self, dict_of_fields: dict, exec_id: dict):
        for name_field, expect_res in dict_of_fields.items():
            res = self.trades.extract_sub_lvl_fields([name_field],
                                                     TradeBookColumns.misc_tab.value, 1, {
                                                         TradeBookColumns.exec_id.value: exec_id[
                                                             OrderBookColumns.exec_id.value]})
            self.trades.compare_values({name_field: expect_res},
                                       {name_field: res['1']}, f"Check fees {name_field}")
