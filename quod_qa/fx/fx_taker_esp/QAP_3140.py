import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from quod_qa.fx.fx_wrapper.common_tools import random_qty
from test_framework.win_gui_wrappers.data_set import OrderBookColumns
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ModifyFXOrderDetails
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_order_ticket(base_request, service, qty):
    order_ticket = FXOrderDetails()
    order_ticket.set_qty(qty)
    order_ticket.set_tif("GoodTillCancel")
    order_ticket.set_price_pips("000")
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def click_on_tob(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.top_of_book()
    esp_request.set_action(ESPTileOrderSide.BUY)
    call(service.placeESPOrder, esp_request.build())


def amend_order(ob_act, base_request, qty, qty_filter):
    order_details = FXOrderDetails()
    order_details.set_qty(qty)
    modify_ot_order_request = ModifyFXOrderDetails(base_request)
    modify_ot_order_request.set_filter(qty_filter)
    modify_ot_order_request.set_order_details(order_details)

    call(ob_act.amendOrder, modify_ot_order_request.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    order_ticket_service = Stubs.win_act_order_ticket_fx
    ob_service = Stubs.win_act_order_book_fx

    connectivity_drop_copy = "fix-sell-m-314luna-drop"
    verifier = Stubs.verifier
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    qty = random_qty(2, 3, 8)
    amend_qty = random_qty(3, 4, 8)

    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        click_on_tob(base_esp_details, ar_service)
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint

        modify_order_ticket(case_base_request, order_ticket_service, qty)
        FXOrderBook(case_id, case_base_request).set_filter([OrderBookColumns.qty.value, qty]).check_order_fields_list(
            {OrderBookColumns.sts.value: "Open"})
        order_book = FXOrderBook(case_id, case_base_request)
        order_id = order_book.set_filter([OrderBookColumns.qty.value, qty]).extract_field(
            OrderBookColumns.order_id.value)

        order_params = {
            'ExecID': '*',
            'OrderQty': qty,
            'LastQty': "*",
            'OrderID': order_id,
            'TransactTime': '*',
            'Side': '*',
            'AvgPx': '*',
            'OrdStatus': '0',
            'Account': '*',
            'SettlCurrency': "USD",
            'SettlDate': spo(),
            'Currency': "EUR",
            'TimeInForce': '1',
            'Price': '*',
            'ExecType': '0',
            'HandlInst': '2',
            'LeavesQty': qty,
            'NoParty': "*",
            'CumQty': "0",
            'LastPx': '*',
            'OrdType': "2",
            'ClOrdID': order_id,
            'QtyType': '*',
            'StrategyName': "*",
            'TargetStrategy': '*',
            'ExecRestatementReason': '*',
            'SettlType': '*',
            'Instrument': {
                'SecurityType': 'FXSPOT',
                'Symbol': "EUR/USD",
                'SecurityID': "EUR/USD",
                'Product': '4',
                'SecurityIDSource': '8',
            }
        }

        verifier.submitCheckRule(
            bca.create_check_rule("Check Drop Copy Execution Report",
                                  bca.filter_to_grpc('ExecutionReport', order_params,
                                                     ["OrderID", "ExecType"]),
                                  checkpoint_id1,
                                  connectivity_drop_copy,
                                  case_id)
        )

        checkpoint_response = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_modify = checkpoint_response.checkpoint
        amend_order(ob_service, case_base_request, amend_qty, [OrderBookColumns.qty.value, qty])
        FXOrderBook(case_id, case_base_request).set_filter(
            [OrderBookColumns.qty.value, amend_qty]).check_order_fields_list(
            {OrderBookColumns.sts.value: "Open"})

        order_params_amend = {
            'OrderQty': amend_qty,
            'OrderID': order_id,
            'OrdType': "2",
            'OrigClOrdID': order_id,
            'TransactTime': "*",
            'TimeInForce': "1",
            'ClOrdID': "*",
            'Price': "*"
        }
        verifier.submitCheckRule(
            bca.create_check_rule("Check Drop Copy Modify Requests",
                                  bca.filter_to_grpc('OrderCancelReplaceRequest', order_params_amend,
                                                     ["OrderID"]),
                                  checkpoint_modify,
                                  connectivity_drop_copy,
                                  case_id)
        )
        checkpoint_response = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_cancel = checkpoint_response.checkpoint
        order_book.cancel_order(filter_list=[OrderBookColumns.qty.value, amend_qty])

        order_params_cancel = {
            'TransactTime': '*',
            'ClOrdID': '*',
            'OrigClOrdID': '*'
        }
        verifier.submitCheckRule(
            bca.create_check_rule("Check Drop Copy CancelRequest",
                                  bca.filter_to_grpc('OrderCancelRequest', order_params_cancel),
                                  checkpoint_cancel,
                                  connectivity_drop_copy,
                                  case_id)
        )

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
