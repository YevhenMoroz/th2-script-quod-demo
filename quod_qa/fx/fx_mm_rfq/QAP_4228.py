import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, broken_2, wk3, broken_w1w2
from quod_qa.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from win_gui_modules.wrappers import set_base




def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "CLIENT123"

    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date_spo = spo()
    settle_type_spo = "0"
    currency = "GBP"

    side = "1"

    qty_1 = random_qty(1, 3, 7)
    try:
        params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo,
                                        currency=currency, side=side,
                                        account=client_tier)
        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_reject(text=f"11620 unknown client {client_tier}")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
