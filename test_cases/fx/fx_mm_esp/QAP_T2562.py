from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import Status, DirectionEnum, GatewaySide
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX


class QAP_T2562(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        # self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_esp
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_esp
        self.gateway_side_sell = GatewaySide.Sell
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.account = self.data_set.get_client_by_name("client_mm_4")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.wrong_settldate = self.data_set.get_settle_date_by_name("tomorrow")
        self.security_type = self.data_set.get_security_type_by_name('fx_spot')
        self.text = "11697 No listing found for order with currency EUR on exchange QUODFX"
        self.no_related_symbols = [{
            'Instrument': {
                'Symbol': self.eur_usd,
                'SecurityType': self.security_type,
                'Product': '4', },
            'SettlType': '0', }]
        self.bands_eur_usd = ["2000000", '6000000', '12000000']
        self.status_reject = Status.Reject

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameters({"SenderSubID": self.account}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

        # region step 2
        self.new_order_single.set_default().change_parameters({"Account": self.account,
                                                               "SettlDate": self.wrong_settldate})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single,
                                                               self.status_reject,
                                                               response=response[-1]).add_tag(
            {'OrdRejReason': '99', "TargetStrategy": "*", "StrategyName": "*"})
        self.execution_report.change_parameter("HandlInst", "*")
        self.execution_report.remove_parameters(
            ["SettlCurrency", "LastMkt", "ExecRestatementReason", "SettlType"])
        self.execution_report.remove_fields_from_component("Instrument", ["SecurityIDSource", "SecurityID"])
        self.execution_report.change_parameter("Text", self.text)
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
