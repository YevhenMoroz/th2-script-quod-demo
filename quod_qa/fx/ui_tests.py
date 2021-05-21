import logging
import time
from datetime import datetime
from pathlib import Path

from th2_grpc_act_gui_quod.layout_panel_service import LayoutPanelServiceService

import rule_management as rm
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import (RFQTileOrderSide, PlaceRFQRequest, ModifyRatesTileRequest,
                                                       ContextActionRatesTile, ModifyRFQTileRequest, ContextAction,
                                                       TableActionsRequest, TableAction, CellExtractionDetails,
                                                       ExtractRFQTileValues, ExtractRatesTileDataRequest)
from win_gui_modules.client_pricing_wrappers import SelectRowsRequest, DeselectRowsRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.layout_panel_wrappers import (WorkspaceModificationRequest, OptionOrderTicketRequest,
                                                   DefaultFXValues)
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
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


def get_trade_book_details(ob_act, base_request, order_id):
    """
    Demonstration of work with Trade book window
    """

    main_order_details = OrdersDetails()
    # to set filter use list with string pairs like ['ColumnName', 'ColumnValue']
    main_order_details.set_filter(["Side", 'Buy',
                                   'Venue', 'QUODFX'])
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id( "trade.1")
    # to extruct values from first row user str pairs 'UniqID','ColumnNanme'
    ob_instr_type = ExtractionDetail("tradeBook.instrtype", "ExecID")
    ob_exec_sts = ExtractionDetail("tradeBook.orderid", "Venue")
    ob_lookup = ExtractionDetail("tradeBook.lookup", "Qty")
    ob_creat_time = ExtractionDetail("tradeBook.creattime", "CreationTime")
    # use next expression to add extraction  settings before  run grpc call
    main_order_details.add_single_order_info(
            OrderInfo.create(
                    action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                         ob_exec_sts,
                                                                                         ob_lookup,
                                                                                         ob_creat_time])))
    # to extract values to a dict use next statement
    result = call(ob_act.getTradeBookDetails, main_order_details.request())
    # you may use loop to check values
    for key,value in result.items():
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

    extract_value.set_extraction_id(exec_id )
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
    modification_request = WorkspaceModificationRequest()
    modification_request.set_default_params(base_request=base_request)
    modification_request.set_filename("demo_export_file.xml")
    modification_request.set_path(
        'C:\\Users\\kbrit\\PycharmProjects\\prev_th2-script-quod-demo\\quod_qa\\fx\\fx_taker_rfq')
    modification_request.do_export()

    call(option_service.modifyWorkspace, modification_request.build())


def import_layout(base_request, option_service):
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
    fx_values = DefaultFXValues();
    fx_values.AggressiveTIF = "Pegger"
    order_type = "Market"
    tif = "FillOrKill"
    strategy_type = "Quod DarkPool"
    strategy = "PeggedTaker"
    child_strategy = "BasicTaker"
    fx_values.AggressiveOrderType = order_type
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
    fx_values.DMASlippage = '12678.09'
    fx_values.Client = "FIXCLIENT4"


    order_ticket_options.set_default_fx_values(fx_values)
    call(option_service.setOptionOrderTicket, order_ticket_options.build())





def set_fx_order_ticket_value(base_request):
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
    order_ticket.set_client('FIXCLIENT3')
    order_ticket.set_tif('Day')
    order_ticket.set_slippage('2.5')
    order_ticket.set_order_type('Limit')
    order_ticket.set_stop_price('1.3')

    new_order_details = NewFxOrderDetails()
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    # new servise was added
    order_ticket_service = Stubs.win_act_order_ticket_fx
    call(order_ticket_service.placeFxOrder, new_order_details.build())


def select_rows(base_tile_details, row_numbers,cp_service):
    """
    To select several rows send tuple or list with numbers [1,2,3].
    WARNING!
    when you send numbers more than 4 test case will scroll up after it select all rows you asked
    """
    request = SelectRowsRequest(base_tile_details)
    request.set_row_numbers(row_numbers)
    call(cp_service.selectRows, request.build())

def deselect_rows(base_tile_details,cp_service):
    """
    The method will deselect all selected rows like Esk button
    """
    request = DeselectRowsRequest(base_tile_details)
    call(cp_service.deselectRows, request.build())


def extract_rates_panel(base_tile_details, ar_service):


    s = 'RatesTile0'
    request = ExtractRatesTileDataRequest(base_tile_details)
    request.set_extraction_id(f'{s}.extraction_id')
    request.extract_instrument(f'{s}.instrument')
    request.extract_quantity(f'{s}.quantity')
    request.extract_tenor(f'{s}.tenor')
    request.extract_best_bid(f'{s}.best_bid')
    request.extract_best_bid_large(f'{s}.best_bid_large')
    request.extract_best_bid_small(f'{s}.best_bid_small')
    request.extract_best_ask(f'{s}.best_ask')
    request.extract_best_ask_large(f'{s}.best_ask_large')
    request.extract_best_ask_small(f'{s}.best_ask_small')
    request.extract_spread(f'{s}.spread')

    result  = call(ar_service.extractRatesTileValues, request.build())
    print(result)
    for k in result:
        print(f'{k} = {result[k]}')


def execute(report_id):
    # region Preparation
    # print('start time = ' + str(datetime.now()))
    common_act = Stubs.win_act

    # Rules
    rule_manager = rm.RuleManager()
    # RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    # TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    # print_active_rules()
    case_name = Path(__file__).name[:-3]
    quote_owner = "kbrit"
    case_instr_type = "Spot"
    case_venue = "HSB"
    order_id = "MO1210310103937245001"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()

    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    base_tile_details = BaseTileDetails(base=base_request)

    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    option_service = Stubs.win_act_options
    # endregion
    Stubs.frontend_is_open = True
    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
        # ,
        #          fe_dir='qf_trading_fe_folder_308',
        #          fe_user='qf_trading_fe_user_308',
        #          fe_pass='qf_trading_fe_password_308')
    else:
        get_opened_fe(case_id, session_id)

    try:
        # region FE workspace ↓
        # import_layout(base_request, option_service)
        # export_layout(base_request, option_service)
        # endregion

        # region FE options ↓
        # get_default_fx_value(base_request, option_service)
        # set_order_ticket_options(option_service, base_request)
        # set_order_ticket_options(option_service, base_request)
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
        # modify_rates_tile(base_request, ar_service, 'GBP', 'USD', 1000000, case_venue)
        # extract_rfq_panel()
        # extract_rfq_table_data()
        extract_rates_panel(base_tile_details, ar_service)
        # endregion

        # region My Orders ↓

        # get_my_orders_details(ob_act,  base_request, order_id)
        # get_trade_book_details(ob_act,  base_request, order_id)

        # endregion

        # region OrderTicket
        # set_fx_order_ticket_value(base_request)
        # endregion

        # region ClientPricing
        # select_rows(base_tile_details, [1, 2, 4], cp_service)
        # print('Sleeping')
        # time.sleep(5)
        # print('Deselecting')
        # deselect_rows(base_tile_details,cp_service)
        # endregion

        # close_fe_2(case_id, session_id)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

# print('end time = ' + str(datetime.now()))
# for rule in [RFQ, TRFQ]:
#     rule_manager.remove_rule(rule)
