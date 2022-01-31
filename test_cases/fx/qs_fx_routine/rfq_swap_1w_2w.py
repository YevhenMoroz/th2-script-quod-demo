import logging
from pathlib import Path

from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, tom
from stubs import Stubs
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

client = 'CLIENT1'
symbol = "USD/OMR"
security_type_swap = "FXSWAP"
security_type_fwd = "FXFWD"
security_type_spo = "FXSPO"
settle_date_spo = spo()
settle_date_w1 = wk1()
settle_date_w2 = wk2()
settle_date_tom = tom()
settle_type_spo = "0"
settle_type_w1 = "W1"

settle_type_w2 = "W2"
settle_type_tom = "2"
currency = "USD"
settle_currency = "OMR"
qty = '1000000'
side = "1"
leg1_side = "2"
leg2_side = "1"




def send_swap_and_filled(case_id):
    params_swap = CaseParamsSellRfq(client, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                    orderqty=qty, leg1_ordqty=qty, leg2_ordqty=qty,
                                    currency=currency, settlcurrency=settle_currency,
                                    leg1_settltype=settle_type_spo, leg2_settltype=settle_type_tom,
                                    settldate=settle_date_spo, leg1_settldate=settle_date_spo,
                                    leg2_settldate=settle_date_tom,
                                    symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                    securitytype=security_type_swap, leg1_securitytype=security_type_spo,
                                    leg2_securitytype=security_type_fwd,
                                    securityid=symbol)

    rfq = FixClientSellRfq(params_swap)
    rfq.send_request_for_quote_swap()
    # rfq.send_new_order_multi_leg()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)


