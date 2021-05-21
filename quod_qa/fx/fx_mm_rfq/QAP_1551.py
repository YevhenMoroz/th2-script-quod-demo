import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from custom.tenor_settlement_date import get_expire_time
from custom.verifier import Verifier as Ver
from quod_qa.fx.default_params_fx import text_messages
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import (BaseTableDataRequest, ModificationRequest,
                                                          ExtractionDetailsRequest)
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import prepare_fe_2, get_opened_fe, set_session_id, get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, case_params):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    act = Stubs.fix_act
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    seconds, nanos = bca.timestamps()  # Store case start time
    service = Stubs.win_act_dealer_intervention_service
    ttl = 120
    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
            },
        'SettlDate': tsd.spo(),
        'SettlType': '0',
        'OrderQty': '25000000'
        }

    try:

        # region send rfq
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

        act.sendMessage(
                bca.convert_to_request(
                        text_messages['sendQR'],
                        case_params['TraderConnectivity'],
                        case_id,
                        bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                        ))
        # endregion

        # region  prepeare fe
        Stubs.frontend_is_open = True
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
            # ,
            #          fe_dir='qf_trading_fe_folder_308',
            #          fe_user='qf_trading_fe_user_308',
            #          fe_pass='qf_trading_fe_password_308')
        else:
            get_opened_fe(case_id, session_id)
        # #endregion

        # region Extract RFQ ID
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_filter_dict({"Status": "New"})
        base_data.set_row_number(1)

        extraction_request = ExtractionDetailsRequest(base_data)
        extraction_request.set_extraction_id("ExtractionId")
        extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.Id", "Id")])

        rfq_id = call(service.getUnassignedRFQDetails, extraction_request.build())
        # clear filter for next tests
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_filter_dict({"Status": ""})
        call(service.getUnassignedRFQDetails, extraction_request.build())
        # endregion

        # region Assign to me rfq
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_filter_dict({"Id": rfq_id['dealerIntervention.Id']})
        base_data.set_row_number(1)

        call(service.assignToMe, base_data.build())
        # endregion

        # region Check Assigned Grid
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_filter_dict({"Id": rfq_id['dealerIntervention.Id']})
        base_data.set_row_number(1)

        extraction_request = ExtractionDetailsRequest(base_data)
        extraction_request.set_extraction_id("ExtractionId")
        extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.Status", "Status")])

        response = call(service.getAssignedRFQDetails, extraction_request.build())
        ver = Ver(case_id)
        ver.set_event_name("Check Assigned Grid")
        ver.compare_values('Status', "New", response["dealerIntervention.Status"])
        ver.verify()
        # endregion

        # region unassigned rfq
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_row_number(1)

        call(service.unAssign, base_data.build())
        # #endregion

        # region Checking unassigned Grid
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_row_number(1)

        extraction_request = ExtractionDetailsRequest(base_data)
        extraction_request.set_extraction_id("ExtractionId")
        extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.Id", "Id")])

        call(service.getUnassignedRFQDetails, extraction_request.build())
        # endregion

        # region Assign to me rfq
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_row_number(1)

        call(service.assignToMe, base_data.build())
        # endregion

        # region Check Assigned Grid
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_filter_dict({"Id": rfq_id['dealerIntervention.Id']})
        base_data.set_row_number(1)

        extraction_request = ExtractionDetailsRequest(base_data)
        extraction_request.set_extraction_id("ExtractionId")
        extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.Status", "Status")])

        response = call(service.getAssignedRFQDetails, extraction_request.build())
        ver = Ver(case_id)
        ver.set_event_name("Check Assigned Grid")
        ver.compare_values('Status', "New", response["dealerIntervention.Status"])
        ver.verify()
        # endregion

        # TODO: add filter cleaner
        # region Clear Filters
        # endregion


    except Exception as e:
        logging.error("Error execution", exc_info=True)



    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
