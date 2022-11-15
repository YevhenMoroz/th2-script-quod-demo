from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2842(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.verifier = Verifier(self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.iridium1 = self.data_set.get_client_by_name("client_mm_3")
        self.settle_date_wk2 = self.data_set.get_settle_date_by_name("wk2")
        self.settle_date_broken = self.data_set.get_settle_date_by_name("wk3")
        self.settle_type_broken = self.data_set.get_settle_type_by_name("wk3")
        self.settle_type_wk2 = self.data_set.get_settle_type_by_name("wk2")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type_fwd
        }
        self.validator = "ok"
        self.validation = "is broken bigger then wk2?"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_rfq_params_fwd()

        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Account=self.iridium1,
                                                           Currency=self.gbp, Instrument=self.instrument,
                                                           SettlDate=self.settle_date_wk2,
                                                           SettlType=self.settle_type_wk2)
        response: list = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)

        wk2_offer_px = response[0].get_parameter('OfferPx')

        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Account=self.iridium1,
                                                           Currency=self.gbp, Instrument=self.instrument,
                                                           SettlDate=self.settle_date_broken,
                                                           SettlType=self.settle_type_broken)
        response: list = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        broken_offer_px = response[0].get_parameter('OfferPx')
        if float(broken_offer_px) > float(wk2_offer_px):
            result = "ok"
        else:
            result = "test_failed"
        self.verifier.set_event_name(self.validation)
        self.verifier.compare_values(self.validation, self.validator, result)
        self.verifier.verify()

        self.quote.set_params_for_quote_fwd(quote_request=self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        # endregion
