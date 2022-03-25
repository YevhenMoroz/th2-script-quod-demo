import logging
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, broken_2, wk3,  broken_w1w2
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from test_cases.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook

client = 'Argentina1'
account = 'Argentina1_1'
client_tier = 'Argentina'
symbol = "EUR/GBP"
security_type_swap = "FXSWAP"
security_type_fwd = "FXFWD"
security_type_spo = "FXSPO"
settle_date_spo = spo()
settle_date_w1 = wk1()
settle_date_w2 = wk2()
settle_type_spo = "0"
settle_type_w1 = "W1"
settle_type_w2 = "W2"
currency = "EUR"
settle_currency = "GBP"
qty = '1000000'
side = "1"
leg1_side = "2"
leg2_side = "1"



def send_swap_and_filled(case_id):
    params_swap = CaseParamsSellRfq(client, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                    orderqty=qty, leg1_ordqty=qty, leg2_ordqty=qty,
                                    currency=currency, settlcurrency=settle_currency,
                                    leg1_settltype=settle_type_w1, leg2_settltype=settle_type_w2,
                                    settldate=settle_date_spo, leg1_settldate=settle_date_w1,
                                    leg2_settldate=settle_date_w2,
                                    symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                    securitytype=security_type_swap, leg1_securitytype=security_type_fwd,
                                    leg2_securitytype=security_type_fwd,
                                    securityid=symbol, account=account)
    # Step 1
    rfq = FixClientSellRfq(params_swap)\
        .send_request_for_quote_swap()
    #Step 2



def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)


from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except

qty = '1000000'

class QAP_3721(TestCase):
    def __init__(self,report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        client = self.data_set.get_client_by_name('client_mm_2')
        account = self.data_set.get_account_by_name('account_mm_2')
        eur = self.data_set.get_currency_by_name('currency_eur')
        gbp = self.data_set.get_currency_by_name('currency_gbp')
        eur_gbp = self.data_set.get_symbol_by_name('symbol_3')
        sttl_date_wk1 = self.data_set.get_settle_date_by_name('wk1')
        sttl_date_wk2 = self.data_set.get_settle_date_by_name('wk2')
        sttl_t_spo = self.data_set.get_settle_type_by_name('spot')
        sttl_t_wk1 = self.data_set.get_settle_type_by_name('wk1')
        sec_t_swap = self.data_set.get_security_type_by_name('fx_swap')
        sec_t_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        sec_t_spo = self.data_set.get_security_type_by_name('fx_spot')
        side = self.data_set.get_side_by_name('buy')
        leg1_side = self.data_set.get_side_by_name('sell')
        leg2_side = self.data_set.get_side_by_name('buy')

        # region Step 1
        # endregion

        # region Step 2
        # endregion

        # region Step 3
        # endregion

        # region Step 4
        # endregion