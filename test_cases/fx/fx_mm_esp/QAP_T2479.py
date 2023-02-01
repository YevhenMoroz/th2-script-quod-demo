from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.data_sets.constants import DirectionEnum, Status

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd


class QAP_T2479(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_mm = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.symbol = self.data_set.get_symbol_by_name('symbol_ndf_1')
        self.currency = self.data_set.get_currency_by_name('currency_usd')
        self.settle_type = self.data_set.get_settle_type_by_name("wk1")
        self.settle_date_spo_ndf = self.data_set.get_settle_date_by_name("spo_ndf")
        self.security_type = self.data_set.get_security_type_by_name("fx_ndf")
        self.client = self.data_set.get_client_by_name("client_mm_4")
        self.account = self.data_set.get_account_by_name("account_mm_4")
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportFX()
        self.status_fill = Status.Fill
        self.maturity_date = tsd.custom(5)
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.symbol,
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type,
        }]
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type,
            "Product": "4",
            "MaturityDate": self.maturity_date
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.client).change_parameter(
            'NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_mm.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ['*', '*', '*'])
        self.md_snapshot.get_parameter("Instrument").update({'MaturityDate': self.maturity_date})
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])

        self.new_order_single.set_default().change_parameters(
            {"Account": self.client,
             'Instrument': self.no_related_symbols[0]['Instrument'],
             'OrdType': '1',
             'SettlType': f'{self.settle_type}',
             'Currency': self.currency})

        self.new_order_single.remove_parameters(['Price', 'SettlDate'])
        self.fix_manager_mm.send_message_and_receive_response(self.new_order_single, self.test_id)

        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.status_fill)
        self.execution_report.add_tag({
            'LastMkt': '*',
            'SpotSettlDate': self.settle_date_spo_ndf,
            'Account': self.account,
        })
        self.execution_report.update_fields_in_component('Instrument', {'MaturityDate': self.maturity_date})
        self.execution_report.remove_fields_from_component('Instrument', ['Product'])
        self.execution_report.remove_parameter('Price')

        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # Deleting rule
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_mm.send_message(self.md_request)
