from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, TriggerType, OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_order_ticket import FXOrderTicket
from test_framework.win_gui_wrappers.forex.rates_tile import RatesTile


class QAP_T2609(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.new_order_sor = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.buy_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.buy_side_esp, self.test_id)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshBuyFX()

        self.symbol = self.data_set.get_symbol_by_name("symbol_8")
        self.tenor_spot = self.data_set.get_tenor_by_name("tenor_spot")
        self.client = self.data_set.get_client_by_name("client_1")
        self.account = self.data_set.get_client_by_name("client_1")
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.md_symbol = self.symbol + ":SPO:REG:" + self.venue
        self.nostratparams = [{
            'StrategyParameterName': 'AllowedVenues',
            'StrategyParameterType': '14',
            'StrategyParameterValue': 'CITI'
        }]
        self.qty = random_qty(4, 5, 7)
        self.higher_than_ask = "1.18151"
        self.lower_than_ask = "1.18149"
        self.lower_than_bid = "1.18149"
        self.higher_than_bid = "1.18151"


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send MD
        self.md_snapshot.set_market_data()
        self.md_snapshot.update_MDReqID(self.md_symbol, self.fix_env.feed_handler, "FX")
        self.fix_manager.send_message(self.md_snapshot, "Send MD to USD/SEK")
        self.sleep(5)
        # endregion
        # region Step 1
        self.new_order_sor.set_default_SOR().change_parameters({"Price": self.higher_than_ask})
        self.new_order_sor.add_tag({"StopPx": self.lower_than_ask})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_sor)
        # endregion
        # region Step 2-3
        self.execution_report.set_params_from_new_order_single(self.new_order_sor)
        self.execution_report.remove_parameters(["OrderCapacity"])
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName", "trailer", "header",
                                                            "OrderCapacity"])
        # endregion

        # region Step 1
        self.new_order_sor.set_default_SOR().change_parameters({"Price": self.higher_than_ask})
        self.new_order_sor.add_tag({"StopPx": self.higher_than_ask})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_sor)
        # endregion
        # region Step 2-3
        self.execution_report.set_params_from_new_order_single(self.new_order_sor, status=Status.New)
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName", "trailer", "header",
                                                            "OrderCapacity"])
        # endregion

        # region Step 1
        self.new_order_sor.set_default_SOR().change_parameters({"Price": self.lower_than_bid, "Side": "2"})
        self.new_order_sor.add_tag({"StopPx": self.higher_than_bid})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_sor)
        # endregion
        # region Step 2-3
        self.execution_report.set_params_from_new_order_single(self.new_order_sor)
        self.execution_report.remove_parameters(["OrderCapacity"])
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName", "trailer", "header",
                                                            "OrderCapacity"])
        # endregion

        # region Step 1
        self.new_order_sor.set_default_SOR().change_parameters({"Price": self.lower_than_bid, "Side": "2"})
        self.new_order_sor.add_tag({"StopPx": self.lower_than_bid})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_sor)
        # endregion
        # region Step 2-3
        self.execution_report.set_params_from_new_order_single(self.new_order_sor, status=Status.New)
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName", "trailer", "header",
                                                            "OrderCapacity"])
        # endregion
