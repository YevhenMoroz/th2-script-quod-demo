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
    # FIXME: multiple issue appears because of dictionary fields differ
    #       check pod="gtwquod5-fx-..."
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    act = Stubs.fix_act
    verifier = Stubs.verifier
    ttl = 120
    wait_step = 5
    seconds, nanos = bca.timestamps()  # Store case start time

    reusable_params = defauot_quote_params
    reusable_params['Account'] = case_params['Account']
    reusable_params['Instrument']['Product'] = 4

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
        'OfferPx': '*',
        'OfferSize': reusable_params['OrderQty'],
        'QuoteID': '*',
        'OfferSpotRate': '*',
        'ValidUntilTime': '*',
        'Currency': 'EUR',
        'QuoteType': rfq_params['NoRelatedSymbols'][0]['QuoteType'],
        'Instrument': reusable_params['Instrument'],
        'Side': reusable_params['Side'],
        'SettlDate': reusable_params['SettlDate'],
        'SettlType': reusable_params['SettlType'],
        'Account': reusable_params['Account']

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
    for i in range(0, int(ttl / wait_step + 2)):
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
