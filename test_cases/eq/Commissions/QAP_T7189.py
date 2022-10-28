import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
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
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set client_commission precondition
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message()
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
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        exec_reply = response[2].get_parameters()
        expected_result = {"CommissionType": "3", "Commission": "0.01"}
        self.java_api_manager.compare_values(expected_result, exec_reply["CommissionData"],
                                             "CommissionData")
