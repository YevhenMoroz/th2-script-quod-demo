import logging
from datetime import datetime
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from th2_grpc_act_gui_quod.fx_dealing_positions_pb2 import ExtractionPositionsAction

import rule_management as rm
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import (RFQTileOrderSide, PlaceRFQRequest,
                                                       ContextActionRatesTile, PlaceESPOrder, ESPTileOrderSide,
                                                       ModifyRatesTileRequest, ContextAction, ActionsRatesTile,
                                                       ModifyRFQTileRequest, ContextActionType, ExtractRFQTileValues)
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, PositionsInfo, \
    ExtractionPositionsFieldsDetails, ExtractionPositionsAction, FilterPositionsDetails
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues, \
    ExtractRatesTileTableValuesRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest, \
    ExtractOrderTicketValuesRequest, ExtractOrderTicketErrorsRequest
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def place_order(base_request, service):
    rfq_request = PlaceESPOrder(details=base_request)
    rfq_request.set_action(ESPTileOrderSide.BUY)
    rfq_request.set_action(ESPTileOrderSide.SELL)
    call(service.placeESPOrder, rfq_request.build())


def modify_direct_venue(base_request, service, venue, quantity):
    modify_request = ModifyRatesTileRequest(details=base_request)

    #    context_action0 = ContextActionRatesTile().open_direct_venue_panel()
    #    context_action2 = ContextActionRatesTile().click_to_ask_esp_order(venue)
    #    context_action2 = ContextActionRatesTile().click_to_bid_esp_order(venue)
    #    context_action1 = ContextActionRatesTile().create_button_click('Resting Orders')
    #    context_action2 = ActionsRatesTile().click_to_bid_esp_order(venue)
    #    context_action4 = ActionsRatesTile().click_to_ask_esp_order_by_quantity(venue, quantity)
    #    context_action3 = ActionsRatesTile().click_to_ask_esp_order(venue)
    #   context_action4 = ActionsRatesTile().click_to_ask_esp_order_by_quantity(venue, quantity)
    #    context_action5 = ActionsRatesTile().click_to_bid_esp_order_by_quantity(venue, quantity)
    context_action6 = ActionsRatesTile().click_to_direct_venue_add_raw(venue)
    context_action7 = ActionsRatesTile().click_to_direct_venue_remove_raw(venue)
    context_action8 = ActionsRatesTile().click_to_resting_orders_checkbox()
    #    modify_request.add_context_actions([context_action1])
    modify_request.add_actions([context_action6, context_action7, context_action8])
    call(service.modifyRatesTile, modify_request.build())


def modify_order(base_request, service, qty, cur1, cur2, tenor, far_tenor, date):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_quantity_as_string(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_far_leg_tenor(far_tenor)
    modify_request.set_far_leg_quantity_as_string(qty)
    modify_request.set_settlement_date(bca.get_t_plus_date(date))
    modify_request.set_far_leg_settlement_date(bca.get_t_plus_date(date))
    modify_request.set_maturity_date(bca.get_t_plus_date(date))
    modify_request.set_far_maturity_date(bca.get_t_plus_date(date))
    # modify_request.clear_quantity(True)
    # modify_request.clear_far_leg_tenor(True)
    call(service.modifyRFQTile, modify_request.build())
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.extract_near_settlement_date("aggrRfqTile.date1")
    extract_value.extract_near_maturity_date("aggrRfqTile.date2")
    extract_value.extract_far_maturity_date("aggrRfqTile.date3")
    extract_value.extract_far_leg_qty("aggrRfqTile.far_leg_qty")
    response = call(service.extractRFQTileValues, extract_value.build())
    print(response)


# def modify_rates_tile(base_request, service, cur1, cur2, qty, quantity, tenor, date):
#     modify_request = ModifyRatesTileRequest(details=base_request)
#     # modify_request.set_from_currency(cur1)
#     # modify_request.set_to_currency(cur2)
#     # modify_request.set_quantity(qty)
#     modify_request.set_instrument(True, cur1, cur2, tenor)
#     modify_request.set_quantity_(True, quantity)
#     modify_request.set_settlement_date(bca.get_t_plus_date(date))
#     modify_request.clear_settlement_date(True)

    # context_action = ContextActionRatesTile().create_venue_filter(venue)
    # context_action2 = ContextActionRatesTile().open_direct_venue_panel()
    # context_action4 = ContextActionRatesTile().filter_full_amount_venues([venue])
    # context_action3 = ContextActionRatesTile().add_full_amount_qty('125')
    # context_action5 = ContextActionRatesTile().filter_top_of_book_venue(venue)
    # context_action0 = ContextActionRatesTile().add_context_action_type(
    #     [ContextActionType.CHECK_EMPTY_TOP_OF_BOOK_MARGINS.value,
    #      ContextActionType.CHECK_VWAP.value,
    #      ContextActionType.CHECK_AGGREGATED_RATES.value,
    #      ContextActionType.CHECK_CUMULATIVE_TOP_OF_BOOK_MARGINS.value,
    #      ContextActionType.CHECK_FULL_AMOUNT.value,
    #      ContextActionType.CHECK_EXCLUDE_UNHEALTHY_VENUES.value,
    #      ContextActionType.CHECK_AGGREGATED_TOP_OF_BOOK.value,
    #      ], details=base_request)
    # # modify_request.add_context_action(context_action0)
    # # modify_request.add_context_action(context_action2)
    # modify_request.add_context_action(context_action4)
    # modify_request.add_context_action(context_action3)
    # # modify_request.add_context_action(context_action)
    # modify_request.add_context_action(context_action5)

    # call(service.modifyRatesTile, modify_request.build())


def modify_rates_tile(base_request, service, instrument, client, pips):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    modify_request.set_pips(pips)
    modify_request.toggle_tiered()
    modify_request.toggle_sweepable()
    call(service.modifyRatesTile, modify_request.build())


def set_fx_order_ticket_value(base_request, order_ticket_service):
    """
    Method just set values( don't close the window)
    """
    order_ticket = FXOrderDetails()
    order_ticket.set_price_large('1.23')
    order_ticket.set_price_pips('456')
    order_ticket.set_qty('1150000')
    order_ticket.set_display_qty('666')
    # order_ticket.set_client('FIXCLIENT3')
    # order_ticket.set_tif('Day')
    # order_ticket.set_slippage('2.5')
    # order_ticket.set_order_type('Limit')
    # order_ticket.set_stop_price('1.3')
    order_ticket.set_pending()
    order_ticket.set_keep_open()
    order_ticket.set_custom_algo_check_box()
    # order_ticket.set_custom_algo("Quod TWAP")
    # order_ticket.set_strategy("TWAPBROKER")

    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(order_ticket_service.placeFxOrder, new_order_details.build())


def place_fx_order(base_request):
    """
    Method demonstrate how work settign valuese to FX Order ticket.
    And then set the details to NewFxOrderDetails object with base_request object.

    You should use FXOrderDetails object to define valused that should be set.
    You may set from 1 to all available fields.
    You should use only dot for separation of numbers with floating point
    """
    order_ticket = FXOrderDetails()
    order_ticket.set_price_large('1.23')
    order_ticket.set_price_pips('456')
    order_ticket.set_qty('1150000')
    order_ticket.set_display_qty('666')
    order_ticket.set_client('ASPECT_CITI')
    order_ticket.set_tif('Day')
    order_ticket.set_slippage('2.5')
    order_ticket.set_order_type('Limit')
    order_ticket.set_stop_price('1.3')
    order_ticket.set_display_qty('666')
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    # new servise was added
    order_ticket_service = Stubs.win_act_order_ticket_fx
    call(order_ticket_service.placeFxOrder, new_order_details.build())


def extract_order_ticket_values(base_tile_details, order_ticket_service):
    """
    function demonstrate what and how you can extract value from Forex Order Ticket
    """
    request = ExtractFxOrderTicketValuesRequest(base_tile_details)
    ot = "OrderTicket"
    request.get_instrument(f"{ot}.instrument")
    request.get_price_large(f'{ot}.price_large')
    request.get_price_pips(f'{ot}.price_pips')
    request.get_tif(f'{ot}.tif')
    request.get_order_type(f'{ot}.order_type')
    request.get_quantity(f'{ot}.quantity')
    request.get_display_quantity(f'{ot}.DisplayQuantity')
    request.get_slippage(f'{ot}.slippage')
    request.get_stop_price(f'{ot}.stopprice')
    request.get_client(f'{ot}.client')

    result = call(order_ticket_service.extractFxOrderTicketValues, request.build())
    print(result)
    for k in result:
        print(f'{k} = {result[k]}')


def get_dealing_positions_details(exec_id, del_act, base_request):
    filterpos = FilterPositionsDetails()
    filterpos.set_default_params(base_request)
    #    filterpos.expand_positions_by_symbol(True)
    filterpos.set_currency_mode(False)
    filterpos.set_account("CLIENT1_1")
    call(del_act.filterDealingPositions, filterpos.request())

    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    dealing_positions_details.set_extraction_id(exec_id)
    dealing_positions_details.set_filter(["Symbol", "EUR/USD", "Account", "CLIENT1_1"])
    currency = ExtractionPositionsFieldsDetails("dealingpositions.symbol", "Symbol")
    account = ExtractionPositionsFieldsDetails("dealingpositions.account", "Account")
    sub_account = ExtractionPositionsFieldsDetails("sub_positions.account", "Account")
    sub_position = ExtractionPositionsFieldsDetails("sub_positions.account", "Position")
    sub_quote_position = ExtractionPositionsFieldsDetails("sub_position.quote_pos_euro", "Quote Position (USD)")
    sub_settle_date = ExtractionPositionsFieldsDetails("sub_positions.settldate", "Settle Date")
    # dealing_positions_details.add_single_positions_info(
    #          PositionsInfo.create(
    #              action=ExtractionPositionsAction.create_extraction_action(extraction_details=[currency, account])))

    lvl1_info = PositionsInfo.create(
        action=ExtractionPositionsAction.create_extraction_action(
            extraction_details=[sub_account, sub_settle_date, sub_position, sub_quote_position]))

    lvl1_details = GetOrdersDetailsRequest.create(info=lvl1_info)

    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[currency, account]),
            positions_by_currency=lvl1_details))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    print(response)


def extract_aggr_rates_table_data(service, base_request):
    # extract rates tile table values
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extract_table_request.set_extraction_id("ExtractionId1")
    extract_table_request.set_row_number(1)

    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Px", "Px"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Qty", "Qty"))
    # extract_table_request.set_ask_extraction_fields([ExtractionDetail("rateTile.Px", "Px")])
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Px", "Px"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Qty", "Qty"))

    extract_table_request.set_row_number(2)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Px2", "Px"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Qty2", "Qty"))
    # extract_table_request.set_ask_extraction_fields([ExtractionDetail("rateTile.Px", "Px")])
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Px2", "Px"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Qty2", "Qty"))
    # extract_table_request.set_bid_extraction_fields([ExtractionDetail("rateTile.Px", "Px")])

    response=call(service.extractESPAggrRatesTableValues, extract_table_request.build())
    print(response)


def extract_error_message_order_ticket(base_request, order_ticket_service):
        # extract rates tile table values
        extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
        extract_errors_request.extract_error_message()
        result = call(order_ticket_service.extractOrderTicketErrors, extract_errors_request.build())
        print(result)

def get_disclose_flag_state(base_request, order_ticket_service):
        # extract rates tile table values
        extract_disclose_flag_request = ExtractOrderTicketValuesRequest(base_request)
        extract_disclose_flag_request.get_disclose_flag_state()
        result = call(order_ticket_service.extractOrderTicketValues, extract_disclose_flag_request.build())
        print(result)


def execute(report_id):
    print('start time = ' + str(datetime.now()))
    common_act = Stubs.win_act
    del_act = Stubs.act_fx_dealing_positions
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    case_base_request = get_base_request(session_id, case_id)
    base_tile_details = BaseTileData(base=base_request)
    base_details = BaseTileDetails(base=case_base_request)
    cp_service = Stubs.win_act_cp_service
    instrument = "NOK/SEK-SPOT"
    client_tier = "Gold_Night"
    pips = "2"

    # Rules
    rule_manager = rm.RuleManager()
    # RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    # TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    # print_active_rules()
    case_name = "esp_ui_tests"
    quote_owner = "kbrit"
    case_instr_type = "Spot"
    venue = "EBS"
    case_qty = 1000000
    case_near_tenor = "Spot"
    case_far_tenor = "1W"
    case_from_currency = "AUD"
    case_to_currency = "BRL"
    case_client = "ASPECT_CITI"
    case_date = 2
    quantity = "666"
    qty = 999
    cur1 = "EUR"
    cur2 = "USD"
    tenor = "Broken"
    date = 2

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    cp_service = Stubs.win_act_cp_service
    ob_act = Stubs.act_fx_dealing_positions
    order_ticket_fx_service = Stubs.win_act_order_ticket_fx
    order_ticket_service = Stubs.win_act_order_ticket
    base_rfq_details = BaseTileDetails(base=case_base_request)
    base_esp_details = BaseTileDetails(base=case_base_request)

    # region Open FE

    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        #         # region Complete order
        #         act = Stubs.win_act_order_book
        #         complete_order_details = ModifyOrderDetails.set_filter(["Order ID", 'AO1210325105659044001'])
        # #        complete_order_details.set_default_params(base_request)
        # #        complete_order_details.set_filter(["Order ID", 'AO1210325105659044001'])
        #         call(act.completeOrder, complete_order_details.build())
        #         # endregion

    #    create_or_get_rates_tile(base_rfq_details, ar_service)
        #        create_or_get_rfq(base_rfq_details, ar_service)
    #    modify_rates_tile(base_esp_details, ar_service, cur1, cur2, qty, quantity, tenor, date)
    #     create_or_get_rates_tile(base_details, cp_service)
    #    modify_rates_tile(base_details, cp_service, instrument, client_tier, pips)
    #    extract_aggr_rates_table_data(ar_service, base_details)

        # place_fx_order(base_request)
        #set_fx_order_ticket_value(base_request, order_ticket_fx_service)
        # extract_order_ticket_values(base_tile_details, order_ticket_fx_service)
    #    extract_error_message_order_ticket(base_request, order_ticket_service)
        get_disclose_flag_state(base_request, order_ticket_service)
    #   call(cp_service.closeRatesTile, base_rfq_details.build())
    #    call(ar_service.closeRatesTile, base_esp_details.build())

    #        modify_direct_venue(base_esp_details, ar_service, 'FAM', '1')

    #        place_order(base_esp_details, ar_service)

    #      get_dealing_positions_details("123", del_act, base_request)

    #       modify_order(base_rfq_details, ar_service, qty, case_from_currency, case_to_currency, case_near_tenor, case_far_tenor, case_date)
    # close_fe_2(case_id, session_id)

    except Exception as e:
        logging.error("Error execution", exc_info=True)


# print('end time = ' + str(datetime.now()))
# for rule in [RFQ, TRFQ]:
#     rule_manager.remove_rule(rule)
