import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets import constants
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.position_calculation_manager import PositionCalculationManager
from test_framework.win_gui_wrappers.fe_trading_constant import PositionBookColumns, QuoteRequestBookColumns, Status
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention
from test_framework.win_gui_wrappers.forex.fx_positions import FXPositions


class QAP_T2677(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.dealing_poss = FXPositions(self.test_id, self.session_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.poss_manager = PositionCalculationManager
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        # region Test data
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.instrument_fwd = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }
        self.qty = random_qty(1, 2, 7)
        self.qty_to_dealer = random_qty(3, 5, 8)
        self.status = constants.Status.Fill
        self.symbol_col = PositionBookColumns.symbol.value
        self.account_col = PositionBookColumns.account.value
        self.position_col = PositionBookColumns.position.value
        self.qty_column = QuoteRequestBookColumns.qty.value
        self.sts_column = QuoteRequestBookColumns.status.value
        self.cur_column = QuoteRequestBookColumns.currency.value
        self.sts_new = Status.new.value
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Creation position to compare
        self.quote_request.set_rfq_params_fwd().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                                Account=self.client,
                                                                                Currency=self.currency,
                                                                                Instrument=self.instrument_fwd,
                                                                                OrderQty=self.qty, Side="2")
        response: list = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote_fwd(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single,
                                                               self.status)
        self.fix_verifier.check_fix_message(self.execution_report, direction=DirectionEnum.FromQuod)
        position_before = self.dealing_poss.set_filter(
            [self.account_col, self.client, self.symbol_col, self.symbol]).extract_field(self.position_col)
        # endregion
        # region Step 1
        self.quote_request.set_rfq_params_fwd().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                                Account=self.client,
                                                                                Currency=self.currency,
                                                                                Instrument=self.instrument_fwd,
                                                                                OrderQty=self.qty_to_dealer)
        response = self.fix_manager.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_dealer(self.quote_request)
        # endregion
        # region Step 2
        self.dealer_intervention.set_list_filter(
            [self.qty_column, self.qty_to_dealer, self.cur_column, self.currency]).check_unassigned_fields(
            {self.sts_column: self.sts_new})
        self.dealer_intervention.assign_quote()
        self.dealer_intervention.estimate_quote()
        # endregion
        # region Step 3
        time.sleep(5)
        self.dealer_intervention.send_quote()
        time.sleep(2)
        self.dealer_intervention.close_window()
        quote_response = next(response)
        quote_from_di = self.fix_manager.parse_response(quote_response)[0]
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        # endregion
        # region Step 4
        self.new_order_single.set_default_for_dealer(self.quote_request, quote_from_di)
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single,
                                                               self.status)
        self.fix_verifier.check_fix_message(self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion
        # region Step 5
        position_after = self.dealing_poss.set_filter(
            [self.account_col, self.client, self.symbol_col, self.symbol]).extract_field(self.position_col)

        expected_pos = self.poss_manager.calculate_position_buy(position_before, self.qty_to_dealer)
        self.dealer_intervention.compare_values(expected_pos, position_after.replace(",", ""),
                                                event_name="Check position after buy order")

        # end region
