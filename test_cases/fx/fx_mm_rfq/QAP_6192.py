from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_6192(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side_rfq
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.status = Status.Fill
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.new_order_single = FixMessageNewOrderMultiLegFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_wk2 = self.data_set.get_settle_type_by_name("wk2")
        self.settle_type_wk1 = self.data_set.get_settle_type_by_name("wk1")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.settle_date_wk2 = self.data_set.get_settle_date_by_name("wk2")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_symbol=self.symbol, leg_sec_type=self.security_type_fwd,
                                           settle_type=self.settle_type_wk1,
                                           settle_date=self.settle_date_wk1)
        self.quote_request.update_far_leg(leg_symbol=self.symbol, settle_type=self.settle_type_wk2,
                                          leg_sec_type=self.security_type_fwd,
                                          settle_date=self.settle_date_wk2)
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0].pop('LegSettlDate')
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1].pop('LegSettlDate')
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 2
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0].update(
            {'LegSettlDate': self.settle_date_wk1})
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1].update(
            {'LegSettlDate': self.settle_date_wk2})
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion
