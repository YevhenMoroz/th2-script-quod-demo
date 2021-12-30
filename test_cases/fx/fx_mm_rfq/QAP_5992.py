import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo, today
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.base_window import decorator_try_except

connectivityRFQ = 'fix-ss-rfq-314-luna-standard'
fix_act = Stubs.fix_act


class QAP_5992(TestCase):

    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_rfq_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)

    @decorator_try_except(test_id=Path(__file__).name[:-3])
    def pre_conditions_and_run(self):
        gateway_side_sell = DataSet.GatewaySide.Sell
        status = DataSet.Status.Fill
        account = self.data_set.get_account_by_name("account_1")
        instrument = {
            "Symbol": "GBP/USD",
            "SecurityType": "FXSWAP"
        }
        sec_type_spo = "FXSPOT"
        sec_type_fwd = "FXFWD"
        leg_symbol = "GBP/USD"
        settle_date_tod = today()
        settle_type_tod = "1"
        settle_date_spo = spo()
        settle_type_spo = "0"

        quote_request = FixMessageQuoteRequestFX().set_swap_rfq_params()
        quote_request.update_near_leg(leg_symbol=leg_symbol, leg_sec_type=sec_type_fwd, settle_type=settle_type_tod,
                                      settle_date=settle_date_tod)
        quote_request.update_far_leg(leg_symbol=leg_symbol, settle_type=settle_type_spo, leg_sec_type=sec_type_spo,
                                     settle_date=settle_date_spo)
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                      Currency="GBP", Instrument=instrument)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote_swap(quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        new_order_single = FixMessageNewOrderMultiLegFX().set_default_prev_quoted_swap(quote_request, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_swap(new_order_single,
                                                                                                  gateway_side_sell,
                                                                                                  status)
        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)

    @decorator_try_except(test_id=Path(__file__).name[:-3])
    def post_conditions(self):
        pass
