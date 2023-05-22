from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegSynergyFX import FixMessageNewOrderMultiLegSynergyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestSynergyFX import FixMessageQuoteRequestSynergyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteSynergyFX import FixMessageQuoteSynergyFX


class QAP_T8025(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_cnx
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestSynergyFX(data_set=self.data_set)
        self.quote = FixMessageQuoteSynergyFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.order = FixMessageNewOrderMultiLegSynergyFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.verifier = Verifier(self.test_id)
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur = self.data_set.get_currency_by_name("currency_eur")
        self.usd = self.data_set.get_currency_by_name("currency_usd")
        self.eur_leg = {"LegSymbol": self.eur_usd,
                        "LegSymbolSfx": self.eur_usd,
                        "LegCurrency": self.eur,
                        "LegSide": "1"}
        self.usd_leg = {"LegSymbol": self.eur_usd,
                        "LegSymbolSfx": self.eur_usd,
                        "LegCurrency": self.usd,
                        "LegSide": "1"}
        self.party = [{
            "PartyID": self.client,
            "PartyIDSource": "D",
            "PartyRole": "1"
        }]
        self.expected_text = "11733 Given currency (GBP) is neither base (EUR) nor quote (USD)"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_synergy_params_multileg()
        self.quote_request.update_value_in_repeating_group("NoRelatedSym", "NoPartyIDs", self.party)
        # self.quote_request.add_tag({"VenueType": "M"})
        self.quote_request.get_parameters()["NoRelatedSym"][0]["NoLegs"][0].update(
            {"InstrumentLeg": self.eur_leg})
        self.quote_request.get_parameters()["NoRelatedSym"][0]["NoLegs"][1].update(
            {"InstrumentLeg": self.usd_leg})
        quote = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)[0]
        # endregion
        # region Step 2
        self.actual_text = quote.get_parameters()['Text']
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check FreeNotes (QuoteFIX message)")
        self.verifier.compare_values("FreeNotes", self.expected_text, self.actual_text)
        self.verifier.verify()
        # endregion
