import logging
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, broken_2, wk3,  broken_w1w2
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

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
settle_type_w3 = "W3"
currency = "EUR"
settle_currency = "GBP"
qty = '1000000'
qty2 = '2000000'
side = "2"
leg1_side = "1"
leg2_side = "2"
defaultmdsymbol_spo = 'EUR/GBP:SPO:REG:CITI'
defaultmdsymbol_wk1 = 'EUR/GBP:FXF:WK1:CITI'
defaultmdsymbol_wk2 = 'EUR/GBP:FXF:WK2:CITI'
price_to_check = '0.0001'
leg_last_px_near = '1.19617'
leg_last_px_far = '1.19627'
last_spot_rate = '1.19597'

no_md_entries_wk1 = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19585,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDEntryForwardPoints": '0.0002',
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19615,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDEntryForwardPoints": '0.0002',
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]

no_md_entries_wk2 = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19485,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDEntryForwardPoints": '0.0003',
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19715,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDEntryForwardPoints": '0.0003',
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]


def send_swap_and_filled(case_id):
    # Precondition
    FixClientSellEsp(
        CaseParamsSellEsp(client, case_id, settltype=settle_type_spo, settldate=settle_date_spo, symbol=symbol,
                          securitytype=security_type_spo, securityid=symbol, currency=currency,
                          settlcurrency=settle_currency)). \
        send_md_request().send_md_unsubscribe()
    FixClientSellEsp(
        CaseParamsSellEsp(client, case_id, settltype=settle_type_spo, settldate=settle_type_w1, symbol=symbol,
                          securitytype=security_type_spo, securityid=symbol, currency=currency,
                          settlcurrency=settle_currency)). \
        send_md_request().send_md_unsubscribe()
    FixClientSellEsp(
        CaseParamsSellEsp(client, case_id, settltype=settle_type_spo, settldate=settle_type_w2, symbol=symbol,
                          securitytype=security_type_spo, securityid=symbol, currency=currency,
                          settlcurrency=settle_currency)). \
        send_md_request().send_md_unsubscribe()
    FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol)).send_market_data_spot()
    FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_wk1, symbol).prepare_custom_md_fwd(
        no_md_entries_wk1)).send_market_data_fwd()
    FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_wk2, symbol).prepare_custom_md_fwd(
        no_md_entries_wk2)).send_market_data_fwd()

    params_swap = CaseParamsSellRfq(client, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                    orderqty=qty2, leg1_ordqty=qty, leg2_ordqty=qty2,
                                    currency=currency, settlcurrency=settle_currency,
                                    leg1_settltype=settle_type_w1, leg2_settltype=settle_type_w2,
                                    settldate=settle_date_spo, leg1_settldate=settle_date_w1,
                                    leg2_settldate=settle_date_w2,
                                    symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                    securitytype=security_type_swap, leg1_securitytype=security_type_fwd,
                                    leg2_securitytype=security_type_fwd,
                                    securityid=symbol, account=account)
    # Step 1
    rfq = FixClientSellRfq(params_swap)
    rfq.send_request_for_quote_swap()
    # Step 2
    rfq.verify_quote_pending_swap(bid_swap_points=price_to_check, bid_px=price_to_check)
    # Step 3
    rfq.send_new_order_multi_leg()
    # Step 4
    rfq.verify_order_pending_swap()
    rfq.verify_order_filled_swap(leg_last_px_near=leg_last_px_near, leg_last_px_far=leg_last_px_far,
                                 spot_rate=last_spot_rate, last_swap_points=price_to_check, avg_px=price_to_check,
                                 last_px=price_to_check)


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
