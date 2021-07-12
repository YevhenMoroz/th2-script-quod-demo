import logging
from pathlib import Path
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.layout_panel_wrappers import FXConfigsRequest, DefaultFXValues, OptionOrderTicketRequest
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, CalcDataContentsRowSelector
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def place_order(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    esp_request.top_of_book()
    call(service.placeESPOrder, esp_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor, days: int, qty):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    modify_request.set_settlement_date(bca.get_t_plus_date(days))
    modify_request.set_quantity(qty)
    call(service.modifyRatesTile, modify_request.build())
    return bca.get_t_plus_date(days).strftime('%Y/%m/%d')


def click_one_click_button(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_click_on_one_click_button()
    call(service.modifyRatesTile, modify_request.build())


def check_order_book(base_request, act_ob, case_id, tenor, settle_date, qty, ord_type):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Tenor", tenor])
    ob.set_filter(["Settle Date", settle_date])
    ob.set_filter(['Qty', qty])
    ob_tenor = ExtractionDetail("orderBook.Tenor", "Tenor")
    ob_settle_date = ExtractionDetail("orderBook.SettleDate", "Settle Date")
    ob_qty = ExtractionDetail("orderBook.Qty", "Qty")
    ob_order_id = ExtractionDetail('orderBook.OrderID', 'Order ID')
    ob_order_type = ExtractionDetail('orderBook.OrdType', 'OrdType')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_tenor,
                                                                                 ob_order_id,
                                                                                 ob_settle_date,
                                                                                 ob_qty,
                                                                                 ob_order_type
                                                                                 ])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Tenor", tenor, response[ob_tenor.name])
    verifier.compare_values("Settle Date", settle_date, response[ob_settle_date.name])
    verifier.compare_values("Qty", qty, response[ob_qty.name].replace(',', ''))
    verifier.compare_values('Order Type', ord_type, response[ob_order_type.name])
    verifier.verify()

    return response[ob_order_id.name]


def check_trades_book(base_request, ob_act, case_id, ord_id, tenor,  settle_date, ord_type):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(base_request)
    execution_details.set_extraction_id(extraction_id)
    execution_details.set_filter(["Order ID", ord_id])
    execution_details.set_filter(["Settle Date", settle_date])
    trades_order_id = ExtractionDetail("tradeBook.OrderID", "Order ID")
    trades_settle_date = ExtractionDetail("tradeBook.settle_date", "Settle Date")
    trades_tenor = ExtractionDetail('tradeBook.Tenor', 'Tenor')
    trades_ord_type = ExtractionDetail("tradeBook.ordType", "Ord type")
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[trades_order_id,
                                                                                 trades_settle_date,
                                                                                 trades_tenor,
                                                                                 trades_ord_type
                                                                                 ])))
    response = call(ob_act.getTradeBookDetails, execution_details.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Trade Book")
    verifier.compare_values("Order ID", ord_id, response[trades_order_id.name])
    verifier.compare_values("Settle Date", settle_date, response[trades_settle_date.name])
    verifier.compare_values('Tenor', tenor, response[trades_tenor.name])
    verifier.compare_values('Ord Type', ord_type, response[trades_ord_type.name])
    verifier.verify()


def execute(report_id, session_id):
    # Create sub-report for case
    case_name = Path(__file__).name[:-3]
    start = datetime.now()
    print(f'{case_name} start time = {start}')
    case_id = bca.create_event(case_name, report_id)
    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service
    ob_service = Stubs.win_act_order_book

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Broken"

    order_type = "Limit"
    qty = '5000000'

    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        settle_date = modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor, 3, qty)
        click_one_click_button(base_esp_details, ar_service)

        # Step 2
        place_order(base_esp_details, ar_service)

        # Step 3
        ord_id = check_order_book(case_base_request, ob_service, case_id, tenor, settle_date, qty, order_type)
        check_trades_book(case_base_request, ob_service, case_id, ord_id, tenor, settle_date, order_type)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
            print(f'{case_name} duration time = ' + str(datetime.now() - start))
        except Exception:
            logging.error("Error execution", exc_info=True)
