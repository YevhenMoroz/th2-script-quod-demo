from decimal import Decimal
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2461(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote = FixMessageQuoteFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.acc_argentina = self.data_set.get_client_by_name("client_mm_2")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_3")
        self.gbp = self.data_set.get_currency_by_name("currency_eur")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.settle_date_today = self.data_set.get_settle_date_by_name("today")
        self.settle_date_tom = self.data_set.get_settle_date_by_name("tomorrow")
        self.settle_type_today = self.data_set.get_settle_type_by_name("today")
        self.settle_type_tom = self.data_set.get_settle_type_by_name("tomorrow")
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type_swap}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.acc_argentina, Currency=self.gbp,
                                                           Instrument=self.instrument)
        self.quote_request.remove_fields_in_repeating_group("NoRelatedSymbols", ["Side"])
        self.quote_request.update_near_leg(leg_symbol=self.gbp_usd, settle_type=self.settle_type_today,
                                           settle_date=self.settle_date_today)
        self.quote_request.update_far_leg(leg_symbol=self.gbp_usd, settle_type=self.settle_type_tom,
                                          settle_date=self.settle_date_tom)
        response: list = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        # region Calculations
        near_bid_pts = response[0].get_parameter("NoLegs")[0]["LegBidForwardPoints"]
        near_offer_pts = response[0].get_parameter("NoLegs")[0]["LegOfferForwardPoints"]
        far_bid_pts = response[0].get_parameter("NoLegs")[1]["LegBidForwardPoints"]
        far_offer_pts = response[0].get_parameter("NoLegs")[1]["LegOfferForwardPoints"]
        expected_bid_swap = str(round(Decimal.from_float(float(far_offer_pts) - float(near_offer_pts)), 5))
        expected_offer_swap = str(round(Decimal.from_float(float(far_bid_pts) - float(near_bid_pts)), 5))
        if expected_offer_swap == "0.00000":
            expected_offer_swap = "0"
        if expected_bid_swap == "0.00000":
            expected_bid_swap = "0"
        # endregion
        # endregion

        # region Step 2
        self.fix_verifier.check_fix_message(fix_message=self.quote_request)
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.quote.change_parameters({"BidSwapPoints": expected_bid_swap, "OfferSwapPoints": expected_offer_swap})
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        # endregion
