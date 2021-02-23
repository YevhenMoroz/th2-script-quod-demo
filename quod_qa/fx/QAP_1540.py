import logging
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from quod_qa.fx.default_params_fx import defauot_quote_params, text_messages
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# fixme: add checko of quote in quote book on FE Tradign
def execute(report_id, case_params):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time

    reusable_params = defauot_quote_params
    reusable_params['Account'] = case_params['Account']
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
        'Product': 4,
        'OfferPx': '35.001',
        'OfferSize': reusable_params['OrderQty'],
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

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
