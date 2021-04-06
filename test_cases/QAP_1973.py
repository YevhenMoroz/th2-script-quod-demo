import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from quod_qa.fx.default_params_fx import text_messages
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, case_params):
    case_name = Path(__file__).name[:-3]
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event(case_name, report_id)

    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXFWD'
            # 'SecurityType': 'FXSPOT'
            },
        'SettlDate': '20210412',
        # 'SettlDate': tsd.spo(),
        'SettlType': 'B'
        # 'SettlType': 0
    }

    def send_mdu(symbol):
        mdu_params = {
            "MDReqID": simulator.getMDRefIDForConnection303(
                    request=RequestMDRefID(
                            symbol=symbol,
                            connection_id=ConnectionID(session_alias="fix-fh-fx-esp"))).MDRefID,
            # "MDReportID": "1",
            # "MDTime": "TBU",
            # "MDArrivalTime": "TBU",
            # "OrigMDTime": "TBU",
            # "OrigMDArrivalTime": "TBU",
            # "ReplyReceivedTime": "TBU",
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXFWD'
            },
            # "LastUpdateTime": "TBU",
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 100.18189,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDEntrySpotRate": 100.01,
                    "MDEntryForwardPoints": 1.2345,
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 0.18195,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDEntrySpotRate": 0.1,
                    "MDEntryForwardPoints": 1.2345,
                },
                # {
                #     "MDEntryType": "0",
                #     "MDEntryPx": 1.18188,
                #     "MDEntrySize": 1000000,
                #     "MDEntryPositionNo": 1,
                #     "MDEntrySpotRate": 1.1819,
                #     # "MDEntryForwardPoints": 0.0002,
                #
                # },
                # {
                #     "MDEntryType": "1",
                #     "MDEntryPx": 1.18194,
                #     "MDEntrySize": 1000000,
                #     "MDEntryPositionNo": 1,
                #     "MDEntrySpotRate": 1.1820,
                #     # "MDEntryForwardPoints": 0.0002,
                # },
            ]
        }

        act.sendMessage(
            bca.convert_to_request(
                'Send MDU' + symbol,
                'fix-fh-fx-esp',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params, 'fix-fh-fx-esp')
            ))

    send_mdu('EUR/USD:FXF:WK1:GS')
    send_mdu('EUR/USD:FXF:WK1:CITI')
    send_mdu('EUR/USD:FXF:WK1:HSBC')
    send_mdu('EUR/USD:FXF:WK2:GS')
    send_mdu('EUR/USD:FXF:WK2:CITI')
    send_mdu('EUR/USD:FXF:WK2:HSBC')
    send_mdu('EUR/USD:FXF:BDA:GS')
    send_mdu('EUR/USD:FXF:BDA:CITI')
    send_mdu('EUR/USD:FXF:BDA:HSBC')

    useful_params = {
                    'RfqQty': '1000000'
        }
    rfq_params = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': useful_params['RfqQty'],
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
        }
    logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))

    quote_params = {
        **reusable_params,
        'QuoteReqID': rfq_params['QuoteReqID'],
        'Product': 4,
        'OfferPx': '35.001',
        'OfferSize': useful_params['RfqQty'],
        'QuoteID': '*',
        'OfferSpotRate': '35.001',
        'ValidUntilTime': '*',
        'Currency': 'EUR'
        }

    verifier.submitCheckRule(
            bca.create_check_rule(
                    text_messages['recQ'],
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
        'OrderQty': useful_params['RfqQty'],
        'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
        'Product': 4,
        'TimeInForce': 4
        }

    send_order = act.placeOrderFIX(
            bca.convert_to_request(
                    text_messages['sendNOS'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('NewOrderSingle', order_params, case_params['TraderConnectivity'])
                    ))

    er_pending_params = {
        'Side': reusable_params['Side'],
        'Account': reusable_params['Account'],
        'ClOrdID': order_params['ClOrdID'],
        'OrderQty': order_params['OrderQty'],
        'LeavesQty': order_params['OrderQty'],
        'TimeInForce': order_params['TimeInForce'],
        'OrdType': order_params['OrdType'],
        'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
        'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
        'NoParty': [
            {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
            ],
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityIDSource': 8,
            'SecurityID': 'EUR/USD',
            'SecurityExchange': 'XQFX'
            },
        'SettlCurrency': 'USD',
        'Currency': 'EUR',
        'HandlInst': 1,
        'AvgPx': 0,
        'QtyType': 0,
        'LastQty': 0,
        'CumQty': 0,
        'LastPx': 0,
        'OrdStatus': 'A',
        'ExecType': 'A',
        'ExecID': '*',
        'TransactTime': '*'
        }

    verifier.submitCheckRule(
            bca.create_check_rule(
                    text_messages['erPending'],
                    bca.filter_to_grpc('ExecutionReport', er_pending_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
                    send_order.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )

    # er_new_params = {
    #     'Side': reusable_params['Side'],
    #     'Account': reusable_params['Account'],
    #     'SettlDate': reusable_params['SettlDate'],
    #     'SettlType': reusable_params['SettlType'],
    #     'ClOrdID': order_params['ClOrdID'],
    #     'OrderQty': order_params['OrderQty'],
    #     'LeavesQty': order_params['OrderQty'],
    #     'TimeInForce': order_params['TimeInForce'],
    #     'OrdType': order_params['OrdType'],
    #     'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
    #     'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
    #     'NoParty': [
    #         {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
    #         ],
    #     'Instrument': {
    #         'Symbol': 'EUR/USD',
    #         'SecurityIDSource': 8,
    #         'SecurityID': 'EUR/USD',
    #         'SecurityExchange': 'XQFX'
    #         },
    #     'SettlCurrency': 'USD',
    #     'Currency': 'EUR',
    #     'ExecRestatementReason': 4,
    #     'HandlInst': 1,
    #     'AvgPx': 0,
    #     'QtyType': 0,
    #     'LastQty': 0,
    #     'CumQty': 0,
    #     'LastPx': 0,
    #     'OrdStatus': 0,
    #     'ExecType': 0,
    #     'ExecID': '*',
    #     'TransactTime': '*'
    #     }
    #
    # verifier.submitCheckRule(
    #         bca.create_check_rule(
    #                 messages['ExecReportPending'],
    #                 bca.filter_to_grpc('ExecutionReport', er_new_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
    #                 send_order.checkpoint_id,
    #                 case_params['TraderConnectivity'],
    #                 case_id
    #                 )
    #         )

    er_filled_params = {
        'Side': reusable_params['Side'],
        'Account': reusable_params['Account'],
        'SettlDate': reusable_params['SettlDate'],
        'TradeDate': datetime.utcnow().strftime('%Y%m%d'),
        'SettlType': reusable_params['SettlType'],
        'ClOrdID': order_params['ClOrdID'],
        'OrderQty': order_params['OrderQty'],
        'LeavesQty': 0,
        'TimeInForce': order_params['TimeInForce'],
        'OrdType': order_params['OrdType'],
        'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
        'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
        'NoParty': [
            {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
            ],
        'Instrument': {
            'SecurityType': 'FXSPOT',
            'Symbol': 'EUR/USD',
            'SecurityIDSource': 8,
            'SecurityID': 'EUR/USD',
            'SecurityExchange': 'XQFX'
            },
        'SettlCurrency': 'USD',
        'Currency': 'EUR',
        'HandlInst': 1,
        'AvgPx': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
        'QtyType': 0,
        'LastQty': order_params['OrderQty'],
        'CumQty': order_params['OrderQty'],
        'LastPx': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
        'OrdStatus': 2,
        'ExecType': 'F',
        'ExecID': '*',
        'TransactTime': '*'
        }

    verifier.submitCheckRule(
            bca.create_check_rule(
                    'Receive ExecutionReport (pending)',
                    bca.filter_to_grpc('ExecutionReport', er_filled_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
                    send_order.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
