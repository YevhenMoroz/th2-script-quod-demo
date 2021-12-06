import logging
from pathlib import Path

from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from test_cases.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs

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
    quote_req_id = bca.client_orderid(8)
    params = {
        'QuoteReqID': quote_req_id,
        'NoRelatedSym': [{
            'Account': "CLIENT1",
            'Instrument': {
                'Symbol': "EUR/USD",
                'SecurityType': "FXSPOT"
            },
            'SettlDate': spo(),
            'SettlType': 0,
            'Currency': "EUR",
            'QuoteType': '1',
            'OrderQty': "1000000",
            'OrdType': 'D'
        }
        ]
    }
    # act = Stubs.fix_act
    # response = act.placeQuoteFIX(
    #     request=bca.convert_to_request(
    #         "SendEarlyRedemption",
    #         "fix-sell-esp-m-314-cnx",
    #         case_id,
    #         bca.message_to_grpc("QuoteRequest", params, "fix-sell-esp-m-314-cnx")
    #     )
    # )

    act = Stubs.fix_act
    response = act.placeQuoteFIX(
        request=bca.convert_to_request(
            "SendEarlyRedemption",
            "fix-sell-esp-m-314-cnx",
            case_id,
            bca.message_to_grpc("QuoteRequest", params, "fix-sell-esp-m-314-cnx")
        )
    )

def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)


