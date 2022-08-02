from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2475(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        status = Status.Fill
        account = self.data_set.get_client_by_name("client_mm_2")
        symbol = self.data_set.get_symbol_by_name("symbol_2")
        security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        settle_type_today = self.data_set.get_settle_type_by_name("today")
        settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        settle_date_spo = self.data_set.get_settle_date_by_name("spot")
        settle_date_tod = self.data_set.get_settle_date_by_name("today")
        instrument = {
            "Symbol": symbol,
            "SecurityType": security_type_swap
        }
        quote_request = FixMessageQuoteRequestFX(data_set=self.data_set).set_swap_rfq_params()
        quote_request.update_near_leg(leg_symbol=symbol, leg_sec_type=security_type_fwd, settle_type=settle_type_today,
                                      settle_date=settle_date_tod)
        quote_request.update_far_leg(leg_symbol=symbol, settle_type=settle_type_spot, leg_sec_type=security_type_spot,
                                     settle_date=settle_date_spo)
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                      Currency="GBP", Instrument=instrument)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote_swap(quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        new_order_single = FixMessageNewOrderMultiLegFX().set_default_prev_quoted_swap(quote_request, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_swap(new_order_single,
                                                                                                  status)
        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)
