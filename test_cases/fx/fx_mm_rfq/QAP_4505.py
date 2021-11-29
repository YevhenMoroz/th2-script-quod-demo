import logging
import time
from datetime import datetime

from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from custom.tenor_settlement_date import spo
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

simulator = Stubs.simulator
act = Stubs.fix_act
verifier = Stubs.verifier
api = Stubs.api_service


def change_update_interval(case_id, interval):
    params = {
        "clientQuoteIDFormat": "#20d",
        "updateMDEntryID": "true",
        "ackOrder": "false",
        "MDUpdateType": "FUL",
        "quotingSessionName": "QSRFQTH2",
        "supportMDRequest": "true",
        "tradingQuotingSession": "true",
        "quotingSessionID": 10,
        "concurrentlyActiveQuoteAge": 120000,
        "updateInterval": interval,
    }
    api.sendMessage(
        request=SubmitMessageRequest(message=bca.wrap_message(params, 'ModifyQuotingSession', 'rest_wa314luna'),
                                     parent_event_id=case_id))


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

    first_bid = 1.18079
    first_ask = 1.18140

    second_bid = 1.17079
    second_ask = 1.17140

    third_bid = 1.16079
    third_ask = 1.16140

    fourth_bid = 1.15079
    fourth_ask = 1.15140
    client_tier = "Iridium1"

    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date_spo = spo()
    settle_type_spo = "0"
    currency = "GBP"

    qty = "1000000"

    quote_params_base = {
        'QuoteID': "*",
        'QuoteMsgID': "*",
        'BidSpotRate': base_bid,
        'SettlType': "*",
        'SettlDate': settle_date_spo,
        'OfferPx': base_ask,
        'OfferSize': qty,
        'BidPx': base_bid,
        'BidSize': qty,
        'ValidUntilTime': '*',
        'OfferSpotRate': base_ask,
        'Currency': currency,
        'Instrument': {
            'Symbol': symbol,
            'SecurityType': security_type_spo,
            'Product': 4,
        },
        'QuoteReqID': '*',
        'QuoteType': 1,
    }
    quote_params4 = {
        'QuoteID': "*",
        'QuoteMsgID': "*",
        'BidSpotRate': fourth_bid,
        'SettlType': "*",
        'SettlDate': settle_date_spo,
        'OfferPx': fourth_ask,
        'OfferSize': qty,
        'BidPx': fourth_bid,
        'BidSize': qty,
        'ValidUntilTime': '*',
        'OfferSpotRate': fourth_ask,
        'Currency': currency,
        'Instrument': {
            'Symbol': symbol,
            'SecurityType': security_type_spo,
            'Product': 4,
        },
        'QuoteReqID': '*',
        'QuoteType': 1,
    }

    try:
        change_update_interval(case_id, 10000)
        send_md(case_id, base_bid, base_ask)
        time.sleep(5)
        checkpoint_response = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id = checkpoint_response.checkpoint
        quote_req_id = bca.client_orderid(8)
        quote_request_params = {
            'QuoteReqID': quote_req_id,
            'NoRelatedSymbols': [{
                'Account': client_tier,
                'Instrument': {
                    'Symbol': symbol,
                    'SecurityType': security_type_spo
                },
                'SettlDate': settle_date_spo,
                'SettlType': settle_type_spo,
                'Currency': currency,
                'QuoteType': '1',
                'OrderQty': qty,
                'OrdType': 'D'
            }
            ]
        }
        quote = act.placeQuoteFIX(
            request=bca.convert_to_request(
                "SendQuoteRequest",
                "fix-ss-rfq-314-luna-standard",
                case_id,
                bca.message_to_grpc("QuoteRequest", quote_request_params, "fix-ss-rfq-314-luna-standard")
            )
        )
        send_md(case_id, first_bid, first_ask)
        time.sleep(1)
        send_md(case_id, second_bid, second_ask)
        time.sleep(1)
        send_md(case_id, third_bid, third_ask)
        time.sleep(1)
        send_md(case_id, fourth_bid, fourth_ask)
        time.sleep(10)
        quotes_sequence_params = {
            'header': {
                'MsgType': ('0', "NOT_EQUAL"),
                'TargetCompID': 'QUOD9',
                'SenderCompID': 'QUODFX_UAT'
            },
        }
        message_filters_req = [
            bca.filter_to_grpc('Quote', quote_params_base),
            bca.filter_to_grpc('Quote', quote_params4)
        ]
        pre_filter_req = bca.prefilter_to_grpc(quotes_sequence_params)
        verifier.submitCheckSequenceRule(
            bca.create_check_sequence_rule(
                description="Check Quotes",
                prefilter=pre_filter_req,
                msg_filters=message_filters_req,
                checkpoint=checkpoint_id,
                connectivity="fix-ss-rfq-314-luna-standard",
                event_id=case_id,
                timeout=3000
            )
        )
        quote_req_id = quote.response_messages_list[0].fields["QuoteReqID"].simple_value
        quote_cancel_params = {
            'QuoteReqID': quote_req_id,
            'QuoteID': '*',
            'QuoteCancelType': '5',
        }
        act.sendMessage(
            bca.convert_to_request(
                'Send QuoteCancel', "fix-ss-rfq-314-luna-standard", case_id,
                bca.message_to_grpc('QuoteCancel', quote_cancel_params,
                                    "fix-ss-rfq-314-luna-standard")
            ))
        change_update_interval(case_id, 10000)
    except Exception:
        logging.error('Error execution', exc_info=True)
