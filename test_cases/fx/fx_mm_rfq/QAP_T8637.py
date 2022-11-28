from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestSynergyFX import FixMessageQuoteRequestSynergyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteSynergyFX import FixMessageQuoteSynergyFX


class QAP_T8637(TestCase):
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
        self.order = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()

        self.instrument = {

                "Symbol": self.data_set.get_symbol_by_name("symbol_1"),
                "SecurityType": self.data_set.get_security_type_by_name("fx_fwd"),
                "Product": "4"
        }

        self.party = [{
            "PartyID": self.client,
            "PartyIDSource": "D",
            "PartyRole": "1"
        }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_synergy_params_fwd()
        self.quote_request.update_value_in_repeating_group("NoRelatedSym", "NoPartyIDs", self.party)
        response: list = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region step 2
        self.quote.set_params_for_quote_fwd(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 3
        self.order.set_default_synergy(self.quote_request, response[0], price="1.18999", side="1")
        self.fix_manager_sel.send_message_and_receive_response(self.order)
        # endregion
        # region Step 4
        self.execution_report.set_params_from_new_order_single_synergy(self.order)
        self.execution_report.add_tag({"SecondaryClOrdID": "*"})
        self.execution_report.update_fields_in_component("Instrument", self.instrument)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
