from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2596(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.account = self.data_set.get_client_by_name("client_mm_2")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_wk3 = self.data_set.get_settle_type_by_name("broken")
        self.settle_date_wk3 = self.data_set.get_settle_date_by_name("broken_w1w2")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           SettlDate=self.settle_date_wk3,
                                                           SettlType=self.settle_type_wk3)

        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_fwd(self.quote_request)

        self.fix_verifier.check_fix_message(self.quote)
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_prev_quoted(self.quote_request,
                                                                                          response[0])
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_single(new_order_single)

        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)
