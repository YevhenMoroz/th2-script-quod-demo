from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_3761(TestCase):

    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_rfq_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        status = Status.Fill
        account = self.data_set.get_client_by_name("client_mm_2")
        currency = self.data_set.get_currency_by_name("currency_gbp")
        symbol = self.data_set.get_symbol_by_name("symbol_2")
        security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        settle_type_wk3 = self.data_set.get_settle_type_by_name("wk3")
        settle_date_wk3 = self.data_set.get_settle_date_by_name("wk3")
        instrument = {
            "Symbol": symbol,
            "SecurityType": security_type_fwd
        }

        quote_request = FixMessageQuoteRequestFX(data_set=self.data_set).set_rfq_params_fwd()
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                      Currency=currency, Instrument=instrument,
                                                      SettlDate=settle_date_wk3, SettlType=settle_type_wk3)

        response: list = self.fix_manager_gtw.send_message_and_receive_response(quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote_fwd(quote_request)

        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_prev_quoted(quote_request, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_single(new_order_single,
                                                                                                    status)

        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)
