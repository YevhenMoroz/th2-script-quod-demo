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
    modify_request.set_change_instrument(False)
    modify_request.set_quantity(qty)
    modify_request.set_change_qty(True)
    modify_request.set_tenor("1W")
    modify_request.set_click_on_one_click_button()
    # action = []
    # action.append(ContextActionRatesTile.create_button_click('Statistics'))
    # modify_request.add_context_actions(action)
    call(service.modifyRatesTile, modify_request.build())


def get_my_orders_details(ob_act, base_request, order_id):
    extraction_id = "order.care"
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(extraction_id)
    # main_order_details.set_filter(["Order ID", order_id])
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.orderid", "Order ID")
    ob_lookup = ExtractionDetail("orderBook.lookup", "Lookup")
    ob_creat_time = ExtractionDetail("orderBook.creattime", "CreatTime")
    # ob_id = ExtractionDetail("orderBook.quoteid", "QuoteID")
    # ob_tenor = ExtractionDetail("orderBook.nearlegtenor", "Near Leg Tenor")
    main_order_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts,
                                                                                 ob_lookup,
                                                                                 ob_creat_time])))

    result = call(ob_act.getMyOrdersDetails, main_order_details.request())
    print(result)
    print(result[ob_instr_type.name])



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
    base_request = get_base_request(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    base_rfq_details = BaseTileDetails(base=base_request)
    base_esp_details = BaseTileDetails(base=base_request)

    order_id = "MO1210310103937245001"

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # ESP tile ↓
        # create_or_get_rates_tile(base_rfq_details, ar_service)
        # modify_rates_tile(base_esp_details, ar_service, 'GBP', 'USD', 1000000, case_venue)

        # My Orders ↓

        get_my_orders_details(ob_act,  base_request, order_id)
        # close_fe_2(case_id, session_id)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    print('end time = ' + str(datetime.now()))
    # for rule in [RFQ, TRFQ]:
    #     rule_manager.remove_rule(rule)
