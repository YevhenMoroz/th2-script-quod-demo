import logging
import random
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, ActionsRatesTile,\
                                                      PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
    ModifyOrderDetails, ModifyFXOrderDetails, ReleaseFXOrderDetails
from win_gui_modules.order_ticket import FXOrderDetails, OrderTicketDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base
from win_gui_modules.client_pricing_wrappers import (SelectRowsRequest, DeselectRowsRequest, ExtractRatesTileValues,
                                                     PlaceRateTileTableOrderRequest, RatesTileTableOrdSide,
                                                     ExtractRatesTileTableValuesRequest)


class CheckClass:
    def __init__(self, _base_request, _service, _init_pips, _init_stop_price,
                 _mod_pips, _mod_stop_price, _tick_size, _click_value, _case_id, _event_name):
        self.base_request = _base_request
        self.service = _service
        self.init_pips = _init_pips
        self.init_stop_price = _init_stop_price
        self.mod_pips = _mod_pips
        self.mod_stop_price = _mod_stop_price
        self.tick_size = _tick_size
        self.click_value = _click_value
        self.case_id = _case_id
        self.event_name = _event_name


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_order_ticket(base_request, service, click_value):
    order_ticket = FXOrderDetails()
    order_ticket.click_pips(click_value)
    order_ticket.click_stop_price(click_value)
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def extract_prices_from_ot(base_request, service):
    order_ticket = ExtractFxOrderTicketValuesRequest(base_request)
    order_ticket.get_price_pips("orderTicket.Pips")
    order_ticket.get_price_large('orderTicket.Large')
    order_ticket.get_stop_price('orderTicket.StopPrice')
    response = call(service.extractFxOrderTicketValues, order_ticket.build())
    return [response['orderTicket.Large'], response['orderTicket.Pips'], response['orderTicket.StopPrice']]


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def place_esp_by_bid_btn(base_request):
    service = Stubs.win_act_aggregated_rates_service
    btd = BaseTileDetails(base=base_request)
    rfq_request = PlaceESPOrder(details=btd)
    rfq_request.set_action(ESPTileOrderSide.BUY)
    rfq_request.top_of_book(False)
    call(service.placeESPOrder, rfq_request.build())


def open_direct_venue(base_request, service, venue):
    modify_request = ModifyRatesTileRequest(details=base_request)
    venue_filter = ContextActionRatesTile.create_venue_filter(venue)
    add_dve_action = ContextActionRatesTile.open_direct_venue_panel()
    modify_request.add_context_actions([venue_filter, add_dve_action])
    call(service.modifyRatesTile, modify_request.build())


def click_on_venue(base_request, service, venue):
    modify_request = ModifyRatesTileRequest(details=base_request)
    click_to_venue = ActionsRatesTile.click_to_ask_esp_order(venue)
    modify_request.add_action(click_to_venue)
    call(service.modifyRatesTile, modify_request.build())


def check_ot_prices(check_class: CheckClass, precision):
    format_str = '{value:.'+precision+'f}'  # Amount of symbols in decimal part
    verifier = Verifier(check_class.case_id)
    verifier.set_event_name(check_class.event_name)
    verifier.compare_values('Check Pips difference (should be equal to ticksize*clicks amount)',
                            format_str.format(value=(float(check_class.click_value) * float(check_class.tick_size))),
                            format_str.format(value=(float(check_class.mod_pips)-float(check_class.init_pips))))

    verifier.compare_values('Check Stop Price difference (should be equal to ticksize*clicks amount)',
                            format_str.format(value=(float(check_class.click_value) * float(check_class.tick_size))),
                            format_str.format(value=(float(check_class.mod_stop_price))))
    verifier.verify()
    order_ticket = FXOrderDetails()
    order_ticket.set_close(True)
    new_order_details = NewFxOrderDetails(check_class.base_request, order_ticket)
    call(check_class.service.placeFxOrder, new_order_details.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    order_ticket_service = Stubs.win_act_order_ticket_fx
    ar_service = Stubs.win_act_aggregated_rates_service

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_data = BaseTileData(base=case_base_request)

    from_curr = "GBP"
    to_curr = "USD"
    tenor_spot = "Spot"
    tenor_1w = "1W"
    venue_gs = 'GS'
    spot_tick_size = 0.00001
    w1_tick_size = 0.0000001
    w1_gs_tick_size = 0.00001
    precision_spot = '5'
    precision_1w = '7'
    precision_gs = '5'
    click_value = 5
    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor_spot)
        place_esp_by_bid_btn(case_base_request)
        pips_and_stop_price = extract_prices_from_ot(base_data, order_ticket_service)
        modify_order_ticket(case_base_request, order_ticket_service, click_value)
        modified_pips_and_stop_price = extract_prices_from_ot(base_data, order_ticket_service)
        check_class = CheckClass(
            _base_request=case_base_request,
            _service=order_ticket_service,
            _init_pips=f'{pips_and_stop_price[0]}{pips_and_stop_price[1]}',
            _init_stop_price=pips_and_stop_price[2],
            _mod_pips=f'{modified_pips_and_stop_price[0]}{modified_pips_and_stop_price[1]}',
            _mod_stop_price=modified_pips_and_stop_price[2],
            _tick_size=spot_tick_size,
            _click_value=click_value,
            _case_id=case_id,
            _event_name=f'Checking Pips and Stop Price After {click_value} click increment (Spot)'
        )

        check_ot_prices(check_class, precision_spot)

        # Step 2
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor_1w)
        place_esp_by_bid_btn(case_base_request)
        pips_and_stop_price = extract_prices_from_ot(base_data, order_ticket_service)
        modify_order_ticket(case_base_request, order_ticket_service, click_value)
        modified_pips_and_stop_price = extract_prices_from_ot(base_data, order_ticket_service)
        check_class = CheckClass(
            _base_request=case_base_request,
            _service=order_ticket_service,
            _init_pips=f'{pips_and_stop_price[0]}{pips_and_stop_price[1]}',
            _init_stop_price=pips_and_stop_price[2],
            _mod_pips=f'{modified_pips_and_stop_price[0]}{modified_pips_and_stop_price[1]}',
            _mod_stop_price=modified_pips_and_stop_price[2],
            _tick_size=w1_tick_size,
            _click_value=click_value,
            _case_id=case_id,
            _event_name=f'Checking Pips and Stop Price After {click_value} click increment (1W)'
        )
        check_ot_prices(check_class, precision_1w)

        # Step 3
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor_1w)
        open_direct_venue(base_esp_details, ar_service, venue_gs)
        click_on_venue(base_esp_details, ar_service, venue_gs)
        pips_and_stop_price = extract_prices_from_ot(base_data, order_ticket_service)
        modify_order_ticket(case_base_request, order_ticket_service, click_value)
        modified_pips_and_stop_price = extract_prices_from_ot(base_data, order_ticket_service)
        check_class = CheckClass(
            _base_request=case_base_request,
            _service=order_ticket_service,
            _init_pips=f'{pips_and_stop_price[0]}{pips_and_stop_price[1]}',
            _init_stop_price=pips_and_stop_price[2],
            _mod_pips=f'{modified_pips_and_stop_price[0]}{modified_pips_and_stop_price[1]}',
            _mod_stop_price=modified_pips_and_stop_price[2],
            _tick_size=w1_gs_tick_size,
            _click_value=click_value,
            _case_id=case_id,
            _event_name=f'Checking Pips and Stop Price After {click_value} click increment (1W GS Venue)'
        )
        check_ot_prices(check_class, precision_gs)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
