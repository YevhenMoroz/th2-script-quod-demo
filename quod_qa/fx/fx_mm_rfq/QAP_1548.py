import logging
import os
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from custom.tenor_settlement_date import get_expire_time
from custom.verifier import Verifier as Ver, Verifier, VerificationMethod
from quod_qa.fx.default_params_fx import text_messages
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import (BaseTableDataRequest, ModificationRequest,
                                                          ExtractionDetailsRequest, RFQExtractionDetailsRequest)
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import prepare_fe_2, get_opened_fe, set_session_id, get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


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


def extract_unassigned_grid(base_request, service, qty, row=1):
    print('extract_unassigned_grid')
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Status": "New"})
    base_data.set_filter_dict({"Qty": str(qty)})
    base_data.set_row_number(row)

    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_request.set_extraction_id("ExtractionId")
    extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.Id", "Id")])

    return call(service.getUnassignedRFQDetails, extraction_request.build())


def assign_request(base_request, service, qty, rfq_id):
    print('assign_request')
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Id": rfq_id['dealerIntervention.Id']})
    base_data.set_filter_dict({"Qty": str(qty)})
    call(service.assignToMe, base_data.build())


def estimate_request(base_request, service, rfq_id):
    print('estimate_request')
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Id": rfq_id['dealerIntervention.Id']})
    call(service.estimate, base_data.build())


def send_rfq(reusable_params, ttl, case_params, case_id, act, rfq_id):
    print(f'quote sent with qty={reusable_params["OrderQty"]}')
    rfq_params = {
        'QuoteReqID': rfq_id,
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': reusable_params['OrderQty'],
            'OrdType': 'D',
            'ExpireTime': get_expire_time(ttl),
            'TransactTime': (datetime.utcnow().isoformat())}]
        }
    logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))

    act.sendMessage(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))


def reject_estimated_quote(base_request, service):
    print('send_estimated_quote')
    modify_request = ModificationRequest(base=base_request)
    modify_request.reject()
    call(service.modifyAssignedRFQ, modify_request.build())


def clear_filters(base_request, service):
    print('clear_filters')
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_row_number(1)
    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_request.set_clear_flag()
    call(service.getAssignedRFQDetails, extraction_request.build())
    call(service.getUnassignedRFQDetails, extraction_request.build())


def verify_quote_request_reject(quote_req_id, verifier, checkpoint_id, connectivity, case_id, instrument):
    print('verify_quote_request_reject')
    quote_request_reject = {
        'QuoteReqID': quote_req_id,
        'QuoteRequestRejectReason': '99',
        'NoRelatedSymbols': [{
            'Currency': instrument[:3],
            'Side': '*',
            'SettlType': '*',
            'OrdType': '*',
            'SettlDate': '*',
            'QuoteType': '*',
            'ExpireTime': '*',
            'Instrument': {
                'SecurityType':'FXSPOT',
                'Symbol': instrument,
                }
            }],
        'header': {
            'MsgType': 'AG'
            }
        }

    print('verify_quote_request')
    verifier.submitCheckRule(
            bca.create_check_rule(
                    text_messages['recQRR'],
                    bca.filter_to_grpc('QuoteRequestReject', quote_request_reject, ['QuoteReqID']),
                    checkpoint_id,
                    connectivity,
                    case_id
                    )
            )


def execute(report_id, case_params):
    # region Preparation
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    act = Stubs.fix_act
    verifier = Stubs.verifier
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    seconds, nanos = bca.timestamps()  # Store case start time
    service = Stubs.win_act_dealer_intervention_service
    ttl = 180
    ask_large = '1.'
    ask_small = '456'
    result_price = f'{ask_large}{ask_small}'
    print(tsd.spo())
    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT',
            'Product': '4',
            },
        'SettlDate': tsd.spo(),
        'SettlType': '2',
        'OrderQty': '26130000'
        }
    rfq_id = bca.client_orderid(9)
    # endregion

    try:
        send_rfq(reusable_params, ttl, case_params, case_id, act, rfq_id)

        prepare_fe(case_id, session_id)

        print(f'rfq_id = {rfq_id}')
        rfq_id_fe = extract_unassigned_grid(base_request, service, reusable_params['OrderQty'])
        print(f'rfq_id = {rfq_id_fe}')
        assign_request(base_request, service, reusable_params['OrderQty'], rfq_id_fe)

        estimate_request(base_request, service, rfq_id_fe)


        # Checkpoint1 creation
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint

        reject_estimated_quote(base_request, service)

        time.sleep(3)

        verify_quote_request_reject(rfq_id,
                                    verifier,
                                    checkpoint_id1,
                                    case_params['TraderConnectivity'],
                                    case_id,reusable_params['Instrument']['Symbol'])


    except Exception as e:
        logging.error("Error execution", exc_info=True)

    finally:
        try:
            clear_filters(base_request, service)
        except Exception:
            logging.error("Error finalization", exc_info=True)

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
