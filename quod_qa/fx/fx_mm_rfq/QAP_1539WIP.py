import logging
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import get_expire_time
from custom.verifier import Verifier
from quod_qa.fx.default_params_fx import defauot_quote_params, text_messages
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


# TODO: quod: add  filter clear in finally block

def prepare_fe(case_id, session_id):
    Stubs.frontend_is_open = True
    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
        # ,
        #          fe_dir='qf_trading_fe_folder_308',
        #          fe_user='qf_trading_fe_user_308',
        #          fe_pass='qf_trading_fe_password_308')
    else:
        get_opened_fe(case_id, session_id)


def send_rfq(rfq_params, act, connectivity, case_id):
    logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))

    send_rfq = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    connectivity,
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, connectivity)
                    ))
    return send_rfq


def verify_qute(reusable_params, rfq_params, case_id, verifier, sent_rfq, connectivity):
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
                    sent_rfq.checkpoint_id,
                    connectivity,
                    case_id
                    )
            )


def cansel_quote(rfq_params, act, connectivity, case_id):
    quote_cancel_params = {
        'QuoteReqID': rfq_params['QuoteReqID'],
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD5',
        'QuoteCancelType': '5'
        }
    logger.debug("Send new order with ClOrdID = {}".format(quote_cancel_params['QuoteReqID']))

    act.sendMessage(
            bca.convert_to_request(
                    'Trying to send QuoteCancel',
                    connectivity,
                    case_id,
                    bca.message_to_grpc('QuoteCancel', quote_cancel_params, connectivity)
                    ))


def check_cancelled_rfq_in_rfq_book(base_request, service, case_id, instrument, qty, client):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["InstrSymbol", instrument,
                    "Qty", str(qty),
                    "Client", client,
                    "Status", 'New'])
    status = ExtractionDetail("quoteRequestBook.status", "Status")
    quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([status, quote_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values('Status', 'Terminated', response[status.name])
    verifier.compare_values("QuoteStatus", 'Canceled', response[quote_status.name])
    verifier.verify()


def execute(report_id, case_params):
    try:
        case_name = Path(__file__).name
        case_id = bca.create_event(case_name, report_id)
        session_id = set_session_id()
        set_base(session_id, case_id)
        base_request = get_base_request(session_id, case_id)

        act = Stubs.fix_act
        verifier = Stubs.verifier
        ar_service = Stubs.win_act_aggregated_rates_service

        seconds, nanos = bca.timestamps()  # Store case start time

        reusable_params = defauot_quote_params
        reusable_params['Account'] = case_params['Account']
        reusable_params['Instrument']['Product'] = 4

        ttl = 120
        rfq_params = {
            'QuoteReqID': bca.client_orderid(9),
            'NoRelatedSymbols': [{
                **reusable_params,
                'Currency': reusable_params['Instrument']['Symbol'][0:3],
                'QuoteType': '1',
                'OrderQty': reusable_params['OrderQty'],
                'OrdType': 'D',
                'ExpireTime': get_expire_time(ttl),
                'TransactTime': (datetime.utcnow().isoformat())}]
            }
        sent_rfq = send_rfq(rfq_params, act, case_params['TraderConnectivity'], case_id)

        verify_qute(reusable_params, rfq_params, case_id, verifier, sent_rfq, case_params['TraderConnectivity'])

        cansel_quote(rfq_params, act, case_params['TraderConnectivity'], case_id)

        prepare_fe(case_id, session_id)

        check_cancelled_rfq_in_rfq_book(base_request,
                                        ar_service,
                                        case_id,
                                        reusable_params['Instrument']['Symbol'],
                                        reusable_params['OrderQty'],
                                        case_params['Account'])

    except Exception as e:
        logging.error(f'Error execution \n{e}', exc_info=True)
    # finally:
    #     try:
    #         clear_filters_rfq_book(base_request, service)
    #     except Exception:
    #         logging.error("Error finalization", exc_info=True)

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
