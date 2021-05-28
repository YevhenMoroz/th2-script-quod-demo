import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name='sendMD'
    act = Stubs.fix_act
    event_store = Stubs.event_store
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    quote_request_qty = 500000
    instrument = 'EUR/USD'
    tenor = 'FXSPOT'

    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event(case_name, report_id)

    mdu_params_spo_hsbc = {
        "MDReqID": simulator.getMDRefIDForConnection303(request=RequestMDRefID(symbol="EUR/USD:SPO:REG:HSBC",
                                                                               connection_id=ConnectionID(
                                                                                   session_alias="fix-fh-314-luna"))).MDRefID,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
        },
        "NoMDEntries": [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.02,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.03,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.026,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.027,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1,
                "MDEntrySize": 20000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.2,
                "MDEntrySize": 20000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
    }

    mdu_params_spo_citi = {
        "MDReqID": simulator.getMDRefIDForConnection303(request=RequestMDRefID(symbol="EUR/USD:SPO:REG:CITI",
                                                                               connection_id=ConnectionID(
                                                                                   session_alias="fix-fh-314-luna"))).MDRefID,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
        },
        "NoMDEntries": [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.02,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.03,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.025,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.026,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.04,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.05,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
    }

    mdu_params_spo_gs = {
        "MDReqID": simulator.getMDRefIDForConnection303(request=RequestMDRefID(symbol="EUR/USD:SPO:REG:GS",
                                                                               connection_id=ConnectionID(
                                                                                   session_alias="fix-fh-314-luna"))).MDRefID,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
        },
        "NoMDEntries": [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.01,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.02,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.02,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.03,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.03,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.04,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
    }

    act.sendMessage(
        bca.convert_to_request(
            'Send MDU',
            'fix-fh-314-luna',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo_hsbc, 'fix-fh-314-luna')
        ))

    act.sendMessage(
        bca.convert_to_request(
            'Send MDU',
            'fix-fh-314-luna',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo_citi, 'fix-fh-314-luna')
        ))

    act.sendMessage(
        bca.convert_to_request(
            'Send MDU',
            'fix-fh-314-luna',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo_gs, 'fix-fh-314-luna')
        ))

    # reusable_params = {
    #     'Account': case_params['Account'],
    #     'Side': 1,
    #     'Instrument': {
    #         'Symbol': instrument,
    #         'SecurityType': 'FXSWAP'
    #     },
    #     'SettlDate': tsd.spo(),
    #     'SettlType': '0'
    # }
    #
    # rfq_params = {
    #     'QuoteReqID': bca.client_orderid(9),
    #     'NoRelatedSymbols': [
    #         {
    #             'Instrument': reusable_params['Instrument'],
    #             'OrderQty': 16000001,
    #             'Currency': 'EUR',
    #             'Account': reusable_params['Account'],
    #             'NoLegs': [
    #                 {
    #                     'InstrumentLeg': {
    #                         'LegSymbol': instrument,
    #                         'LegSecurityType': 'FXSPOT'
    #                     },
    #                     'LegSide': 1,
    #                     'LegSettlType': 0,
    #                     'LegSettlDate': tsd.spo(),
    #                     'LegOrderQty': 16000001
    #                 },
    #                 {
    #                     'InstrumentLeg': {
    #                         'LegSymbol': instrument,
    #                         'LegSecurityType': 'FXFWD'
    #                     },
    #                     'LegSide': 2,
    #                     'LegSettlType': 7,
    #                     'LegSettlDate': tsd.wk1(),
    #                     'LegOrderQty': 16000001
    #                 },
    #             ]
    #         }
    #     ]
    # }
    # logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))
    #
    # send_rfq = act.placeQuoteFIX(
    #     bca.convert_to_request(
    #         'Send QuoteRequest',
    #         case_params['TraderConnectivity'],
    #         case_id,
    #         bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
    #     ))

    # quote_params = {
    #     **reusable_params,
    #     'QuoteReqID': rfq_params['QuoteReqID'],
    #     'Product': 4,
    #     'OfferPx': '35.001',
    #     'OfferSize': 500000,
    #     'QuoteID': '*',
    #     'OfferSpotRate': '35.001',
    #     'ValidUntilTime': '*',
    #     'Currency': 'EUR'
    # }
    #
    # verifier.submitCheckRule(
    #     bca.create_check_rule(
    #         'Receive Quote message',
    #         bca.filter_to_grpc('Quote', quote_params, ['QuoteReqID']),
    #         send_rfq.checkpoint_id,
    #         case_params['TraderConnectivity'],
    #         case_id
    #     )
    # )
    #
    # order_params = {
    #     **reusable_params,
    #     'QuoteID': send_rfq.response_messages_list[0].fields['QuoteID'],
    #     'ClOrdID': bca.client_orderid(9),
    #     'OrdType': 'D',
    #     'TransactTime': (datetime.utcnow().isoformat()),
    #     'OrderQty': '1000000',
    #     'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
    #     'Product': 4,
    #     'TimeInForce': 4
    # }
    #
    # send_order = act.placeOrderFIX(
    #     bca.convert_to_request(
    #         'Send NewOrderSingle',
    #         case_params['TraderConnectivity'],
    #         case_id,
    #         bca.message_to_grpc('NewOrderSingle', order_params, case_params['TraderConnectivity'])
    #     ))
    #
    # er_pending_params = {
    #     'Side': reusable_params['Side'],
    #     'Account': reusable_params['Account'],
    #     'ClOrdID': order_params['ClOrdID'],
    #     'OrderQty': order_params['OrderQty'],
    #     'LeavesQty': order_params['OrderQty'],
    #     'TimeInForce': order_params['TimeInForce'],
    #     'OrdType': order_params['OrdType'],
    #     'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
    #     'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
    #     'NoParty': [
    #         {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
    #     ],
    #     'Instrument': {
    #         'Symbol': 'EUR/USD',
    #         'SecurityIDSource': 8,
    #         'SecurityID': 'EUR/USD',
    #         'SecurityExchange': 'XQFX'
    #     },
    #     'SettlCurrency': 'USD',
    #     'Currency': 'EUR',
    #     'HandlInst': 1,
    #     'AvgPx': 0,
    #     'QtyType': 0,
    #     'LastQty': 0,
    #     'CumQty': 0,
    #     'LastPx': 0,
    #     'OrdStatus': 'A',
    #     'ExecType': 'A',
    #     'ExecID': '*',
    #     'TransactTime': '*'
    # }
    #
    # verifier.submitCheckRule(
    #     bca.create_check_rule(
    #         'Receive ExecutionReport (pending)',
    #         bca.filter_to_grpc('ExecutionReport', er_pending_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
    #         send_order.checkpoint_id,
    #         case_params['TraderConnectivity'],
    #         case_id
    #     )
    # )
    #
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
    #     ],
    #     'Instrument': {
    #         'Symbol': 'EUR/USD',
    #         'SecurityIDSource': 8,
    #         'SecurityID': 'EUR/USD',
    #         'SecurityExchange': 'XQFX'
    #     },
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
    # }
    #
    # verifier.submitCheckRule(
    #     bca.create_check_rule(
    #         'Receive ExecutionReport (pending)',
    #         bca.filter_to_grpc('ExecutionReport', er_new_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
    #         send_order.checkpoint_id,
    #         case_params['TraderConnectivity'],
    #         case_id
    #     )
    # )
    #
    # er_filled_params = {
    #     'Side': reusable_params['Side'],
    #     'Account': reusable_params['Account'],
    #     'SettlDate': reusable_params['SettlDate'],
    #     'TradeDate': datetime.utcnow().strftime('%Y%m%d'),
    #     'SettlType': reusable_params['SettlType'],
    #     'ClOrdID': order_params['ClOrdID'],
    #     'OrderQty': order_params['OrderQty'],
    #     'LeavesQty': 0,
    #     'TimeInForce': order_params['TimeInForce'],
    #     'OrdType': order_params['OrdType'],
    #     'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
    #     'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
    #     'NoParty': [
    #         {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
    #     ],
    #     'Instrument': {
    #         'SecurityType': 'FXSPOT',
    #         'Symbol': 'EUR/USD',
    #         'SecurityIDSource': 8,
    #         'SecurityID': 'EUR/USD',
    #         'SecurityExchange': 'XQFX'
    #     },
    #     'SettlCurrency': 'USD',
    #     'Currency': 'EUR',
    #     'HandlInst': 1,
    #     'AvgPx': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
    #     'QtyType': 0,
    #     'LastQty': order_params['OrderQty'],
    #     'CumQty': order_params['OrderQty'],
    #     'LastPx': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
    #     'OrdStatus': 2,
    #     'ExecType': 'F',
    #     'ExecID': '*',
    #     'TransactTime': '*'
    # }
    #
    # verifier.submitCheckRule(
    #     bca.create_check_rule(
    #         'Receive ExecutionReport (pending)',
    #         bca.filter_to_grpc('ExecutionReport', er_filled_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
    #         send_order.checkpoint_id,
    #         case_params['TraderConnectivity'],
    #         case_id
    #     )
    # )

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))

