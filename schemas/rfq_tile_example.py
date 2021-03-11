import logging
from datetime import datetime

import rule_management as rm
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, \
    ModifyRFQTileRequest, TableActionsRequest, TableAction, PlaceRFQRequest, ExtractRFQTileValues, \
    ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call
from win_gui_modules.wrappers import set_base

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
    ar_service = Stubs.win_act_aggregated_rates_service

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    try:
        # create rfq tile order
        base_details = BaseTileDetails(base=base_request)
        call(ar_service.createRFQTile, base_details.build())

        # maximize aggregated rates window
        call(ar_service.maximizeWindow, base_request)

        # modify rfq order
        modify_request = ModifyRFQTileRequest(details=base_details)
        modify_request.set_quantity(123)
        modify_request.set_from_currency("EUR")
        modify_request.set_to_currency("USD")
        modify_request.set_near_tenor("Spot")
        modify_request.set_far_leg_tenor("1W")
        modify_request.set_change_currency(True)
        modify_request.set_settlement_date(bca.get_t_plus_date(2))
        modify_request.set_far_leg_settlement_date(bca.get_t_plus_date(5))

        # add context action
        action = ContextAction.create_venue_filters(["HSB", "MGS"])
        modify_request.add_context_action(action)
        # or
        # action = ContextAction.create_venue_filter("HSB")
        # action1 = ContextAction.create_venue_filter("MGS")
        # modify_request.add_context_actions([action, action1])

        # context button click
        # click_action = ContextAction.create_button_click("Quotes")
        # modify_request.add_context_action(click_action)

        call(ar_service.modifyRFQTile, modify_request.build())

        # extracting rfq value
        extract_values_request = ExtractRFQTileValues(details=base_details)
        extract_values_request.extract_near_leg_tenor("aggrRfqTile.tenor")
        extract_values_request.extract_currency("aggrRfqTile.currency")
        extract_values_request.extract_quantity("aggrRfqTile.qty")
        extract_values_request.extract_currency_pair("aggrRfqTile.currencyPair")
        extract_values_request.extract_far_leg_tenor("aggrRfqTile.farLegTenor")
        extract_values_request.extract_near_settlement_date("aggrRfqTile.nearSettlement")
        extract_values_request.extract_far_leg_settlement_data("aggrRfqTile.farLegSettlement")
        call(ar_service.extractRFQTileValues, extract_values_request.build())

        # check venues in table, could be used with verify action
        table_actions_request = TableActionsRequest(details=base_details)
        check1 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.hsbVenue", "HSB"))
        check2 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.mgsVenue", "MGS"))
        table_actions_request.set_extraction_id("extrId")
        table_actions_request.add_actions([check1, check2])
        call(ar_service.processTableActions, table_actions_request.build())

        # send rfq tile
        call(ar_service.sendRFQOrder, base_details.build())

        # place rfq tile
        rfq_request = PlaceRFQRequest(details=base_details)
        # rfq_request.set_venue("VENUE")
        rfq_request.set_action(RFQTileOrderSide.BUY)
        # call(ar_service.placeRFQOrder, rfq_request.build())

        # cancel rfq tile
        call(ar_service.cancelRFQ, base_details.build())

        # minimize aggregated rates window
        call(ar_service.minimizeWindow, base_request)

        # close aggregated rates window
        call(ar_service.closeWindow, base_request)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    for rule in [RFQ, TRFQ]:
        rule_manager.remove_rule(rule)

    close_fe_2(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
