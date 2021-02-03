import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs

from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call
from win_gui_modules.wrappers import set_base
from win_gui_modules.rfq_wrappers import RFQTileDetails, RFQTileOrderDetails, RFQTileOrderSide, RFQTilePanelDetails

import rule_management as rm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):

    # Rules
    rule_manager = rm.RuleManager()
    RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-585"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    rfq_service = Stubs.win_act_rfq_service

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    try:
        details = RFQTileDetails(base=base_request)
        details.set_from_currency("EUR")
        details.set_to_currency("USD")
        details.set_settlement_date(bca.get_t_plus_date(2))
        details.set_near_tenor("Spot")
        call(rfq_service.createRFQ, details.request())

        details = RFQTileOrderDetails(base=base_request)
        details.set_venue("HSB")
        details.set_action(RFQTileOrderSide.BUY)
        call(rfq_service.sendRFQOrder, details.request())

        details = RFQTilePanelDetails(base=base_request)
        call(rfq_service.cancelRFQ, details.request())

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    for rule in [RFQ, TRFQ]:
        rule_manager.remove_rule(rule)

    close_fe_2(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
