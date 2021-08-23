import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from pathlib import Path

from custom.tenor_settlement_date import spo, wk1, wk2
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "Silver1"
    symbol = "EUR/USD"
    security_type_swap = "FXSWAP"
    security_type_fwd = "FXFWD"
    security_type_spo = "FXSPOT"
    settle_date_w1 = wk1()
    settle_date_w2 = wk2()
    settle_type_w1 = "W1"
    settle_type_w2 = "W2"
    currency = "EUR"
    settle_currency = "USD"
    default_md_symbol_spo = 'EUR/USD:SPO:REG:HSBC'

    mdu_params_spo = [
        {
            "MDEntryType": "0",
            "MDEntryPx": 1.19585,
            "MDEntrySize": 1000000,
            "MDEntryPositionNo": 1,
            'SettlDate': spo(),
            "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        },
        {
            "MDEntryType": "1",
            "MDEntryPx": 1.19612,
            "MDEntrySize": 1000000,
            "MDEntryPositionNo": 1,
            'SettlDate': spo(),
            "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        },
        {
            "MDEntryType": "0",
            "MDEntryPx": 1.19584,
            "MDEntrySize": 6000000,
            "MDEntryPositionNo": 2,
            'SettlDate': spo(),
            "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        },
        {
            "MDEntryType": "1",
            "MDEntryPx": 1.19615,
            "MDEntrySize": 6000000,
            "MDEntryPositionNo": 2,
            'SettlDate': spo(),
            "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        },
        {
            "MDEntryType": "0",
            "MDEntryPx": 1.19581,
            "MDEntrySize": 12000000,
            "MDEntryPositionNo": 3,
            'SettlDate': spo(),
            "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        },
        {
            "MDEntryType": "1",
            "MDEntryPx": 1.19620,
            "MDEntrySize": 12000000,
            "MDEntryPositionNo": 3,
            'SettlDate': spo(),
            "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        },
    ]

    try:
        # Send custom MarketData
        FixClientBuy(CaseParamsBuy(case_id, default_md_symbol_spo, symbol, security_type_spo).
                     prepare_custom_md_spot(mdu_params_spo)).send_market_data_spot()

        params_swap = CaseParamsSellRfq(client_tier, case_id, side="", leg1_side="1", leg2_side="2",
                                        orderqty="1000000", leg1_ordqty="1000000", leg2_ordqty="1000000",
                                        currency=currency, settlcurrency=settle_currency,
                                        leg1_settltype=settle_type_w1, leg2_settltype=settle_type_w2,
                                        settldate=settle_date_w1, leg1_settldate=settle_date_w1,
                                        leg2_settldate=settle_date_w2,
                                        symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                        securitytype=security_type_swap, leg1_securitytype=security_type_fwd,
                                        leg2_securitytype=security_type_fwd,
                                        securityid=symbol)
        # Send RFQ
        rfq = FixClientSellRfq(params_swap)
        rfq.send_request_for_quote_swap()
        bid_price = float(mdu_params_spo[0]["MDEntryPx"])
        offer_price = float(mdu_params_spo[1]["MDEntryPx"])
        mid_price = str(round((bid_price + offer_price) / 2, 5))
        rfq.verify_quote_pending_swap(bid_spot_rate=mid_price, offer_spot_rate=mid_price)

    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
