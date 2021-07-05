import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from quod_qa.fx.default_params_fx import defauot_quote_params
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, case_params):
    case_name = Path(__file__).name
    case_id = bca.create_event(case_name, report_id)

    act = Stubs.fix_act
    verifier = Stubs.verifier
    seconds, nanos = bca.timestamps()  # Store case start time

    reusable_params = defauot_quote_params
    reusable_params['Account'] = case_params['Account']
    reusable_params.pop('OrderQty')
    useful_params = {
        'RfqQty': '500000',
        'OrderQty': '1000000'
        }

    rfq_params = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': reusable_params['Instrument']['Symbol'][0:3],
            'QuoteType': '1',
            'OrderQty': useful_params['RfqQty'],
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
        'OfferSize': useful_params['RfqQty'],
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
        'OrderQty': useful_params['OrderQty'],
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
            'Symbol': reusable_params['Instrument']['Symbol'],
            'SecurityIDSource': 8,
            'SecurityID': reusable_params['Instrument']['Symbol'],
            'SecurityExchange': 'XQFX'
            },
        'Text': "11605 'OrdQty' ({}) doesn't match the quote's 'OfferSize' ({})".
            format(useful_params['OrderQty'], useful_params['RfqQty']),

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
    # TODO: quod: add check of second FE User
    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
