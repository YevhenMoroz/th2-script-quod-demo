import logging
import os
from datetime import datetime, timedelta
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


def extract_unassigned_grid(base_request, service, row, qty):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Status": "New"})
    base_data.set_filter_dict({"Qty": str(qty)})
    base_data.set_row_number(row)

    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_request.set_extraction_id("ExtractionId")
    extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.CreationTime", "CreationTime"), ])

    return call(service.getUnassignedRFQDetails, extraction_request.build())


def assign_firs_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_row_number(1)

    call(service.assignToMe, base_data.build())


def send_rfq(reusable_params, ttl, case_params, case_id, act):
    print('quote sent')
    rfq_params = {
        'QuoteReqID': bca.client_orderid(9),
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

    send_rfq = act.sendMessage(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))


def verify_sorting_order(rfq_id1, rfq_id2, case_id, table_name: str):
    # {'dealerIntervention.CreationTime': '2021/06/01 12:45:48.155'}
    # {'dealerIntervention.CreationTime': '2021/06/01 12:27:33.861'}
    #     rfq_id1 = '2021/06/01 12:45:48.155'
    #     rfq_id2 = '2021/06/01 12:27:33.861'
    expected_result = "correct(newest first)"
    datetime1 = datetime.strptime(rfq_id1['dealerIntervention.CreationTime'], '%Y/%m/%d %H:%M:%S.%f')
    datetime2 = datetime.strptime(rfq_id2['dealerIntervention.CreationTime'], '%Y/%m/%d %H:%M:%S.%f')
    delta = (datetime1 - datetime2).total_seconds()
    print(f'delta = {delta}')
    if delta > 0:
        actual_result = expected_result
    elif delta < 0:
        actual_result = "incorrect(latest first)"
    else:
        actual_result = "incorrect, time is equal"
    ver = Ver(case_id)
    ver.set_event_name(f"Check Sorting {table_name}")
    ver.compare_values('Order', actual_result, expected_result)
    ver.verify()


def extract_assigned_grid(base_request, service, row, qty):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Status": "New"})
    base_data.set_filter_dict({"Qty": str(qty)})
    base_data.set_row_number(row)

    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_request.set_extraction_id("ExtractionId")
    extraction_request.add_extraction_details(
            [ExtractionDetail("dealerIntervention.CreationTime", "CreationTime"), ])

    return call(service.getAssignedRFQDetails, extraction_request.build())


def execute(report_id, case_params):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    act = Stubs.fix_act
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    seconds, nanos = bca.timestamps()  # Store case start time
    service = Stubs.win_act_dealer_intervention_service
    ttl = 180
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
        'SettlType': '0',
        'OrderQty': '23000000'
        }

    try:
        # region send rfq
        send_rfq(reusable_params, ttl, case_params, case_id, act)
        send_rfq(reusable_params, ttl, case_params, case_id, act)
        # endregion

        prepare_fe(case_id, session_id)

        rfq_id1 = extract_unassigned_grid(base_request, service, 1, reusable_params['OrderQty'])
        rfq_id2 = extract_unassigned_grid(base_request, service, 2, reusable_params['OrderQty'])
        #
        print(f'result 1:{rfq_id1}')
        print(f'result 2:{rfq_id2}')

        assign_firs_request(base_request, service)
        assign_firs_request(base_request, service)

        verify_sorting_order(rfq_id1, rfq_id2, case_id, ' Unassigned Table')

        rfq_id1 = extract_assigned_grid(base_request, service, 1, reusable_params['OrderQty'])
        rfq_id2 = extract_assigned_grid(base_request, service, 2, reusable_params['OrderQty'])
        #
        print(f'result 1:{rfq_id1}')
        print(f'result 2:{rfq_id2}')

        verify_sorting_order(rfq_id1, rfq_id2, case_id, ' Assigned Table')



    except Exception as e:
        logging.error("Error execution", exc_info=True)

    finally:
        try:
            # region Clear Filters
            base_data = BaseTableDataRequest(base=base_request)
            base_data.set_row_number(1)
            extraction_request = ExtractionDetailsRequest(base_data)
            extraction_request.set_clear_flag()
            call(service.getAssignedRFQDetails, extraction_request.build())
            call(service.getUnassignedRFQDetails, extraction_request.build())
            # endregion
        except Exception:
            logging.error("Error execution", exc_info=True)

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
