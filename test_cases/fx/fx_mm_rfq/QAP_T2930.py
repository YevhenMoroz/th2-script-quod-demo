import random
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T2930(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.qty1 = str(random.randint(54000000, 55000000))
        self.qty2 = str(random.randint(54000000, 55000000))
        self.unassigned_result = "DI - Unassigned RFQs window sorting is correct"
        self.assigned_result = "DI - Assigned RFQs window sorting is correct"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           OrderQty=self.qty1, Account=self.account,
                                                           Instrument=self.instrument, Currency=self.currency)
        self.fix_manager_sel.send_message(self.quote_request)
        time.sleep(5)
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           OrderQty=self.qty2, Account=self.account,
                                                           Instrument=self.instrument, Currency=self.currency)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion
        # region step 2
        unassigned_creation_time_1 = time.strftime(self.dealer_intervention.extract_field_from_unassigned
                                                   ("CreationTime", row_number=2))
        unassigned_creation_time_2 = time.strftime(self.dealer_intervention.extract_field_from_unassigned
                                                   ("CreationTime", row_number=3))
        if unassigned_creation_time_1 > unassigned_creation_time_2:
            actual_result = "DI - Unassigned RFQs window sorting is correct"
        else:
            actual_result = "DI - Unassigned RFQs window sorting is incorrect"
        self.dealer_intervention.compare_values(expected_value=self.unassigned_result, actual_value=actual_result,
                                                event_name="Checking sorting Unassigned RFQs window")
        # endregion
        # region step 3
        self.dealer_intervention.assign_quote(row_number=1)
        self.dealer_intervention.assign_quote(row_number=1)

        time.sleep(5)

        assigned_creation_time_1 = time.strftime(self.dealer_intervention.extract_field_from_assigned
                                                 ("CreationTime", row_number=2))
        assigned_creation_time_2 = time.strftime(self.dealer_intervention.extract_field_from_assigned
                                                 ("CreationTime", row_number=3))
        if assigned_creation_time_1 > assigned_creation_time_2:
            actual_result = "DI - Assigned RFQs window sorting is correct"
        else:
            actual_result = "DI - Assigned RFQs window sorting is incorrect"
        self.dealer_intervention.compare_values(expected_value=self.assigned_result, actual_value=actual_result,
                                                event_name="Checking sorting Assigned RFQs window")
        self.dealer_intervention.close_window()
        # endregion
