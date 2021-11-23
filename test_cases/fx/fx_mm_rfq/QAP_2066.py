import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from custom.tenor_settlement_date import get_expire_time
from custom.verifier import Verifier as Ver, Verifier, VerificationMethod
from test_cases.fx.default_params_fx import text_messages
from test_framework.old_wrappers.common_win import prepare_fe
from test_framework.old_wrappers.fx_mm_rfq import send_swap_rfq
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import (BaseTableDataRequest, ModificationRequest,
                                                          ExtractionDetailsRequest, RFQExtractionDetailsRequest)
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import prepare_fe_2, get_opened_fe, set_session_id, get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def extract_unassigned_grid(base_request, service, qty, row=1):
    print('extract_unassigned_grid()')
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Status": "New"})
    base_data.set_filter_dict({"Qty": str(qty)})
    base_data.set_row_number(row)

    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_request.set_extraction_id("ExtractionId")
    extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.Id", "Id")])

    id =  call(service.getUnassignedRFQDetails, extraction_request.build())
    return id['dealerIntervention.Id']


def assign_firs_request(base_request, service, rfq_id: str):
    print('assign_firs_request()')
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({'Id': rfq_id})

    call(service.assignToMe, base_data.build())


def estimate_first_request(base_request, service, rfq_id: str):
    print('estimate_first_request()')
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({'Id': rfq_id})
    call(service.estimate, base_data.build())


def reject_rfq(base_request, service):
    print('reject_rfq()')
    modify_request = ModificationRequest(base=base_request)
    modify_request.reject()
    call(service.modifyAssignedRFQ, modify_request.build())


def verify_assigned_grid_row(base_request, service, case_id, rfq_id):
    base_data = BaseTableDataRequest(base=base_request)

    base_data.set_row_number(1)
    base_data.set_filter_dict({"Id": rfq_id['dealerIntervention.Id']})

    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_request.set_extraction_id("ExtractionId")
    extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.Status", "Status"),
                                               ExtractionDetail("dealerIntervention.QuoteStatus", "QuoteStatus")])

    response = call(service.getAssignedRFQDetails, extraction_request.build())
    print(response)
    ver = Ver(case_id)
    ver.set_event_name("Check Assigned Grid")
    ver.compare_values('Status', "Rejected", response["dealerIntervention.Status"])
    ver.compare_values('QuoteStatus', "", response["dealerIntervention.QuoteStatus"])
    ver.verify()


def check_dmi_disabled(base_request, dmi_service,case_id):
    print('check_dmi_disabled()')
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_request.set_extraction_id("ExtractionId")
    dmi_rfq = 'rfqDetails'
    extraction_request.extract_is_bid_price_pips_enabled(f'{dmi_rfq}.is_bid_price_pips_enabled')
    extraction_request.extract_is_ask_price_pips_enabled(f'{dmi_rfq}.is_ask_price_pips_enabled')
    extraction_request.extract_is_price_spread_enabled(f'{dmi_rfq}.is_price_spread_enabled')
    extraction_request.extract_is_bid_price_large_enabled(f'{dmi_rfq}.is_bid_price_large_enabled')
    extraction_request.extract_is_ask_price_large_enabled(f'{dmi_rfq}.is_ask_price_large_enabled')

    result = call(dmi_service.getRFQDetails, extraction_request.build())

    ver = Verifier(case_id)
    ver.set_event_name("Check is DMI panel Enabled ")
    for key,value in result.items():
        ver.compare_values(key[len(dmi_rfq)+1:], value, 'False')
    ver.verify()

def check_dmi_enabled(base_request, dmi_service,case_id):
    print('check_dmi_enabled()')
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_request.set_extraction_id("ExtractionId")
    dmi_rfq = 'rfqDetails'
    extraction_request.extract_is_bid_price_pips_enabled(f'{dmi_rfq}.is_bid_price_pips_enabled')
    extraction_request.extract_is_ask_price_pips_enabled(f'{dmi_rfq}.is_ask_price_pips_enabled')
    extraction_request.extract_is_price_spread_enabled(f'{dmi_rfq}.is_price_spread_enabled')
    extraction_request.extract_is_bid_price_large_enabled(f'{dmi_rfq}.is_bid_price_large_enabled')
    extraction_request.extract_is_ask_price_large_enabled(f'{dmi_rfq}.is_ask_price_large_enabled')

    result = call(dmi_service.getRFQDetails, extraction_request.build())

    ver = Verifier(case_id)
    ver.set_event_name("Check is DMI panel Disabled ")
    for key, value in result.items():
        ver.compare_values(key[len(dmi_rfq)+1:], value, 'True')
    ver.verify()


def clear_dmi_filters(base_request, dmi_service):
    print('clear_dmi_filters()')
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_row_number(1)
    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_request.set_clear_flag()
    call(dmi_service.getAssignedRFQDetails, extraction_request.build())
    call(dmi_service.getUnassignedRFQDetails, extraction_request.build())


def execute(report_id, case_params, session_id):
    # region Preparation
    case_name = Path(__file__).name[:-3]
    print(f'{case_name} started')
    case_id = bca.create_event(case_name, report_id)
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    seconds, nanos = bca.timestamps()  # Store case start time
    dmi_service = Stubs.win_act_dealer_intervention_service
    ttl = 180
    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': 'GBP/USD',
            'SecurityType': 'FXSWAP',
            'Product': '4',
            },
        'SettlDate': tsd.spo(),
        'SettlType': '0',
        'OrderQty': '25010000'
        }
    # endregion
    try:
        send_swap_rfq(reusable_params, case_params, case_id, fix_act,
                      ttl,
                      int(reusable_params['OrderQty']),
                      int(reusable_params['OrderQty'])+ 1000000)

        rfq_id = extract_unassigned_grid(base_request, dmi_service, reusable_params['OrderQty'])

        assign_firs_request(base_request, dmi_service, rfq_id)

        estimate_first_request(base_request, dmi_service, rfq_id)

        check_dmi_enabled(base_request, dmi_service,case_id)

        reject_rfq(base_request, dmi_service)

        check_dmi_disabled(base_request, dmi_service,case_id)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    finally:
        try:
            clear_dmi_filters(base_request, dmi_service)
        except Exception:
            logging.error("Error execution", exc_info=True)

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
