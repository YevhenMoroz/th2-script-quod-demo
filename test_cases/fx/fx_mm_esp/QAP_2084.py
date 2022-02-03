import time
from pathlib import Path

from custom.tenor_settlement_date import wk1
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet, DirectionEnum, Status
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiModifyMarketMakingStatusMessages import \
    RestApiModifyMarketMakingStatusMessages


class QAP_2084(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.dealer_intervention = None
        self.ss_connectivity = SessionAliasFX().ss_esp_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX()
        self.new_order_single = FixMessageNewOrderSingleFX()
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.account = self.data_set.get_client_by_name("client_mm_4")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date = self.data_set.get_settle_date_by_name("spot")
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.status_reject = Status.Reject
        self.qty = "58000000"
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type,
            'Product': '4'}
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type}]


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)

        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "MDTime"])
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

        # region step 2
        self.new_order_single.set_default().change_parameters(
            {"Account": self.account, "OrderQty": self.qty})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        # endregion

        # region step 3-5
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.status_reject)
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
