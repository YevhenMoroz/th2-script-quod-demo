from datetime import datetime
from pathlib import Path
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


class QAP_T2380(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.esp_t_connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.fx_fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager = FixManager(self.esp_t_connectivity, self.test_id)
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.esp_t_connectivity, self.test_id)
        self.new_order_singe = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.md_req_id = "EUR/USD:SPO:REG:BNP"
        self.no_md_entries_spot = [{
            "MDEntryType": "0",
            "MDEntryPx": 1.1815,
            "MDEntrySize": 1000000,
            "MDQuoteType": 1,
            "MDEntryPositionNo": 1,
            "SettlDate": spo(),
            "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
            "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
        },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1813,
                "MDEntrySize": 2000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18165,
                "MDEntrySize": 2000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.181,
                "MDEntrySize": 7000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 3,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18186,
                "MDEntrySize": 7000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 3,
                "SettlDate": spo(),
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
        ]
        self.no_strategy_parameters = [{"StrategyParameterName": "AllowedVenues", "StrategyParameterType": "14",
                                        "StrategyParameterValue": "BNP"}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
        # endregion
        # region 2
        self.new_order_singe.set_default_SOR().update_repeating_group("NoStrategyParameters",
                                                                      self.no_strategy_parameters)
        self.new_order_singe.change_parameters({"TimeInForce": "3", "OrderQty": "2800000"})
        response = self.fix_manager.send_message_and_receive_response(self.new_order_singe)
        # endregion
        # region 3
        gateway_side_sell = GatewaySide.Sell
        status = Status.Fill
        self.execution_report.set_params_from_new_order_single(self.new_order_singe, gateway_side_sell, status,
                                                               response[-1])
        self.execution_report.change_parameter("LastQty", "1000000")
        self.fix_verifier.check_fix_message(fix_message=self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
