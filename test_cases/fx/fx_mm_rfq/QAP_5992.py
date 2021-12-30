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
        self.ss_connectivity = SessionAliasFX().ss_rfq_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)

    @decorator_try_except(test_id=Path(__file__).name[:-3])
    def pre_conditions_and_run(self):
        gateway_side_sell = DataSet.GatewaySide.Sell
        status = DataSet.Status.Fill
        account = self.data_set.get_account_by_name("account_1")
        near_leg = {
            "InstrumentLeg": {
                "LegSymbol": "GBP/USD",
                "LegSecurityType": "FXFWD"
            },
            "LegSide": "2",
            "LegSettlType": "1",
            "LegSettlDate": today(),
            "LegOrderQty": "1000000"
        }

        far_leg = {
            "InstrumentLeg": {
                "LegSymbol": "GBP/USD",
                "LegSecurityType": "FXSPOT"
            },
            "LegSide": "1",
            "LegSettlType": "0",
            "LegSettlDate": spo(),
            "LegOrderQty": "1000000"
        }
        instrument = {
            "Symbol": "GBP/USD",
            "SecurityType": "FXSWAP"
        }
        quote_request = FixMessageQuoteRequestFX().set_swap_rfq_params().update_near_leg(near_leg).update_far_leg(
            far_leg)
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
