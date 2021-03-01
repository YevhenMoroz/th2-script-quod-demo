from datetime import datetime
from logging import getLogger, INFO

from custom.basic_custom_actions import timestamps, create_event
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import RFQExtractionDetailsRequest
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call
from win_gui_modules.wrappers import *

logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "Get RFQ details example"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
    username = Stubs.custom_config['qf_trading_fe_user_303']
    password = Stubs.custom_config['qf_trading_fe_password_303']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)

    try:
        service = Stubs.win_act_dealer_intervention_service

        extraction_request = RFQExtractionDetailsRequest(base=base_request)
        extraction_request.set_extraction_id("ExtractionId")
        extraction_request.extract_quote_ttl("rfqDetails.quoteTTL")
        extraction_request.extract_price_spread("rfqDetails.priceSpread")
        extraction_request.extract_ask_price_large("rfqDetails.askPriceLarge")
        extraction_request.extract_bid_price_large("rfqDetails.bidPriceLarge")
        extraction_request.extract_ask_price_pips("rfqDetails.askPricePips")
        extraction_request.extract_bid_price_pips("rfqDetails.bidPricePips")
        extraction_request.extract_near_leg_quantity("rfqDetails.nerLegQty")
        # extraction_request.extract_far_leg_quantity("rfqDetails.farLegQty")
        extraction_request.extract_request_state("rfqDetails.requestState")
        extraction_request.extract_request_side("rfqDetails.requestSide")

        call(service.getRFQDetails, extraction_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
