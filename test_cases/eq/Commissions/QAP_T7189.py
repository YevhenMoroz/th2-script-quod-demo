import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, \
    ExecSts, SecondLevelTabs, TradeBookColumns, Basis
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7189(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '7180'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')  # GBp
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')  # MOClient_EUREX
        self.venue = self.data_set.get_mic_by_name('mic_2')  # XEUR
        self.client = self.data_set.get_client('client_com_1')  #
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        rate = '0.5'
        # region set client_commission precondition
        trade_rule = order_id = None
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.data_set.get_comm_profile_by_name('per_u_qty'))
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create DMA order step 1 and step 2
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            self.fix_message.set_default_dma_limit(instr='instrument_3')
            self.fix_message.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'Currency': self.currency, 'ExDestination': 'XEUR'})
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
            self.rest_commission_sender.clear_commissions()
        # endregion

        # region check expected result from step 2
        filter_list = [OrderBookColumns.order_id.value, order_id]
        dict_of_extraction = {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value}
        expected_result = {OrderBookColumns.exec_sts.value: ExecSts.filled.value}
        message = "Comparing expected and actual result from precondition"
        self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
        # endregion

        # region check step 3
        list_of_column = [OrderBookColumns.currency.value, TradeBookColumns.rate.value, TradeBookColumns.basis.value,
                          TradeBookColumns.amount.value]
        amount = float(rate) * int(self.qty) / 100
        amount = str(round(amount, 1))
        filter_dict = {filter_list[0]: filter_list[1]}
        exec_id = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                      [TradeBookColumns.exec_id.value], [1], filter_dict)[0]
        expected_result = [{'1': self.data_set.get_currency_by_name('currency_2')}, {'1': rate},
                           {'1': Basis.per_unit.value},
                           {'1': amount}]
        self.__compare_values_of_commission(exec_id, expected_result, list_of_column)

        # endregion

    def __check_expected_result_from_order_book(self, filter_list, expected_result, dict_of_extraction, message):
        self.order_book.set_filter(filter_list=filter_list)
        actual_result = self.order_book.extract_fields_list(
            dict_of_extraction)
        self.order_book.compare_values(expected_result, actual_result,
                                       message)

    def __compare_values_of_commission(self, filter_dict, expected_result, list_of_column: list):
        for value in list_of_column:
            actual_result = self.trade_book.extract_sub_lvl_fields(
                [value], SecondLevelTabs.commissions.value, 1, filter_dict)
            print(actual_result)
            self.order_book.compare_values(expected_result[list_of_column.index(value)], actual_result,
                                           f"Comparing {value} after trade")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
