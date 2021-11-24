from custom.tenor_settlement_date import spo
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from pathlib import Path
from custom import basic_custom_actions as bca

security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"

def order_sell(client, case_id, symbol, settle_currency, currency, account):
    params_spot = CaseParamsSellRfq(client, case_id, orderqty='1000000', symbol=symbol,
                                    securitytype=security_type_spo, settldate=settle_date_spo,
                                    settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                    currency=currency, side='1',
                                    account=account)
    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price=price). \
        verify_order_pending(). \
        verify_order_filled()

def order_buy(client, case_id, symbol, settle_currency, currency, account):
    params_spot = CaseParamsSellRfq(client, case_id, orderqty='1000000', symbol=symbol,
                                    securitytype=security_type_spo, settldate=settle_date_spo,
                                    settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                    currency=currency, side='2',
                                    account=account)
    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("BidPx")
    rfq.send_new_order_single(price=price). \
        verify_order_pending(). \
        verify_order_filled()

def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    order_buy('AURUM1', case_id, "USD/SEK", "SEK", "USD", "AURUM1_1")
    order_sell('AURUM1', case_id, "USD/SEK", "SEK", "USD", "AURUM1_1")

    order_buy('AURUM1', case_id, "NOK/SEK", "SEK", "NOK", "AURUM1_1")
    order_sell('AURUM1', case_id, "NOK/SEK", "SEK", "NOK", "AURUM1_1")

    order_buy('AURUM1', case_id, "EUR/USD", "USD", "EUR", "AURUM1_1")
    order_sell('AURUM1', case_id, "EUR/USD", "USD", "EUR", "AURUM1_1")

    order_buy('AURUM1', case_id, "EUR/NOK", "NOK", "EUR", "AURUM1_1")
    order_sell('AURUM1', case_id, "EUR/NOK", "NOK", "EUR", "AURUM1_1")

    order_buy('AURUM1', case_id, "USD/DKK", "DKK", "USD", "AURUM1_1")
    order_sell('AURUM1', case_id, "USD/DKK", "DKK", "USD", "AURUM1_1")

    order_buy('AURUM1', case_id, "USD/ZAR", "ZAR", "USD", "AURUM1_1")
    order_sell('AURUM1', case_id, "USD/ZAR", "ZAR", "USD", "AURUM1_1")

    order_buy('AURUM1', case_id, "EUR/CHF", "CHF", "EUR", "AURUM1_1")
    order_sell('AURUM1', case_id, "EUR/CHF", "CHF", "EUR", "AURUM1_1")

    order_buy('AURUM1', case_id, "CHF/THB", "THB", "CHF", "AURUM1_1")
    order_sell('AURUM1', case_id, "CHF/THB", "THB", "CHF", "AURUM1_1")

    order_buy('AURUM1', case_id, "GBP/DKK", "DKK", "GBP", "AURUM1_1")
    order_sell('AURUM1', case_id, "GBP/DKK", "DKK", "GBP", "AURUM1_1")

    order_buy('Osmium1', case_id, "EUR/USD", "USD", "EUR", "Osmium1_1")
    order_sell('Osmium1', case_id, "EUR/USD", "USD", "EUR", "Osmium1_1")
