import logging
import pandas as pd
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from stubs import Stubs


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = Stubs.fix_act
    event_store = Stubs.event_store
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event(case_name, report_id)

    instrument_spot = {
        'Symbol': 'EUR/USD',
        'SecurityType': 'FXSPOT'
    }

# Market data update
#     mdu_params = {
#         "MDReqID": "EUR/USD:SPO:REG:HSBC_2",
#         "MDReportID": "3",
#         # "MDTime": "TBU",
#         # "MDArrivalTime": "TBU",
#         # "OrigMDTime": "TBU",
#         # "OrigMDArrivalTime": "TBU",
#         # "ReplyReceivedTime": "TBU",
#         "Instrument": instrument_fx,
#         # "LastUpdateTime": "TBU",
#         "NoMDEntries": [
#             {
#                 "MDEntryType": "1",
#                 "MDEntryPx": 100,
#                 "MDEntrySize": 1000,
#                 "MDEntryPositionNo": 1
#             },
#             {
#                 "MDEntryType": "0",
#                 "MDEntryPx": 110,
#                 "MDEntrySize": 1000,
#                 "MDEntryPositionNo": 1
#             },
#
#         ]
#     }
#
#     send_mdu = act.sendMessage(
#         bca.convert_to_request(
#             'Send MDU',
#             'fix-fh-fx-esp',
#             case_id,
#             bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params, 'fix-fh-fx-esp')
#         ))

# Prepare user input
    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': instrument_spot,
        'SettlDate': tsd.spo()
    }

    rfq_params = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
                                **reusable_params,
                                'Currency': 'EUR',
                                'QuoteType': '1',
                                'OrderQty': '1000000',
                                'OrdType': 'D',
                                'ExpireTime': '20210128-00:00:00.000',
                                'TransactTime': (datetime.utcnow().isoformat()),
                                'SettlType': '0'}]
    }
    logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
        bca.convert_to_request(
            'Send QuoteRequest',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
        ))

    quote_params = {
        **reusable_params,
        'QuoteReqID': rfq_params['QuoteReqID'],
        'Product': 4
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive Quote message',
            bca.filter_to_grpc('Quote', quote_params, ['QuoteReqID']),
            send_rfq.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    order_params = {
        **reusable_params,
        'QuoteID': send_rfq.response_messages_list[0].fields['QuoteID'],
        'ClOrdID': bca.client_orderid(9),
        'OrdType': 'D',
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': '1000000',
        'Price': send_rfq.response_messages_list[0].fields['OfferPx'],
        'Product': 4,
        'TimeInForce': 4
    }

    send_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewOrderSingle',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', order_params, case_params['TraderConnectivity'])
        ))

    # print(dir(send_RFQ))
    # print()

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
