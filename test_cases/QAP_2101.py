import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe303, close_fe, call
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = Stubs.fix_act
    event_store = Stubs.event_store
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    quote_request_qty = 500000
    instrument = 'EUR/USD'
    tenor = 'FXSPOT'

    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event(case_name, report_id)

    mdu_params_fwd = {
        "MDReqID": simulator.getMDRefIDForConnection303(
            request=RequestMDRefID(
                symbol="EUR/USD:FXF:WK1:CITI", connection_id=ConnectionID(
                    session_alias="fix-fh-fx-esp"))).MDRefID,
        # "MDReqID": "EUR/USD:FXF:WK1:HSBC",
        "MDReportID": "3",
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
                "MDEntryPx": 31.18192,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntrySpotRate": 31.1819,
                "MDEntryForwardPoints": 0.0002,
                # 'SettlDate': tsd.wk1(),
                # "MDEntryDate": datetime.utcnow().strftime('%Y-%m-%d'),
                # "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 39.18220,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntrySpotRate": 39.1820,
                "MDEntryForwardPoints": 0.0002,
                # 'SettlDate': tsd.wk1(),
                # "MDEntryDate": datetime.utcnow().strftime('%Y-%m-%d'),
                # "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
            }
        ]
    }

    act.sendMessage(
        bca.convert_to_request(
            'Send MDU',
            'fix-fh-fx-esp',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_fwd, 'fix-fh-fx-esp')
        ))

    mdu_params_spo = {
        "MDReqID": simulator.getMDRefIDForConnection303(
            request=RequestMDRefID(
                symbol="EUR/USD:SPO:REG:HSBC", connection_id=ConnectionID(
                    session_alias="fix-fh-fx-esp"))).MDRefID,
        # "MDReqID": "EUR/USD:FXF:WK1:HSBC",
        "MDReportID": "3",
        # "MDTime": "TBU",
        # "MDArrivalTime": "TBU",
        # "OrigMDTime": "TBU",
        # "OrigMDArrivalTime": "TBU",
        # "ReplyReceivedTime": "TBU",
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
        },
        # "LastUpdateTime": "TBU",
        "NoMDEntries": [
            {
                "MDEntryType": "0",
                "MDEntryPx": 31.1819,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntrySpotRate": 31.1819,
                "MDEntryForwardPoints": 0.0002,
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 39.1820,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntrySpotRate": 39.1820,
                "MDEntryForwardPoints": 0.0002,
            }
        ]
    }

    act.sendMessage(
        bca.convert_to_request(
            'Send MDU',
            'fix-fh-fx-esp',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, 'fix-fh-fx-esp')
        ))

    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': instrument,
            'SecurityType': 'FXSWAP',
            # 'Product': 4
        },
        'SettlDate': tsd.spo(),
        'SettlType': '0'
    }

    rfq_params = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [
            {
                'Instrument': reusable_params['Instrument'],
                'OrderQty': 1000000,
                'Currency': 'EUR',
                'Account': reusable_params['Account'],
                'NoLegs': [
                    {
                        'InstrumentLeg': {
                            'LegSymbol': instrument,
                            'LegSecurityType': 'FXSPOT'
                        },
                        'LegSide': 1,
                        'LegSettlType': 0,
                        'LegSettlDate': tsd.spo(),
                        'LegOrderQty': 1000000
                    },
                    {
                        'InstrumentLeg': {
                            'LegSymbol': instrument,
                            'LegSecurityType': 'FXFWD'
                        },
                        'LegSide': 2,
                        'LegSettlType': '1W',
                        'LegSettlDate': tsd.wk1(),
                        'LegOrderQty': 1000000
                    },
                ]
            }
        ]
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
        'Account': case_params['Account'],
        'Instrument': {
            'Symbol': instrument,
            'SecurityType': 'FXSWAP',
            'Product': 4,
        },
        'QuoteReqID': rfq_params['QuoteReqID'],
        'OfferSize': 1000000,
        'BidSize': 1000000,
        'QuoteID': '*',
        'ValidUntilTime': '*',
        'Currency': 'EUR',
        'BidSpotRate': 35.18195,
        'OfferSpotRate': 35.18195,
        'OfferSwapPoints': 0,
        'BidSwapPoints': 0,
        'OfferPx': 0,
        'BidPx': 0,
        'QuoteType': 1,
        'NoLegs': [
            {
                'LegSide': 1,
                'InstrumentLeg': {}
            },
            {
                'LegSide': 1,
                'InstrumentLeg': {}
            }
        ]
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
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': instrument,
            'SecurityType': 'FXSWAP',
            'Product': 4
        },
        'SettlDate': tsd.spo(),
        'SettlType': '0',
        'QuoteID': send_rfq.response_messages_list[0].fields['QuoteID'],
        'ClOrdID': bca.client_orderid(9),
        'OrdType': 'D',
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': '1000000',
        'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
        # 'Product': 4,
        'TimeInForce': 4
    }

    send_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewOrderSingle',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', order_params, case_params['TraderConnectivity'])
        ))
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

    # GUI block
    common_act = Stubs.win_act
    ob_act = Stubs.win_act_order_book
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    prepare_fe303(case_id, session_id, Stubs.custom_config['qf_trading_fe_folder_303'],
                  Stubs.custom_config['qf_trading_fe_user_303'], Stubs.custom_config['qf_trading_fe_password_303'])

    execution_id = bca.client_orderid(4)
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob_exec_sts = ExtractionDetail('orderBook.execsts', 'ExecSts')
    ob_id = ExtractionDetail('orderBook.quoteid', 'QuoteID')
    order_info = OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_details=[ob_exec_sts, ob_id]))
    ob.add_single_order_info(
        order_info)
    call(ob_act.getOrdersDetails, ob.request())

    call(common_act.verifyEntities, verification(execution_id, 'checking OB',
                                                 [verify_ent('OB ExecSts', ob_exec_sts.name, 'Filled'),
                                                  verify_ent('OB ID vs QB ID', ob_id.name,
                                                             send_rfq.response_messages_list[0].fields['QuoteID'])]))

    close_fe(case_id, session_id)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
