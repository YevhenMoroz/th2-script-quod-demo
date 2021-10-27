import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from quod_qa.fx.fx_wrapper.common_tools import random_qty
from quod_qa.win_gui_wrappers.data_set import OrderBookColumns
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_order_ticket(base_request, service, qty):
    order_ticket = FXOrderDetails()
    order_ticket.set_qty(qty)
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def click_on_bid_btn(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.top_of_book()
    esp_request.set_action(ESPTileOrderSide.BUY)
    call(service.placeESPOrder, esp_request.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    order_ticket_service = Stubs.win_act_order_ticket_fx

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
    qty = random_qty(1, 3, 7)
    strategy = "1555"

    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        click_on_bid_btn(base_esp_details, ar_service)
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint

        modify_order_ticket(case_base_request, order_ticket_service, qty)
        FXOrderBook(case_id, case_base_request).set_filter([OrderBookColumns.qty.value, qty]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: "Filled"})
        order_book = FXOrderBook(case_id, case_base_request)
        order_id = order_book.set_filter([OrderBookColumns.qty.value, qty]).extract_field(
            OrderBookColumns.order_id.value)

        order_params = {
            'ExecID': '*',
            'OrderQty': qty,
            'LastQty': "*",
            'LastSpotRate': '*',
            'OrderID': order_id,
            'TransactTime': '*',
            'Side': '*',
            'AvgPx': '*',
            'OrdStatus': '2',
            'LastExecutionPolicy': '*',
            'TradeReportingIndicator': '*',
            'ReplyReceivedTime': '*',
            'SettlCurrency': "USD",
            'SettlDate': spo(),
            'Currency': "EUR",
            'TimeInForce': '3',
            'TradeDate': '*',
            'Price': '*',
            'ExecType': 'F',
            'HandlInst': '2',
            'LeavesQty': '0',
            'NoParty': [{
                'PartyID': '*',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'CumQty': qty,
            'LastPx': '*',
            'SpotSettlDate': spo(),
            'OrdType': "2",
            'Text': "*",
            'ClOrdID': order_id,
            'SecondaryOrderID': '*',
            'QtyType': '*',
            'StrategyName': strategy,
            'TargetStrategy': '*',
            'SettlType': '*',
            'Instrument': {
                'SecurityType': 'FXSPOT',
                'Symbol': "EUR/USD",
                'SecurityID': "EUR/USD",
                'Product': '4',
                'SecurityIDSource': '8',
                'SecurityExchange': '*'
            },
            'SecondaryExecID': '*',
            'ExDestination': '*',
            'GrossTradeAmt': '*',
        }

        verifier.submitCheckRule(
            bca.create_check_rule("Check Drop Copy Execution Report",
                                  bca.filter_to_grpc('ExecutionReport', order_params,
                                                     ["OrderID", "ExecType", "LeavesQty"]),
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
            call(ar_service.closeRatesTile, base_esp_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
