import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, broken_w1w2, broken_2
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from test_cases.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

client = 'Argentina1'
account = 'Argentina1_1'
client_tier = 'Argentina'
symbol = "GBP/USD"
security_type_swap = "FXSWAP"
security_type_fwd = "FXFWD"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_date_broken1 = broken_2()
settle_date_broken2 = broken_w1w2()
settle_type_broken = "B"
settle_type_spo = "0"
currency = "GBP"
settle_currency = "USD"
qty = '5000000'
side = ""
leg1_side = ""
leg2_side = ""
defaultmdsymbol_spo = 'GBP/USD:SPO:REG:CITI'
offer_swap_pts = '0.000015'
bid_swap_pts = '-0.000008'
last_spot_rate = '1.19603'


def send_swap_and_filled(case_id):
    # Precondition
    FixClientSellEsp(
        CaseParamsSellEsp(client, case_id, settltype=settle_type_spo, settldate=settle_date_spo, symbol=symbol,
                          securitytype=security_type_spo, securityid=symbol, currency=currency,
                          settlcurrency=settle_currency)). \
        send_md_request().send_md_unsubscribe()
    FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol)).send_market_data_spot()
    params_swap = CaseParamsSellRfq(client, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                    orderqty=qty, leg1_ordqty=qty, leg2_ordqty=qty,
                                    currency=currency, settlcurrency=settle_currency,
                                    leg1_settltype=settle_type_broken, leg2_settltype=settle_type_broken,
                                    settldate=settle_date_broken1, leg1_settldate=settle_date_broken1,
                                    leg2_settldate=settle_date_broken2,
                                    symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                    securitytype=security_type_swap, leg1_securitytype=security_type_fwd,
                                    leg2_securitytype=security_type_fwd,
                                    securityid=symbol, account=account)
    # Step 1
    rfq = FixClientSellRfq(params_swap)
    rfq.send_request_for_quote_swap()
    # Step 2
    rfq.verify_quote_pending_swap(bid_swap_points=bid_swap_pts, bid_px=bid_swap_pts, offer_swap_points=offer_swap_pts,offer_px=offer_swap_pts)
    # Step 3
    rfq.send_new_order_multi_leg(side='1')
    # Step 4
    rfq.verify_order_pending_swap(side='1')
    rfq.verify_order_filled_swap(side='1', spot_rate=last_spot_rate, last_swap_points=offer_swap_pts,
                                 avg_px=offer_swap_pts,
                                 last_px=offer_swap_pts)


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
