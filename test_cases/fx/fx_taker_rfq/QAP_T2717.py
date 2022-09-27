import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, qty, cur1, cur2, tenor, client, venue):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_quantity_as_string(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_client(client)
    action = ContextAction.create_venue_filter(venue)
    modify_request.add_context_action(action)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.SELL)
    call(service.placeRFQOrder, rfq_request.build())


def check_order_book(base_request, act_ob, case_id, qty):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Qty", qty])
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_id = ExtractionDetail("orderBook.orderId", "Order ID")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_exec_sts,
                                                                                 ob_id])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('Sts', 'Filled', response[ob_exec_sts.name])
    verifier.verify()
    return response[ob_id.name]


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book

    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_near_tenor = "Spot"
    case_venue = "CITI"
    symbol = case_from_currency + "/" + case_to_currency

    case_qty = random_qty(1, 3, 7)
    connectivity_drop_copy = "fix-sell-m-314luna-drop"
    verifier = Stubs.verifier

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency, case_to_currency,
                        case_client, case_near_tenor, case_venue)
        send_rfq(base_rfq_details, ar_service)
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint
        place_order_tob(base_rfq_details, ar_service)
        order_id = check_order_book(case_base_request, ob_act, case_id, case_qty)

        order_params = {
            'ExecID': '*',
            'OrderQty': case_qty,
            'LastQty': case_qty,
            'LastSpotRate': '*',
            'OrderID': order_id,
            'TransactTime': '*',
            'Side': '*',
            'AvgPx': '*',
            'OrdStatus': '2',
            'SettlCurrency': case_to_currency,
            'SettlDate': spo(),
            'Currency': case_from_currency,
            'TimeInForce': '3',
            'TradeDate': '*',
            'ExecType': 'F',
            'HandlInst': '1',
            'LeavesQty': '0',
            'NoParty': [{
                'PartyID': '*',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'CumQty': case_qty,
            'LastPx': '*',
            'SpotSettlDate': spo(),
            'OrdType': "D",
            'ClOrdID': order_id,
            'SecondaryOrderID': '*',
            'LastMkt': '*',
            'QtyType': '*',
            'SettlType': '*',
            'Price': '*',
            'Instrument': {
                'SecurityType': 'FXSPOT',
                'Symbol': symbol,
                'SecurityID': symbol,
                'Product': '4',
                'SecurityExchange': '*'
            },
            'SecondaryExecID': '*',
            'ExDestination': '*',
            'GrossTradeAmt': '*',
        }
        verifier.submitCheckRule(
            bca.create_check_rule("Check Drop Copy Execution Report",
                                  bca.filter_to_grpc('ExecutionReport', order_params, ["OrderID", "OrdStatus"]),
                                  checkpoint_id1,
                                  connectivity_drop_copy,
                                  case_id)
        )

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
