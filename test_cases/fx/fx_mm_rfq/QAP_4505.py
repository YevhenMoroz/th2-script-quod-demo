import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from custom.tenor_settlement_date import spo
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

simulator = Stubs.simulator
act = Stubs.fix_act


def send_md(case_id, bid_price, ask_price):
    mdu_params = {
        "MDReqID": simulator.getMDRefIDForConnection314(
            request=RequestMDRefID(
                symbol="GBP/USD:SPO:REG:HSBC",
                connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
        'Instrument': {
            'Symbol': 'GBP/USD',
            'SecurityType': 'FXSPOT'
        },
        "NoMDEntries": [
            {
                "MDEntryType": "0",
                "MDEntryPx": bid_price,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                'SettlDate': tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": ask_price,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                'SettlDate': tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
    }
    act.sendMessage(
        bca.convert_to_request(
            'Send Market Data SPOT',
            'fix-fh-314-luna',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params, "fix-fh-314-luna")
        ))


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    base_bid = 1.18579
    base_ask = 1.18640

    first_ask = 1.18079
    first_bid = 1.18140

    second_bid = 1.17079
    second_ask = 1.17140

    third_bid = 1.16079
    third_ask = 1.16140

    fourth_bid = 1.15079
    fourth_ask = 1.15140
    client_tier = "Iridium1"
    account = "Iridium1_1"

    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date_spo = spo()
    settle_type_spo = "0"
    currency = "GBP"
    settle_currency = "USD"

    side = "1"
    qty = "1000000"

    try:
        send_md(case_id, base_bid, base_ask)
        time.sleep(5)
        checkpoint_response = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id = checkpoint_response.checkpoint
        params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol,
                                        currency=currency, settlcurrency=settle_currency,
                                        account=account)

        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        send_md(case_id, first_bid, first_ask)
        time.sleep(1)
        send_md(case_id, second_bid, second_ask)
        time.sleep(1)
        send_md(case_id, third_bid, third_ask)
        time.sleep(1)
        send_md(case_id, fourth_bid, fourth_ask)
        time.sleep(10)
        rfq.verify_quote_sequence(checkpoint_id_=checkpoint_id)



    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        # md.send_md_unsubscribe()
        pass
