import logging
from datetime import datetime
import rule_management as rm
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import (RFQTileOrderSide, PlaceRFQRequest, ModifyRatesTileRequest,
                                                       ContextActionRatesTile, ModifyRFQTileRequest, ContextAction)
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, cur1, cur2, qty, venue):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_change_instrument(True)
    modify_request.set_quantity(qty)
    modify_request.set_change_qty(True)
    context_action = ContextActionRatesTile()
    context_action.create_venue_filter(venue)
    modify_request.add_context_action(context_action)
    call(service.modifyRatesTile, modify_request.build())





def execute(report_id):
    print('start time = ' + str(datetime.now()))
    common_act = Stubs.win_act

    # Rules
    rule_manager = rm.RuleManager()
    # RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    # TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    # print_active_rules()
    case_name = "kbrit_ui_tests"
    quote_owner = "kbrit"
    case_instr_type = "Spot"
    case_venue = "HSB"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    base_rfq_details = BaseTileDetails(base=case_base_request)
    base_esp_details = BaseTileDetails(base=case_base_request)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # modify rfq order
        # modify_request = ModifyRFQTileRequest()
        # modify_request.set_quantity(123)
        # modify_request.set_from_currency("EUR")
        # modify_request.set_to_currency("USD")
        # modify_request.set_near_tenor("Spot")
        # modify_request.set_far_leg_tenor("1W")
        # modify_request.set_change_currency(True)
        # # add context action
        # action = ContextAction.create_venue_filters(["HSB", "MGS"])
        # modify_request.add_context_action(action)
        # # or
        # # action = ContextAction.create_venue_filter("HSB")
        # # action1 = ContextAction.create_venue_filter("MGS")
        # # modify_request.add_context_actions([action, action1])
        #
        # # context button click
        # click_action = ContextAction.create_button_click("Quotes")
        # modify_request.add_context_action(click_action)
        #
        # call(ar_service.modifyRFQTile, modify_request.build())
        #

        create_or_get_rates_tile(base_rfq_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, 'GBP', 'USD', 1000000, case_venue)

        # close_fe_2(case_id, session_id)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    print('end time = ' + str(datetime.now()))
    # for rule in [RFQ, TRFQ]:
    #     rule_manager.remove_rule(rule)
