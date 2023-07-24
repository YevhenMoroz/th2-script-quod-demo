from datetime import datetime
from pathlib import Path

from test_cases.fx.fx_wrapper.common_tools import check_value_in_db
from test_framework.data_sets.constants import GatewaySide, Status
from custom.tenor_settlement_date import spo
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker


class QAP_T2489(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.esp_t_connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.fx_fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager = FixManager(self.esp_t_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.esp_t_connectivity, self.test_id)
        self.new_order_singe = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.no_strategy_parameters = [{"StrategyParameterName": "AllowedVenues", "StrategyParameterType": "14",
                                        "StrategyParameterValue": "CITI/BARX/HSBC"}]
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur = self.data_set.get_currency_by_name("currency_eur")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.md_req_id_barx = 'EUR/USD:SPO:REG:BARX'
        self.md_req_id_citi = 'EUR/USD:SPO:REG:CITI'
        self.md_req_id_hsbc = 'EUR/USD:SPO:REG:HSBC'
        self.no_md_entries_spot_barx = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18066,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18146,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            }
        ]
        self.no_md_entries_spot_citi = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18075,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18141,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            }
        ]
        self.no_md_entries_spot_hsbc = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18079,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.1814,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            }
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot_barx)
        self.fix_md.update_MDReqID(self.md_req_id_barx, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)

        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot_citi)
        self.fix_md.update_MDReqID(self.md_req_id_citi, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)

        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot_hsbc)
        self.fix_md.update_MDReqID(self.md_req_id_hsbc, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
        # region 2
        self.new_order_singe.set_default_SOR().update_repeating_group("NoStrategyParameters",
                                                                      self.no_strategy_parameters)
        response = self.fix_manager.send_message_and_receive_response(self.new_order_singe)
        order_id = response[0].get_parameters()["OrderID"]
        venue = check_value_in_db(extracting_value="destinationvenueid",
                                     query=f"SELECT destinationvenueid FROM ordr "
                                           f"WHERE sorparentordid = '{order_id}'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check Venues of Child Orders")
        self.verifier.compare_values("Venue when price is 1.18999", "HSBC", venue)
        # endregion
        # region 3
        self.execution_report.set_params_from_new_order_single(self.new_order_singe, response=response[-1])
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName", "trailer",
                                                            "header"])
        # endregion
        self.new_order_singe.set_default_SOR().update_repeating_group("NoStrategyParameters",
                                                                      self.no_strategy_parameters)
        self.new_order_singe.change_parameters({"Price": "1.18"})
        response = self.fix_manager.send_message_and_receive_response(self.new_order_singe)
        order_id = response[0].get_parameters()["OrderID"]
        venue = check_value_in_db(extracting_value="destinationvenueid",
                                     query=f"SELECT destinationvenueid FROM ordr "
                                           f"WHERE sorparentordid = '{order_id}'")
        self.verifier.compare_values("Venue when price is 1.18", "HSBC", venue)
        self.verifier.verify()
        self.execution_report.set_params_from_new_order_single(self.new_order_singe, response=response[-1])
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["GatingRuleCondName", "GatingRuleName", "trailer",
                                                            "header"])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id_barx, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id_citi, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id_hsbc, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
