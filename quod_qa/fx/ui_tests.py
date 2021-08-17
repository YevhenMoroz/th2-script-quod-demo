import base64
import logging
from datetime import datetime
from pathlib import Path

from PIL import Image
import pybase64
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from th2_grpc_act_gui_quod.order_book_fx_pb2 import FXOrderInfo

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import (ModifyRatesTileRequest,
                                                       ContextActionRatesTile, ModifyRFQTileRequest,
                                                       TableActionsRequest, TableAction, CellExtractionDetails,
                                                       ExtractRFQTileValues, ExtractRatesTileDataRequest, PlaceESPOrder,
                                                       ESPTileOrderSide)
from win_gui_modules.client_pricing_wrappers import (SelectRowsRequest, DeselectRowsRequest, ExtractRatesTileValues,
                                                     PlaceRateTileTableOrderRequest, RatesTileTableOrdSide,
                                                     ExtractRatesTileTableValuesRequest, GetCPRTPColors,
                                                     ModifyClientRFQTileRequest, ClientRFQTileOrderDetails,
                                                     ExtractRatesTileTableValuesRequest, GetCPRTPColors,
                                                     PlaceRatesTileOrderRequest)
from win_gui_modules.common_wrappers import BaseTileDetails, MoveWindowDetails
from win_gui_modules.dealer_intervention_wrappers import RFQExtractionDetailsRequest, ModificationRequest
from win_gui_modules.layout_panel_wrappers import (WorkspaceModificationRequest, OptionOrderTicketRequest,
                                                   DefaultFXValues, FXConfigsRequest)
from win_gui_modules.order_book_wrappers import (OrdersDetails, FXOrderInfo, OrderInfo as OrdInf, ExtractionDetail,
                                                 ExtractionAction,ModifyFXOrderDetails, CancelFXOrderDetails,
                                                 ReleaseFXOrderDetails, FXOrdersDetails)
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, cur1, cur2, qty, venue):
    print('modify_rates_tile()')
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    # modify_request.set_change_instrument(False)
    modify_request.set_quantity(str(qty))
    # modify_request.set_change_qty(True)
    modify_request.set_tenor("Spot")
    # modify_request.set_click_on_one_click_button()
    action = []
    action.append(ContextActionRatesTile.filter_synthetic_combinations(["Direct", "EUR/USD"]))
    modify_request.add_context_actions(action)
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
            FXOrderInfo.create(
                    action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                         ob_exec_sts,
                                                                                         ob_lookup,
                                                                                         ob_creat_time])))

    result = call(ob_act.getMyOrdersDetails, main_order_details.request())
    print(result)
    print(result[ob_instr_type.name])


def get_trade_book_details(ob_act, base_request, order_id):
    """
    Demonstration of work with Trade book window
    """

    main_order_details = OrdersDetails()
    # to set filter use list with string pairs like ['ColumnName', 'ColumnValue']
    main_order_details.set_filter(["Side", 'Buy',
                                   'Venue', 'QUODFX'])
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("trade.1")
    # to extruct values from first row user str pairs 'UniqID','ColumnNanme'
    ob_instr_type = ExtractionDetail("tradeBook.instrtype", "ExecID")
    ob_exec_sts = ExtractionDetail("tradeBook.orderid", "Venue")
    ob_lookup = ExtractionDetail("tradeBook.lookup", "Qty")
    ob_creat_time = ExtractionDetail("tradeBook.creattime", "CreationTime")
    # use next expression to add extraction  settings before  run grpc call
    main_order_details.add_single_order_info(
            OrdInf.create(
                    action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                         ob_exec_sts,
                                                                                         ob_lookup,
                                                                                         ob_creat_time])))
    # to extract values to a dict use next statement
    result = call(ob_act.getTradeBookDetails, main_order_details.request())
    # you may use loop to check values
    for key, value in result.items():
        print(f'\t {key} = {value}')
    # or single value extraction
    print(result[ob_instr_type.name])


def check_venue(base_details, ar_service):
    table_actions_request = TableActionsRequest(details=base_details)
    check1 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.hsbVenue", "HSB"))
    check2 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.mgsVenue", "MGS"))
    table_actions_request.set_extraction_id("extrId")
    table_actions_request.add_actions([check1, check2])
    result = call(ar_service.processTableActions, table_actions_request.build())
    print(result)


def extract_rfq_table_data(base_details, ar_service):
    """
    It is simple demonstration of hot to cell data extract.
    In example bellow created one TableActionsRequest and 4 cells extracting.
    CellExtractionDetails() use next income position args:
        name - is unique name for cell,
        column_name - is actual column name from FE Trading,
        venue_name - it is the venue short name from FE Trading( used for search correct row),
        int_side - it need for search correct column from same sell/buy cells( SELL=0/BUY=1)

    result - is a dictionary with string values

    """
    table_actions_request = TableActionsRequest(details=base_details)
    extract1 = TableAction.extract_cell_value(CellExtractionDetails("DistSell1", "Dist", "HSB", 0))
    extract2 = TableAction.extract_cell_value(CellExtractionDetails("PtsSell1", "Pts", "HSB", 0))
    extract3 = TableAction.extract_cell_value(CellExtractionDetails("PtsBuy1", "Pts", "HSB", 1))
    extract4 = TableAction.extract_cell_value(CellExtractionDetails("DistBuy1", "Dist", "HSB", 1))
    # There is two way of headers extraction
    # 1 is use list of colIndexes to extruct custom header(if you know what you want) !!!warning indexes start from 1!!!
    # extract5 = TableAction.extract_headers(colIndexes=(3,4,9,10))
    # 2 you may use empty list to extract all available headers
    extract5 = TableAction.extract_headers(colIndexes=())
    table_actions_request.set_extraction_id("extrId")
    table_actions_request.add_actions([extract5])
    result = call(ar_service.processTableActions, table_actions_request.build())
    print(result)
    for s in result['Headers'].split(';'):
        print(s)


def extract_rfq_panel(exec_id, base_request, service):
    """
    Class ExtractRFQTileValues was extended.
    Here bellow you can see all available fx_wrapper.

    param name is common for all extract.. fx_wrapper.
    name it's unique str. It need to extract value from result dict

    """
    extract_value = ExtractRFQTileValues(details=base_request)
    # extract_value.extract_currency_pair("ar_rfq.extract_currency_pair")
    extract_value.extract_send_button_text("ar_rfq.extract_send_button_text")
    # extract_value.extract_left_checkbox("ar_rfq.extract_left_checkbox")
    # extract_value.extract_right_checkbox("ar_rfq.extract_right_checkbox")
    # extract_value.extract_currency("ar_rfq.extract_currency")
    # extract_value.extract_quantity("ar_rfq.extract_quantity")
    # extract_value.extract_tenor("ar_rfq.extract_tenor")
    # extract_value.extract_far_leg_tenor("ar_rfq.extract_far_leg_tenor")
    # extract_value.extract_near_settlement_date("ar_rfq.extract_near_settlement_date")
    # extract_value.extract_far_leg_settlement_date("ar_rfq.extract_far_leg_settlement_date")
    # extract_value.extract_best_bid("ar_rfq.extract_best_bid")
    # extract_value.extract_best_bid_large("ar_rfq.extract_best_bid_large")
    # extract_value.extract_best_bid_small("ar_rfq.extract_best_bid_small")
    # extract_value.extract_best_ask("ar_rfq.extract_best_ask")
    # extract_value.extract_best_ask_large("ar_rfq.extract_best_ask_large")
    # extract_value.extract_best_ask_small("ar_rfq.extract_best_ask_small")
    # extract_value.extract_spread("ar_rfq.extract_spread")
    # extract_value.extract_swap_diff_days("ar_rfq.extract_swap_diff_days")
    # extract_value.extract_beneficiary("ar_rfq.extract_beneficiary")
    # extract_value.extract_client("ar_rfq.extract_client")
    # extract_value.extract_cur_label_right("ar_rfq.extract_label_buy")
    # extract_value.extract_cur_label_left("ar_rfq.extract_label_sell")

    extract_value.set_extraction_id(exec_id)
    response = call(service.extractRFQTileValues, extract_value.build())
    for line in response:
        print(f'{line} = {response[line]}')
    # extract_qty = response["ar_rfq.qty"]
    # verifier = Verifier(case_id)
    # verifier.set_event_name("Verify Qty on RFQ tile")
    # verifier.compare_values("Qty", '10,000,000.00', extract_qty)


def extruct_popup_lists_demo(exec_id, base_request, service):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.extract_near_tenor_list("1")

    extract_value.set_extraction_id(exec_id)
    response = call(service.extractRFQTileValues, extract_value.build())
    for line in response:
        print(f'{line} = {response[line]}')


def modify_rfq_tile(base_request, service):
    modify_request = ModifyRFQTileRequest(details=base_request)
    # modify_request.set_quantity(123)
    # modify_request.set_far_leg_qty(456)
    # modify_request.set_from_currency("EUR")
    # modify_request.set_to_currency("USD")
    # modify_request.set_near_tenor("TOM")
    # modify_request.set_far_leg_tenor("1W")
    # modify_request.set_client('FIXCLIENT3')
    # modify_request.set_change_currency()
    modify_request.click_checkbox_left()
    modify_request.click_checkbox_right()
    call(service.modifyRFQTile, modify_request.build())


def export_layout(base_request, option_service):
    print('export_layout()')
    modification_request = WorkspaceModificationRequest()
    modification_request.set_default_params(base_request=base_request)
    modification_request.set_filename("demo_export_file.xml")
    modification_request.set_path(
            'C:\\Users\\kbrit\\PycharmProjects\\prev_th2-script-quod-demo\\quod_qa\\fx\\fx_taker_rfq')
    modification_request.do_export()

    call(option_service.modifyWorkspace, modification_request.build())


def import_layout(base_request, option_service):
    print('import_layout()')
    modification_request = WorkspaceModificationRequest()
    modification_request.set_default_params(base_request=base_request)
    modification_request.set_filename("demo_export_file.xml")
    modification_request.set_path(
            'C:\\Users\\kbrit\\PycharmProjects\\prev_th2-script-quod-demo\\quod_qa\\fx\\fx_taker_rfq')
    modification_request.do_import()

    call(option_service.modifyWorkspace, modification_request.build())


def set_order_ticket_options(option_service, base_request):
    """
    The method can be used for set Only OrderTicket>DefaultFXValues
        (to add more elements raise a sub-task)
    To  select Option use Panels
    Ex: to select valuese in Options>Order Ticket> DefaultFxValues use DefaultFXValues()

    """

    order_ticket_options = OptionOrderTicketRequest(base=base_request)
    # slippage = CustomCurrencySlippage(instrument='EUR/USD', dmaSlippage='1234.56789', algoSlippage='98765.4321')
    # slippage2 = CustomCurrencySlippage(instrument='GBP/USD', dmaSlippage='1234.56789', algoSlippage='98765.4321')
    # order_qty_increment = OrderQuantityIncrements(quantity='1000000', increment='555')
    # fx_values = DefaultFXValues(custom_currency_slippage_list=[],
    #                             order_quantity_increments_list=[order_qty_increment])
    # fx_values = DefaultFXValues([slippage])
    order_type = "Market"
    # tif = "FillOrKill"
    # strategy_type = "Quod DarkPool"
    # strategy = "PeggedTaker"
    # child_strategy = "BasicTaker"
    # fx_values.AggressiveTIF = "Pegger"
    # fx_values.AggressiveOrderType = order_type
    # fx_values.AggressiveTIF = tif
    # fx_values.AggressiveStrategyType = strategy_type
    # fx_values.AggressiveStrategy = strategy
    # fx_values.AggressiveChildStrategy = child_strategy
    # fx_values.PassiveOrderType = order_type
    # fx_values.PassiveTIF = tif
    # fx_values.PassiveStrategyType = strategy_type
    # fx_values.PassiveStrategy = strategy
    # fx_values.PassiveChildStrategy = child_strategy
    # fx_values.AlgoSlippage = '12367.45'
    # fx_values.DMASlippage = '12678.09'
    # fx_values.Client = "FIXCLIENT4"

    # order_ticket_options.set_default_fx_values(fx_values)
    # call(option_service.setOptionOrderTicket, order_ticket_options.build())


def set_one_click_mod(option_service, base_request):
    """


    """
    fx_configs = FXConfigsRequest(base=base_request)

    fx_configs.set_cumulative_qty('5')
    fx_configs.set_one_click_mode('DoubleClick')
    fx_configs.set_algo_default_qty('5.1')
    fx_configs.set_headers_prices_format('VWAP of Default Quantity')

    call(option_service.setOptionForexConfigs, fx_configs.build())

def check_quote_request_b(base_request, service, case_id, status = "New", quote_status = "Accepted", venue = "HSBCR"):
    qrb = QuoteDetailsRequest(base=base_request)
    qrb.set_extraction_id("set_here_any_random_ID")
    qrb.set_filter(["Venue", venue,"User", "QA3"])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_venue,qrb_status ])
    qrb.add_child_extraction_details([qrb_quote_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())


    print( response)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values('Venue', "HSBCR", response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values('QuoteStatus', quote_status, response[qrb_quote_status.name])
    verifier.verify()


def set_fx_order_ticket_value(base_request, order_ticket_service):
    """
    Method just set values( don't close the window)
    """
    order_ticket = FXOrderDetails()

    order_ticket.set_price_large('1.23')
    # order_ticket.set_price_pips('456')
    # order_ticket.set_qty('1150000')
    # order_ticket.set_client('ASPECT_CITI')
    # order_ticket.set_tif('FillOrKill')
    # order_ticket.set_slippage('2.5')
    # order_ticket.set_order_type('Limit')
    # order_ticket.set_stop_price('1.3')
    order_ticket.click_pips(-3)
    # order_ticket.click_qty(-3)
    # order_ticket.click_slippage(3)
    # order_ticket.click_stop_price(3)
    # order_ticket.set_custom_algo_check_box()
    # order_ticket.set_custom_algo('Quod VWAP')
    # order_ticket.set_strategy('Quod VWAP Default')
    # order_ticket.set_child_strategy('test')
    # order_ticket.set_care_order('QA3 (HeadOfSaleDealer)', True)  # Desk Market Marking FX (CN)
    # order_ticket.set_care_order('Text Aspect Desk of Traders (CN)', False)#Stubs.custom_config['qf_trading_fe_user_desk'], False) # Desk Market Marking FX (CN)

    # strategy = order_ticket.add_multilisting_strategy("Quod MultiListing")
    # strategy.set_allow_missing_trim(True)
    # strategy.set_available_venues(True)
    # strategy.set_allowed_venues('HSBC')
    # strategy.set_forbidden_venues('CITI')
    # strategy.set_fok_exploration(True)
    # strategy.set_available_venues(True)
    # strategy.set_sweeping_allowed(True)
    # strategy.set_post_mode('Single')

    strategy = order_ticket.add_twap_strategy("QUOD TWAP")
    strategy.set_start_date(from_date='Now', offset='1')
    strategy.set_end_date(from_date='CloseTime', offset='2')
    strategy.set_waves('5')
    strategy.set_slice_duration('7')
    strategy.set_reserve_quantity('7')
    strategy.set_allowed_venues("HBCS")
    strategy.set_forbidden_venues("CITI")

    # order_ticket.set_place()
    order_ticket.set_pending()
    # order_ticket.set_keep_open()

    new_order_details = NewFxOrderDetails(base_request, order_ticket, isMM=True)
    call(order_ticket_service.placeFxOrder, new_order_details.build())


def place_fx_order(base_request, order_ticket_service):
    """
    Method demonstrate how work setting values to FX Order ticket.
    And then set the details to NewFxOrderDetails object with base_request object.

    You should use FXOrderDetails object to define values that should be set.
    You may set from 1 to all available fields.
    You should use only dot for separation of numbers with floating point
    """
    order_ticket = FXOrderDetails()
    order_ticket.set_price_large('1.23')
    order_ticket.set_price_pips('456')
    order_ticket.set_qty('1150000')
    order_ticket.set_client('FIXCLIENT3')
    order_ticket.set_tif('Day')
    order_ticket.set_slippage('2.5')
    order_ticket.set_order_type('Limit')
    order_ticket.set_stop_price('1.3')
    order_ticket.set_place()

    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    # new servise was added
    order_ticket_service = Stubs.win_act_order_ticket_fx
    call(order_ticket_service.placeFxOrder, new_order_details.build())


def close_fx_order(base_request, order_ticket_service):
    """

    """
    order_ticket = FXOrderDetails()
    order_ticket.set_close(True)

    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(order_ticket_service.placeFxOrder, new_order_details.build())


def select_rows(base_tile_details, row_numbers, cp_service):
    """
    To select several rows send tuple or list with numbers [1,2,3].
    WARNING!
    when you send numbers more than 4 test case will scroll up after it select all rows you asked
    """
    request = SelectRowsRequest(base_tile_details)
    request.set_row_numbers(row_numbers)
    call(cp_service.selectRows, request.build())


def deselect_rows(base_tile_details, cp_service):
    """
    The method will deselect all selected rows like Esk button
    """
    request = DeselectRowsRequest(base_tile_details)
    call(cp_service.deselectRows, request.build())


def extract_rates_panel_esp(base_tile_details, ar_service):
    s = 'RatesTile0'
    request = ExtractRatesTileDataRequest(base_tile_details)
    request.set_extraction_id(f'{s}.extraction_id')
    request.extract_instrument(f'{s}.instrument')
    # request.extract_quantity(f'{s}.quantity')
    # request.extract_tenor(f'{s}.tenor')
    # request.extract_best_bid(f'{s}.best_bid')
    # request.extract_best_bid_large(f'{s}.best_bid_large')
    # request.extract_best_bid_small(f'{s}.best_bid_small')
    # request.extract_best_ask(f'{s}.best_ask')
    # request.extract_best_ask_large(f'{s}.best_ask_large')
    # request.extract_best_ask_small(f'{s}.best_ask_small')
    # request.extract_spread(f'{s}.spread')
    # request.extract_instrument(f'{s}.instrument')
    # request.extract_client_tier(f'{s}.client_tier')
    request.extract_1click_btn_text(f'{s}.btn_text')
    request.extract_header_color(f'{s}.header_color') # https://www.color-hex.com/color/b68ab5 to understand is it expected ))

    result = call(ar_service.extractRatesTileValues, request.build())
    print(result)
    for k in result:
        print(f'{k} = {result[k]}')


def extract_order_ticket_values(base_tile_details, order_ticket_service):
    """
    function demonstrate what and how you can extract value from Forex Order Ticket
    """
    print('extract_order_ticket_values()')
    request = ExtractFxOrderTicketValuesRequest(base_tile_details)
    # ot = "fx_order_ticket"
    # request.get_instrument(f"{ot}.instrument")
    # request.get_price_large(f'{ot}.price_large')
    # request.get_price_pips(f'{ot}.price_pips')
    # request.get_tif(f'{ot}.tif')
    # request.get_order_type(f'{ot}.order_type')
    # request.get_quantity(f'{ot}.quantity')
    # request.get_slippage(f'{ot}.slippage')
    # request.get_stop_price(f'{ot}.stopprice')
    # request.get_client(f'{ot}.client')
    # request.get_algo()
    # request.get_strategy()
    # request.get_child_strategy()
    # request.get_is_algo_checked()

    request.get_error_message_text()
    request.get_send_btn_text()
    print('call()')
    result = call(order_ticket_service.extractFxOrderTicketValues, request.build())
    print(result)
    for k in result:
        print(f'{k} = {result[k]}')


def extract_cp_rates_panel(base_tile_details, cp_service):
    values = ExtractRatesTileValues(details=base_tile_details)

    s = 'RatesTile0'
    values.extract_instrument(f'{s}.instrument')
    values.extract_client_tier(f'{s}.client_tier')

    result = call(cp_service.extractRateTileValues, values.build())
    print(result)


def extract_di_panel(base_request, dealer_intervention_service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_request.set_extraction_id("ExtractionId")
    # extraction_request.extract_quote_ttl("rfqDetails.quoteTTL")
    # extraction_request.extract_price_spread("rfqDetails.priceSpread")
    # extraction_request.extract_ask_price_large("rfqDetails.askPriceLarge")
    # extraction_request.extract_bid_price_large("rfqDetails.bidPriceLarge")
    # extraction_request.extract_ask_price_pips("rfqDetails.askPricePips")
    # extraction_request.extract_bid_price_pips("rfqDetails.bidPricePips")
    # extraction_request.extract_near_leg_quantity("rfqDetails.nerLegQty")
    # # extraction_request.extract_far_leg_quantity("rfqDetails.farLegQty")
    # extraction_request.extract_request_state("rfqDetails.requestState")
    # extraction_request.extract_request_side("rfqDetails.requestSide")
    # extraction_request.extract_button_text("rfqDetails.buttonText")
    dmi_rfq = 'rfqDetails'
    # extraction_request.extract_instrument_label_control(f'{dmi_rfq}.instrument_label_control')
    # extraction_request.extract_currency_value_label_control(f'{dmi_rfq}.currency_value_label_control')
    # extraction_request.extract_near_tenor_label(f'{dmi_rfq}.near_tenor_label')
    # extraction_request.extract_far_tenor_label(f'{dmi_rfq}.far_tenor_label')
    # extraction_request.extract_near_settl_date_label(f'{dmi_rfq}.near_settl_date_label')
    # extraction_request.extract_far_settl_date_label(f'{dmi_rfq}.far_settl_date_label')
    # extraction_request.extract_party_value_label_control(f'{dmi_rfq}.party_value_label_control')
    # extraction_request.extract_request_side_value_label_control(f'{dmi_rfq}.request_side_value_label_control')
    # extraction_request.extract_fill_side_value_label_control(f'{dmi_rfq}.fill_side_value_label_control')
    # extraction_request.extract_creation_value_label_control(f'{dmi_rfq}.creation_value_label_control')
    # extraction_request.extract_bid_near_points_value_label(f'{dmi_rfq}.bid_near_points_value_label')
    # extraction_request.extract_bid_far_points_value_label(f'{dmi_rfq}.bid_far_points_value_label')
    # extraction_request.extract_bid_near_price_value_label(f'{dmi_rfq}.bid_near_price_value_label')
    # extraction_request.extract_bid_far_price_value_label(f'{dmi_rfq}.bid_far_price_value_label')
    # extraction_request.extract_bid_value_label(f'{dmi_rfq}.bid_value_label')
    # extraction_request.extract_ask_value_label(f'{dmi_rfq}.ask_value_label')
    # extraction_request.extract_ask_near_points_value_label(f'{dmi_rfq}.ask_near_points_value_label')
    # extraction_request.extract_ask_far_points_value_label(f'{dmi_rfq}.ask_far_points_value_label')
    # extraction_request.extract_ask_near_price_value_label(f'{dmi_rfq}.ask_near_price_value_label')
    # extraction_request.extract_ask_far_price_value_label(f'{dmi_rfq}.ask_far_price_value_label')
    # extraction_request.extract_opposite_near_bid_qty_value_label(f'{dmi_rfq}.opposite_near_bid_qty_value_label')
    # extraction_request.extract_opposite_near_ask_qty_value_label(f'{dmi_rfq}.opposite_near_ask_qty_value_label')
    # extraction_request.extract_opposite_far_bid_qty_value_label(f'{dmi_rfq}.opposite_far_bid_qty_value_label')
    # extraction_request.extract_opposite_far_ask_qty_value_label(f'{dmi_rfq}.opposite_far_ask_qty_value_label')
    #
    # extraction_request.extract_is_bid_price_pips_enabled(f'{dmi_rfq}.is_bid_price_pips_enabled')
    # extraction_request.extract_is_ask_price_pips_enabled(f'{dmi_rfq}.is_ask_price_pips_enabled')
    # extraction_request.extract_is_near_leg_quantity_enabled(f'{dmi_rfq}.is_near_leg_quantity_enabled')
    extraction_request.extract_is_far_leg_quantity_enabled(f'{dmi_rfq}.is_far_leg_quantity_enabled')
    # extraction_request.extract_is_price_spread_enabled(f'{dmi_rfq}.is_price_spread_enabled')
    # extraction_request.extract_is_bid_price_large_enabled(f'{dmi_rfq}.is_bid_price_large_enabled')
    # extraction_request.extract_is_ask_price_large_enabled(f'{dmi_rfq}.is_ask_price_large_enabled')
    # extraction_request.extract_case_state_value_label_control(f'{dmi_rfq}.case_state_value_label_control')
    # extraction_request.extract_quot_estate_value_label_control(f'{dmi_rfq}.quot_estate_value_label_control')

    result = call(dealer_intervention_service.getRFQDetails, extraction_request.build())
    for R in result:
        print(f'{R} = {result[R]}')


def set_value_di_panel(base_request, dealer_interventions_service):
    modify_request = ModificationRequest(base=base_request)
    modify_request.set_quote_ttl("123")
    modify_request.set_bid_large('999.')
    modify_request.set_bid_small('999')
    modify_request.set_ask_large('999.')
    modify_request.set_ask_small('999')
    modify_request.set_spread_step('999')
    modify_request.click_is_hedged_chec_box()
    # modify_request.increase_ask()
    # modify_request.decrease_ask()
    # modify_request.increase_bid()
    # modify_request.decrease_bid()
    # modify_request.narrow_spread()
    # modify_request.widen_spread()
    # modify_request.skew_towards_ask()
    # modify_request.skew_towards_bid()
    # modify_request.send()
    # modify_request.reject()

    call(dealer_interventions_service.modifyAssignedRFQ, modify_request.build())

def close_dmi_window(base_request, dealer_interventions_service):

    call(dealer_interventions_service.closeWindow, base_request)


def place_esp_by_bid_btn(base_request):
    service = Stubs.win_act_aggregated_rates_service
    btd = BaseTileDetails(base=base_request)
    rfq_request = PlaceESPOrder(details=btd)
    rfq_request.set_action(ESPTileOrderSide.BUY)
    rfq_request.top_of_book(False)
    call(service.placeESPOrder, rfq_request.build())


def place_esp_by_ask_btn(base_request):
    service = Stubs.win_act_aggregated_rates_service
    btd = BaseTileDetails(base=base_request)
    rfq_request = PlaceESPOrder(details=btd)
    rfq_request.set_action(ESPTileOrderSide.SELL)
    rfq_request.top_of_book(False)
    call(service.placeESPOrder, rfq_request.build())


def place_esp_by_tob_buy(base_request):
    service = Stubs.win_act_aggregated_rates_service
    btd = BaseTileDetails(base=base_request)
    rfq_request = PlaceESPOrder(details=btd)
    rfq_request.set_action(ESPTileOrderSide.BUY)
    rfq_request.top_of_book()
    rfq_request.doubleClick()
    call(service.placeESPOrder, rfq_request.build())


def place_esp_by_tob_sell(base_request):
    service = Stubs.win_act_aggregated_rates_service
    btd = BaseTileDetails(base=base_request)
    rfq_request = PlaceESPOrder(details=btd)
    rfq_request.set_action(ESPTileOrderSide.SELL)
    rfq_request.top_of_book()
    call(service.placeESPOrder, rfq_request.build())


def open_ot_by_doubleclick_row(btd, cp_service, row):
    request = PlaceRateTileTableOrderRequest(btd, row, RatesTileTableOrdSide.SELL)
    call(cp_service.placeRateTileTableOrder, request.build())


def open_ar_window_move_left(ar_service, empty_request):
    print('open_ar_window_move_left')
    move_window_details = MoveWindowDetails(base=empty_request)
    move_window_details.set_from_offset('800', '15')
    move_window_details.set_to_offset('-200', '0')

    positions = call(ar_service.arWindowPilotsOrderBookRequest, move_window_details.build())
    print(positions)
    return positions


def ar_pilots_to_actions(ar_service, empty_request, positions):
    print('resize_order_ticket')
    move_window_details = MoveWindowDetails(base=empty_request)
    move_window_details.set_from_offset('950', '50')
    move_window_details.set_to_offset(str(950 + 990), str(50 + 125))

    positions = call(ar_service.arWindowPilotsOrderBookRequest, move_window_details.build())
    print(positions)
    return positions


def get_height(positions, key) -> int:
    # {'newPosition': 'Left:1966 Top:137 Width:570 Height:837', 'initialPosition': 'Left:1016 Top:137 Width:570 Height:837'}
    return int(positions[key].split(' ')[3].split(':')[1])


def get_width(positions, key) -> int:
    # {'newPosition': 'Left:1966 Top:137 Width:570 Height:837', 'initialPosition': 'Left:1016 Top:137 Width:570 Height:837'}
    return int(positions[key].split(' ')[2].split(':')[1])


def amend_order(ob_act, base_request):
    order_details = FXOrderDetails()
    order_details.set_qty('123123123')
    modify_ot_order_request = ModifyFXOrderDetails(base_request)
    modify_ot_order_request.set_order_details(order_details)

    call(ob_act.amendOrder, modify_ot_order_request.build())


def open_order_ticket_via_double_click(ob_act, base_request):
    order_details = FXOrderDetails()
    # order_details.set_qty('123123123')
    modify_ot_order_request = ModifyFXOrderDetails(base_request)
    modify_ot_order_request.set_order_details(order_details)

    call(ob_act.openOrderTicketByDoubleClick, modify_ot_order_request.build())


def cancel_order(ob_act, base_request):
    cancel_order_request = CancelFXOrderDetails(base_request)
    call(ob_act.cancelOrder, cancel_order_request.build())


def release_order(ob_act, base_request):
    order_details = FXOrderDetails()
    release_order_request = ReleaseFXOrderDetails(base_request)
    release_order_request.set_order_details(order_details)
    call(ob_act.releaseOrder, release_order_request.build())


def check_tile_value(base_request, service, row):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.is_tiered(True)
    extract_table_request.set_ask_extraction_fields([ExtractionDetail("rateTile.askPx", "Px"),
                                                     ExtractionDetail("rateTile.askPub", "Pub")])
    extract_table_request.set_bid_extraction_fields([ExtractionDetail("rateTile.bidPx", "Px"),
                                                     ExtractionDetail("rateTile.bidPub", "Pub")])
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    print(response)


def extract_color_from_pricing_button(base_tile_data, cp_service, x, y):
    requests = GetCPRTPColors(base_tile_data=base_tile_data)
    requests.get_pricing_btn_pixel_color(x, y)
    result = call(cp_service.getCPRatesTileColors, requests.build())

    file_name = "image.png"
    with open(file_name, "wb") as fh:
        bts = bytes(base64.standard_b64decode(result['PRICING_BUTTON']))
        print(result['PRICING_BUTTON'])
        fh.write(bts)

    red_image = Image.open(file_name)
    red_image_rgb = red_image.convert("RGB")
    for i in range(90,100):
        for j in range(1,10):
            rgb_pixel_value = red_image_rgb.getpixel((i, j))
            print(rgb_pixel_value, end=' ') # you can check color value in https://www.w3schools.com/colors/colors_rgb.asp
        print()


def create_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    print('create_client_rfq_tile()')
    call(cp_service.createClientRFQTile, base_tile_data)


def close_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    print('close_client_rfq_tile()')
    call(cp_service.closeClientRFQTile, base_tile_data)


def modify_client_rfq_tile(cp_service, base_tile_data):
    print('modify_client_rfq_tile()')
    request = ModifyClientRFQTileRequest(data=base_tile_data)

    request.change_client_tier("Palldium1")
    request.set_from_curr("EUR")
    request.set_to_curr("USD")
    request.change_currency()
    request.change_near_tenor("Spot")
    request.change_far_tenor("1W")
    request.change_client("Palldium1")
    request.change_near_leg_aty("1m")
    request.change_far_leg_aty("2b")
    call(cp_service.modifyRFQTile, request.build())


def place_client_rfq_order(cp_service, base_tile_data):
    print('place_client_rfq_order()')
    requests = ClientRFQTileOrderDetails(data=base_tile_data)
    # requests.set_action_buy()
    requests.set_action_sell()
    call(cp_service.placeClientRFQOrder, requests.build())


def send_client_rfq(cp_service, base_tile_data):
    print('send_client_rfq()')
    call(cp_service.sendRFQOrder, base_tile_data)


def check_fx_order_book_lvl1(base_request, act_ob, case_id, order_id):
    print('check_fx_order_book()')
    ob = FXOrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Order ID", order_id])
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob.add_single_order_info(
            FXOrderInfo.create(
                    action=ExtractionAction.create_extraction_action(
                            extraction_detail=ob_sts)))
    response = call(act_ob.getOrdersDetails, ob.request())
    for k, v in response.items():
        print(f'{k} = {v}')

    verifier = Verifier(case_id)
    verifier.set_event_name("Check that order is canceled")
    verifier.compare_values("Order status", "Cancelled", response[ob_sts.name])
    verifier.verify()


def check_fx_order_book_lvl2(base_request, act_ob, case_id, order_id):
    ob = FXOrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Order ID", order_id])

    child_ord_id = ExtractionDetail("orderBook.childId", "Order ID")
    child_sts = ExtractionDetail("orderBook.childSts", "Sts")
    child_lmt_price = ExtractionDetail("orderBook.childLmtPrice", "Limit Price")
    child_qty = ExtractionDetail("orderBook.childQty", "Qty")

    child_info = FXOrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[child_ord_id,
                                                                                                         child_sts,
                                                                                                         child_lmt_price,
                                                                                                         child_qty]))
    child_details = FXOrdersDetails.create(info=child_info)

    ob_ord_id = ExtractionDetail("OrderBook.ordId", "Order ID")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob_lmt_price = ExtractionDetail("orderBook.lmtPrice", "Limit Price")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    ob.add_single_order_info(
            FXOrderInfo.create(
                    action=ExtractionAction.create_extraction_action(
                            extraction_details=[ob_sts, ob_lmt_price, ob_qty, ob_ord_id]),
                    sub_order_details=child_details))
    response = call(act_ob.getOrdersDetails, ob.request())
    for k, v in response.items():
        print(f'{k} = {v}')

    verifier = Verifier(case_id)
    verifier.set_event_name("Check that order is canceled")
    verifier.compare_values("Order status", "PCA", response[ob_sts.name])
    verifier.verify()


# def reject_from_quote_request_book(base_request, ar_servise):
#     ob = QuoteRequestDetails()
#     execution_id = bca.client_orderid(4)
#     ob.set_default_params(base_request)
#     ob.set_filter(['User', 'QA3'])
#     ob.set_extraction_id(execution_id)
#
#     ob.add_single_order_info(QuoteRequestInfo.create(action=ContextActionsQuoteBook.reject))
#     call(ar_servise.getQuoteRequestBookDetails, ob.request())


def create_or_get_cp_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def place_order(base_request, service):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_slippage("1.23")
    place_request.set_quantity("12334545")
    place_request.click_pips(-3)
    place_request.click_qty(-3)
    print('click()')
    place_request.click_slippage(3)
    place_request.click_stop_price(3)
    # place_request.buy()
    call(service.placeRatesTileOrder, place_request.build())


def execute(report_id, session_id):
    # region Precondition
    common_act = Stubs.win_act

    case_name = Path(__file__).name[:-3]
    quote_owner = "kbrit"
    case_instr_type = "Spot"
    case_venue = "HSB"
    order_id = "MO1210310103937245001"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    print(f'{case_name} started {datetime.now()}')

    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=base_request)
    base_tile_details = BaseTileDetails(base=base_request)

    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    ob_fx_act = Stubs.win_act_order_book_fx
    cp_service = Stubs.win_act_cp_service
    option_service = Stubs.win_act_options
    order_ticket_service = Stubs.win_act_order_ticket_fx
    dealer_interventions_service = Stubs.win_act_dealer_intervention_service
    # endregion

    try:

        # region FE workspace ↓
        # export_layout(base_request, option_service)
        # import_layout(base_request, option_service)
        # endregion

        # region FE options ↓
        # get_default_fx_value(base_request, option_service)
        # set_order_ticket_options(option_service, base_request)
        # set_order_ticket_options(option_service, base_request)
        # set_one_click_mod(option_service, base_request)
        # endregion

        # region RFQ tile ↓
        # modify_rfq_tile(base_tile_details, ar_service)
        # check_venue(base_tile_details, ar_service)
        # extract_rfq_table_data(base_tile_details, ar_service)
        # extract_rfq_panel("rfq_tile_data", base_tile_details, ar_service)
        # temporary doesn't available because of PROC-261
        # extruct_popup_lists_demo("rfq_tenor_popup",base_tile_details,ar_service)
        # endregion

        # region ESP tile ↓
        # create_or_get_rates_tile(base_tile_details, ar_service)
        # modify_rates_tile(base_tile_details, ar_service, 'NOK', 'SEK', 1000000, case_venue)
        # extract_rfq_panel()
        # extract_rfq_table_data()
        # extract_rates_panel_esp(base_tile_details, ar_service)
        # all available ways to open orderTicket via esp panel
        # place_esp_by_bid_btn(base_request)
        # place_esp_by_ask_btn(base_request)
        # place_esp_by_tob_buy(base_request)
        # place_esp_by_tob_sell(base_request
        # )

        # endregion

        # region My Orders ↓
        # get_my_orders_details(ob_act,  base_request, order_id)
        # get_trade_book_details(ob_act,  base_request, order_id)
        # endregion

        # region OrderTicket
        # place_fx_order(base_request,order_ticket_service)
        set_fx_order_ticket_value(base_request,order_ticket_service)
        # extract_order_ticket_values(base_tile_data, order_ticket_service)
        # close_fx_order(base_request,order_ticket_service);
        # endregion

        # region ClientPricing
        # extract_cp_rates_panel(base_tile_details,cp_service)
        # create_or_get_cp_rates_tile(base_tile_details, cp_service)
        # check_tile_value(base_tile_details, cp_service,1 )
        # select_rows(base_tile_details, [1, 2], cp_service)
        # print('Sleeping')
        # time.sleep(5)
        # print('Deselecting')
        # deselect_rows(base_tile_details,cp_service)
        # row = 2
        # open_ot_by_doubleclick_row(base_tile_data, cp_service, row)
        # set_fx_order_ticket_value(base_request,order_ticket_service)
        # for i in range(0, 10):
        # for j in range(100,110):
        #     print(j,end=" ")
        # extract_color_from_pricing_button(base_tile_data, cp_service,89, 0)
        # place_order(base_tile_details, cp_service)
        # endregion

        # region Client Pricing RFQ tile

        # create_client_rfq_tile(cp_service, base_tile_data)
        # modify_client_rfq_tile(cp_service, base_tile_data)
        # send_client_rfq(cp_service, base_tile_data)
        # place_client_rfq_order(cp_service, base_tile_data)
        # close_client_rfq_tile(cp_service, base_tile_data)
        # extract_color_from_pricing_button(base_tile_data, cp_service,0, 0)

        # endregion

        # region Dealer Intervention
        # extract_di_panel(base_request, dealer_interventions_service)
        # set_value_di_panel(base_request, dealer_interventions_service)
        # close_dmi_window(base_request, dealer_interventions_service)
        # endregion

        # region example of Drab&Drop
        # coords = open_ar_window_move_left(ar_service, base_request)
        # ar_pilots_to_actions(ar_service, base_request, coords)
        # endregion

        # region OrderBook actions
        # amend_order(ob_fx_act, base_request)
        # open_order_ticket_via_double_click(ob_fx_act, base_request)
        # cancel_order(ob_fx_act, base_request)
        # release_order(ob_fx_act, base_request)
        # clear_filters(ob_fx)
        # check_fx_order_book_lvl1(base_request, ob_fx_act, report_id, 'AO1210708111556095001')
        # check_fx_order_book_lvl2(base_request, ob_fx_act, report_id, 'AO1210708111556095001')
        # endregion

        # region Quote Request Book
        # reject_from_quote_request_book(base_request, ar_service)
        # endregion

    except Exception as e:
        logging.error("Error execution", exc_info=True)

# print('end time = ' + str(datetime.now()))
# for rule in [RFQ, TRFQ]:
#     rule_manager.remove_rule(rule)
