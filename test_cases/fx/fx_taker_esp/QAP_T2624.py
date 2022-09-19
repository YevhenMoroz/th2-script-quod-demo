from datetime import datetime
from pathlib import Path
from test_framework.data_sets.constants import GatewaySide, Status
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportTakerMO import FixMessageExecutionReportTakerMO
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker


class QAP_T2624(TestCase):
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
        self.new_order_single = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.execution_report_mo_1 = FixMessageExecutionReportTakerMO()
        self.execution_report_mo_2 = FixMessageExecutionReportTakerMO()
        self.status = Status.Fill
        self.acc_argentina = self.data_set.get_client_by_name("client_mm_3")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur = self.data_set.get_currency_by_name("currency_eur")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.md_req_id_hsbc = 'EUR/USD:SPO:REG:HSBC'
        self.no_md_entries_spot_hsbc = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19568,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19679,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18507,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19628,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18400,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19632,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
        self.no_strategy_parameters = [{'StrategyParameterName': 'AllowedVenues', 'StrategyParameterType': '14',
                                        'StrategyParameterValue': 'HSBC'}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot_hsbc)
        self.fix_md.update_MDReqID(self.md_req_id_hsbc, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
        # endregion
        # region 2
        self.new_order_single.set_default_SOR().update_repeating_group("NoStrategyParameters",
                                                                       self.no_strategy_parameters)
        self.new_order_single.change_parameters({"TimeInForce": "3", "OrderQty": "2800000"})
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        # endregion
        # region 3
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.execution_report.change_parameter("LastQty", "2800000")
        self.fix_verifier.check_fix_message(fix_message=self.execution_report)
        # endregion

    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id_hsbc, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)