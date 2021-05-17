import logging
import time
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from quod_qa.fx.default_params_fx import defauot_quote_params, text_messages
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

def execute(report_id, case_params):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    act = Stubs.fix_act
    verifier = Stubs.verifier


    reusable_params = defauot_quote_params
    reusable_params['Account'] = case_params['Account']
    reusable_params['Instrument']['Product'] = 4
    # TODO: ttl could be changed to smaller when it would be fixed( you may ask kbrit about it)
    ttl = 120
    wait_step = 5
    seconds, nanos = bca.timestamps()  # Store case start time

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
    logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))

    quote_params = {
        'QuoteReqID': rfq_params['QuoteReqID'],
        'Account': reusable_params['Account'],
        'OfferPx': '*',
        'OfferSize': reusable_params['OrderQty'],
        'QuoteID': '*',
        'OfferSpotRate': '*',
        'ValidUntilTime': '*',
        'Side': reusable_params['Side'],
        'SettlType': reusable_params['SettlType'],
        'SettlDate': reusable_params['SettlDate'],
        'Currency': 'EUR',
        'Instrument': reusable_params['Instrument'],
        'QuoteType': '1'
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


    print(f'Waiting while quote expire for {ttl} time')
    for i in range(0, int(ttl / wait_step + 1)):
        print(f'{ttl - i * wait_step}sec left')
        time.sleep(wait_step)

    quote_cancel_params = {
        'QuoteReqID': rfq_params['QuoteReqID'],
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD5',
        'QuoteCancelType': '5'
        }

    verifier.submitCheckRule(
            bca.create_check_rule(
                    "Checking QuoteCancell",
                    bca.filter_to_grpc("QuoteCancel", quote_cancel_params),
                    send_rfq.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
