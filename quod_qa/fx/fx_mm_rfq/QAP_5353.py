
import logging
from datetime import datetime
from pathlib import Path

from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs

client = 'Argentina1'
account = 'Argentina1_1'
client_tier = 'Argentina'
symbol = "EUR/USD"
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
settle_currency = "USD"
qty = '1000000'
side = "1"
leg1_side = "2"
leg2_side = "1"
venue_msr = 'MSR'
mic_msr = 'MS-RFQ'
venue_ms = 'MS'
mic_ms = 'MS-SW'
api = Stubs.api_service
def_md_symbol_eur_usd = "EUR/USD:SPO:REG:MS"
no_md_entries_spo = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.18222,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.18333,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.18220,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.18335,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.18218,
        "MDEntrySize": 3000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.18337,
        "MDEntrySize": 3000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    }
]
avg_px='0.0000399'
last_swap_points='0.0000399'
last_px='0.0000399'


def send_swap_and_filled(case_id):
    # Precondition
    params_eur_usd = CaseParamsSellEsp(client, case_id, settltype=settle_type_spo, settldate=settle_date_spo,
                                       symbol=symbol, securitytype=security_type_spo)
    FixClientSellEsp(params_eur_usd). \
        send_md_request(). \
        send_md_unsubscribe()
    FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_eur_usd, symbol).prepare_custom_md_spot(
        no_md_entries_spo)).send_market_data_spot()
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
    rfq = FixClientSellRfq(params_swap)
    rfq.send_request_for_quote_swap()
    # Step 2
    rfq.verify_quote_pending_swap()
    rfq.send_new_order_multi_leg(ccy1=settle_currency, ccy2=currency)
    rfq.verify_order_pending_swap(ccy1=settle_currency, ccy2=currency)
    rfq.verify_order_filled_swap(ccy1=settle_currency, ccy2=currency, avg_px=avg_px, last_px=last_px,last_swap_points=last_swap_points)


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
