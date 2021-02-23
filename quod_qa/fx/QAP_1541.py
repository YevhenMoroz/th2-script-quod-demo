import logging
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from quod_qa.fx.default_params_fx import defauot_quote_params, text_messages
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, case_params):
    # region Declaration
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time

    reusable_params = defauot_quote_params
    reusable_params['Account'] = case_params['Account']
    unknow_instrument = 'AAA/BBB'

    reusable_params['Instrument']['Symbol'] = unknow_instrument  # create a unknown instrument
    unknown_account = 'NotAccount'
    known_symbol = 'EUR/USD'
    wrong_qty1 = -1000000
    ttl = 100

    rfq_params = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': reusable_params['Instrument']['Symbol'][0:3],
            'QuoteType': '1',
            'OrderQty': reusable_params['OrderQty'],
            'OrdType': 'D',
            'ExpireTime': (datetime.now() + timedelta(seconds=ttl)).strftime("%Y%m%d-%H:%M:%S.000"),
            'TransactTime': (datetime.utcnow().isoformat())}]
        }
    quote_request_reject = {
        'QuoteReqID': rfq_params['QuoteReqID'],
        'NoRelatedSymbols': [{
            'Currency': unknow_instrument[:3],
            'Instrument': {
                'Symbol': unknow_instrument,
                }
            }],
        'Text': '11620 Unknown instrument',
        'header': {
            'MsgType': 'AG'
            }
        }
    # endregion

    # region Step 1 check of incorrect currency Symbol

    logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))

    verifier.submitCheckRule(
            bca.create_check_rule(
                    text_messages['recQRR'],
                    bca.filter_to_grpc('QuoteRequestReject', quote_request_reject, ['QuoteReqID']),
                    send_rfq.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )
    # endregion

    # region Step 2 check of incorrect Currency
    rfq_params['NoRelatedSymbols'][0]["Instrument"]['Symbol'] = known_symbol
    rfq_params['NoRelatedSymbols'][0]['Currency'] = unknow_instrument[:3]
    rfq_params['NoRelatedSymbols'][0]['Account'] = case_params['Account']
    quote_request_reject['NoRelatedSymbols'][0]["Instrument"]['Symbol'] = known_symbol
    quote_request_reject['NoRelatedSymbols'][0]['Currency'] = unknow_instrument[:3]
    quote_request_reject['Text'] = "11733 Given currency ({}) is neither base ({}) nor quote ({})".\
        format(unknow_instrument[:3],
               known_symbol[:3],
               known_symbol[-3:])

    logger.debug(text_messages['sendNOwithID'].format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))

    verifier.submitCheckRule(
            bca.create_check_rule(
                    text_messages['recQRR'],
                    bca.filter_to_grpc('QuoteRequestReject', quote_request_reject, ['QuoteReqID']),
                    send_rfq.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )
    # endregion

    # region Step 3 check of incorrect Account
    rfq_params['NoRelatedSymbols'][0]["Instrument"]['Symbol'] = known_symbol
    rfq_params['NoRelatedSymbols'][0]['Currency'] = known_symbol[:3]
    rfq_params['NoRelatedSymbols'][0]['Account'] = unknown_account
    quote_request_reject['NoRelatedSymbols'][0]["Instrument"]['Symbol'] = known_symbol
    quote_request_reject['NoRelatedSymbols'][0]['Currency'] = known_symbol[:3]
    quote_request_reject['Text'] = "11620 Unknown 'AccountGroupID': {} (not found in 'AccountGroup' cache)". \
        format(unknown_account)

    logger.debug(text_messages['sendNOwithID'].format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))

    verifier.submitCheckRule(
            bca.create_check_rule(
                    text_messages['recQRR'],
                    bca.filter_to_grpc('QuoteRequestReject', quote_request_reject, ['QuoteReqID']),
                    send_rfq.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )
    # endregion

    # region Step 4 checko of wrong qty

    rfq_params['NoRelatedSymbols'][0]['Account'] = case_params['Account']
    rfq_params['NoRelatedSymbols'][0]['OrderQty'] = wrong_qty1
    quote_request_reject['Text'] = "11603 'OrdQty' ({}) negative or zero". \
        format(wrong_qty1)

    logger.debug(text_messages['sendNOwithID'].format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))

    verifier.submitCheckRule(
            bca.create_check_rule(
                    text_messages['recQRR'],
                    bca.filter_to_grpc('QuoteRequestReject', quote_request_reject, ['QuoteReqID']),
                    send_rfq.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )
    # endregion

    # region Step 5 checko of wrong

    rfq_params['NoRelatedSymbols'][0]['Account'] = case_params['Account']
    rfq_params['NoRelatedSymbols'][0].pop('OrderQty')
    quote_request_reject['Text'] = "11603 'OrdQty' ({}) negative or zero". \
        format(wrong_qty1)

    logger.debug(text_messages['sendNOwithID'].format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))

    verifier.submitCheckRule(
            bca.create_check_rule(
                    text_messages['recQRR'],
                    bca.filter_to_grpc('QuoteRequestReject', quote_request_reject, ['QuoteReqID']),
                    send_rfq.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )
    # endregion






    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
