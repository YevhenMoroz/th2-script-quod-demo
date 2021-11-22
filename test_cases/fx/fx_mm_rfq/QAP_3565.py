import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    qty_1 = random_qty(1, 3, 7)
    client_tier = "Iridium1"
    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_type_spo = "0"
    currency = "GBP"

    side = "1"
    try:
        params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                        securitytype=security_type_spo,
                                        settltype=settle_type_spo,
                                        currency=currency, side=side,
                                        account=client_tier)

        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
