from pathlib import Path

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiModifyMarketMakingStatusMessages import \
    RestApiModifyMarketMakingStatusMessages


class QAP_2872(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.dealer_intervention = None
        self.rest_message = RestApiModifyMarketMakingStatusMessages()
        self.rest_manager = RestApiManager
        self.fix_subscribe = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.ss_connectivity = SessionAliasFX().ss_esp_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.client = self.data_set.get_client_by_name("client_mm_5")
        self.gbp_nok = self.data_set.get_symbol_by_name("symbol_10")
        self.instrument = self.gbp_nok + "-1W"
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.security_type = self.data_set.get_security_type_by_name('fx_fwd')
        self.settltype = self.data_set.get_settle_type_by_name("wk1")
        self.no_related_symbols = [{
            'Instrument': {
                'Symbol': self.gbp_nok,
                'SecurityType': self.security_type,
                'Product': '4'},
            'SettlType': self.settltype}]
        self.instrument = {
            'Symbol': self.gbp_nok,
            'SecurityType': self.security_type,
            'Product': '4'}
        self.status_reject = Status.Reject
        self.bands = ["1000000", '2000000']

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.client}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        # endregion

        # region step 2-3
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands, priced=False)
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

        # region step 4
        self.new_order_single.set_default().change_parameters(
            {"Account": self.client, "Instrument": self.instrument, "Currency": self.currency,
             "SettlType": self.settltype})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)

        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.status_reject)
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe)
