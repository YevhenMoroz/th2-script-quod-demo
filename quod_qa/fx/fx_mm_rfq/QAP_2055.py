import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
import os
from custom.tenor_settlement_date import get_expire_time
from custom.verifier import Verifier as Ver, Verifier, VerificationMethod
from quod_qa.fx.default_params_fx import text_messages
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import (BaseTableDataRequest, ModificationRequest,
                                                          ExtractionDetailsRequest, RFQExtractionDetailsRequest
                                                          )
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import prepare_fe_2, get_opened_fe, set_session_id, get_base_request, call
from win_gui_modules.wrappers import set_base
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

client = 'Palladium1'
settltype = '0'
symbol = 'EUR/USD'
currency = 'EUR'
securitytype = 'FXSPOT'
securityidsource = '8'
side = '2'
orderqty = '58000000'
securityid = 'EUR/USD'
settldate = tsd.spo()


def extract_from_unassigned(base_request, service, qty, row=1):
    try:
        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_filter_dict({"Status": "New"})
        base_data.set_filter_dict({"Qty": str(qty)})
        base_data.set_row_number(row)

        extraction_request = ExtractionDetailsRequest(base_data)
        extraction_request.set_extraction_id("ExtractionId")
        extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.Id", "Id")])
        extraction_request.add_extraction_details([ExtractionDetail('dealerIntervention.AutomaticQuoting', 'AutomaticQuoting')])
        result = call(service.getUnassignedRFQDetails, extraction_request.build())
        return result
    except Exception:
        logging.error("Error execution", exc_info=True)


def extract_from_quote_request_book(base_request, service, qty, row=1):
    try:
        base_data = QuoteDetailsRequest(base=base_request)
        base_data.set_filter(["Status", "New"])
        base_data.set_filter(["Qty", str(qty)])
        base_data.set_row_number(row)
        base_data.add_extraction_details([ExtractionDetail("quoteRequestBook.Id", "Id")])
        base_data.add_extraction_details([ExtractionDetail('quoteRequestBook.AutomaticQuoting', 'AutomaticQuoting')])
        result = call(service.getQuoteRequestBookDetails, base_data.request())
        return result
    except Exception:
        logging.error("Error execution", exc_info=True)


def verify_results(case_id, di_extraction, qrb_extraction):
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking values from QRB and DI')
    verifier.compare_values(
        'Quote ID',
        str(di_extraction.get('dealerIntervention.Id')),
        str(qrb_extraction.get('quoteRequestBook.Id'))
    )
    verifier.compare_values(
        'QRB AutomaticQuoting',
        'No',
        str(qrb_extraction.get('quoteRequestBook.AutomaticQuoting'))
    )
    verifier.compare_values(
        'DI AutomaticQuoting',
        'No',
        str(di_extraction.get('dealerIntervention.AutomaticQuoting'))
    )
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    di_service = Stubs.win_act_dealer_intervention_service
    ar_service = Stubs.win_act_aggregated_rates_service

    base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=base_request)

    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time

    ttl = 180
    # print(tsd.spo())
    try:

        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)

        # Step 1-2
        params = CaseParamsSellRfq(
            client, case_id, side=side,
            orderqty=orderqty, symbol=symbol, securitytype=securitytype,
            settldate=settldate, settltype=settltype, currency=currency,
        )
        params.prepare_rfq_params()
        FixClientSellRfq(params).send_request_for_quote()
        unassigned_extraction = extract_from_unassigned(base_request, di_service, orderqty)
        qrb_extraction = extract_from_quote_request_book(base_request, ar_service, orderqty)
        # print(f'{unassigned_extraction}\n{qrb_extraction}')
        verify_results(case_id, unassigned_extraction, qrb_extraction)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            pass
        except Exception:
            logging.error("Error execution", exc_info=True)
