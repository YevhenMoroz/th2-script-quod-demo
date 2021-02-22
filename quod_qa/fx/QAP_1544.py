import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event(case_name, report_id)

    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
            },
        'SettlDate': tsd.spo(),
        'SettlType': '0',
        'RfqQty': '500000',
        'OrderQty': '1000000'
        }

    rfq_params = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': reusable_params['Instrument']['Symbol'][0:3],
            'QuoteType': '1',
            'OrderQty': reusable_params['RfqQty'],
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
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
        'Product': 4,
        'OfferPx': '35.001',
        'OfferSize': reusable_params['RfqQty'],
        'QuoteID': '*',
        'OfferSpotRate': '35.001',
        'ValidUntilTime': '*',
        'Currency': 'EUR'
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
        'OrderQty': reusable_params['OrderQty'],
        'Price': send_rfq.response_messages_list[0].fields['OfferPx'].simple_value,
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

    er_pending_params = {
        'Side': reusable_params['Side'],
        'Account': reusable_params['Account'],
        'ClOrdID': order_params['ClOrdID'],
        'OrderQty': order_params['OrderQty'],
        'TimeInForce': order_params['TimeInForce'],
        'OrdRejReason': '99',
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityIDSource': 8,
            'SecurityID': 'EUR/USD',
            'SecurityExchange': 'XQFX'
            },
        'Text': "11605 'OrdQty' (1000000) doesn't match the quote's 'OfferSize' (500000)",

        }

    verifier.submitCheckRule(
            bca.create_check_rule(
                    'Receive ExecutionReport (pending)',
                    bca.filter_to_grpc('ExecutionReport', er_pending_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
                    send_order.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
