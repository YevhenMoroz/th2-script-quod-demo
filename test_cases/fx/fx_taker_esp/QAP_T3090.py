# import logging
# from pathlib import Path
#
# from custom import basic_custom_actions as bca
# from custom.verifier import Verifier, VerificationMethod
# from stubs import Stubs
# from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, ActionsRatesTile, \
#     PlaceESPOrder, ESPTileOrderSide
# from win_gui_modules.common_wrappers import BaseTileDetails
# from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
# from win_gui_modules.order_ticket import FXOrderDetails
# from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
# from win_gui_modules.utils import call, get_base_request
# from win_gui_modules.wrappers import set_base
#
#
# def create_or_get_rates_tile(base_request, service):
#     call(service.createRatesTile, base_request.build())
#
#
# def modify_order_ticket(base_request, service, qty, tif, client):
#     order_ticket = FXOrderDetails()
#     order_ticket.set_qty(qty)
#     order_ticket.set_tif(tif)
#     order_ticket.set_client(client)
#     order_ticket.set_place()
#     new_order_details = NewFxOrderDetails(base_request, order_ticket)
#     call(service.placeFxOrder, new_order_details.build())
#
#
# def place_order(base_request, service):
#     esp_request = PlaceESPOrder(details=base_request)
#     esp_request.top_of_book()
#     esp_request.set_action(ESPTileOrderSide.BUY)
#     call(service.placeESPOrder, esp_request.build())
#
#
# def modify_rates_tile(base_request, service, from_c, to_c, tenor):
#     modify_request = ModifyRatesTileRequest(details=base_request)
#     modify_request.set_instrument(from_c, to_c, tenor)
#     call(service.modifyRatesTile, modify_request.build())
#
#
# def filter_venue(base_request, service, venues):
#     modify_request = ModifyRatesTileRequest(details=base_request)
#     venue_filter = ContextActionRatesTile.create_venue_filters(venues)
#     modify_request.add_context_action(venue_filter)
#     call(service.modifyRatesTile, modify_request.build())
#
#
# def check_order_book_2_child(base_request, act_ob, case_id, tif, owner, qty):
#     ob = OrdersDetails()
#     execution_id = bca.client_orderid(4)
#     ob.set_default_params(base_request)
#     ob.set_extraction_id(execution_id)
#     ob.set_filter(["Owner", owner, "Qty", qty])
#     child_1_tif = ExtractionDetail("child_1.tif", "TIF")
#     child_1_ext_action = ExtractionAction.create_extraction_action(
#         extraction_detail=child_1_tif)
#     child_1_info = OrderInfo.create(action=child_1_ext_action)
#     child_2_tif = ExtractionDetail("child_2.tif", "TIF")
#     child_2_ext_action = ExtractionAction.create_extraction_action(
#         extraction_detail=child_2_tif)
#     child_2_info = OrderInfo.create(action=child_2_ext_action)
#
#     child_orders_details = OrdersDetails.create(order_info_list=[child_1_info, child_2_info])
#
#     ob_tif = ExtractionDetail("orderBook.tif", "TIF")
#     ob.add_single_order_info(
#         OrderInfo.create(
#             action=ExtractionAction.create_extraction_action(extraction_details=[ob_tif]),
#             sub_order_details=child_orders_details))
#     response = call(act_ob.getOrdersDetails, ob.request())
#     verifier = Verifier(case_id)
#     verifier.set_event_name("Check Order book")
#     verifier.compare_values("Main order TIF", tif, response[ob_tif.name])
#     verifier.compare_values("Check that child orders have different TIF", response[child_1_tif.name],
#                             response[child_2_tif.name], VerificationMethod.NOT_EQUALS)
#
#     verifier.verify()
#
#
# def check_order_book_1_child(base_request, act_ob, case_id, tif, owner, qty):
#     ob = OrdersDetails()
#     execution_id = bca.client_orderid(4)
#     ob.set_default_params(base_request)
#     ob.set_extraction_id(execution_id)
#     ob.set_filter(["Owner", owner, "Qty", qty])
#     child_1_tif = ExtractionDetail("child_1.tif", "TIF")
#     child_1_ext_action = ExtractionAction.create_extraction_action(
#         extraction_detail=child_1_tif)
#     child_1_info = OrderInfo.create(action=child_1_ext_action)
#
#     child_orders_details = OrdersDetails.create(order_info_list=[child_1_info])
#
#     ob_tif = ExtractionDetail("orderBook.tif", "TIF")
#     ob.add_single_order_info(
#         OrderInfo.create(
#             action=ExtractionAction.create_extraction_action(extraction_details=[ob_tif]),
#             sub_order_details=child_orders_details))
#     response = call(act_ob.getOrdersDetails, ob.request())
#     verifier = Verifier(case_id)
#     verifier.set_event_name("Check Order book")
#     verifier.compare_values("Main order TIF", tif, response[ob_tif.name])
#     verifier.compare_values("Check child order TIF", tif, response[child_1_tif.name])
#
#     verifier.verify()
#
#
# def execute(report_id, session_id):
#     case_name = Path(__file__).name[:-3]
#
#     order_ticket_service = Stubs.win_act_order_ticket_fx
#     ob_act = Stubs.win_act_order_book
#
#     # Create sub-report for case
#     case_id = bca.create_event(case_name, report_id)
#
#     set_base(session_id, case_id)
#     ar_service = Stubs.win_act_aggregated_rates_service
#
#     case_base_request = get_base_request(session_id, case_id)
#     base_esp_details = BaseTileDetails(base=case_base_request)
#
#     owner = Stubs.custom_config['qf_trading_fe_user']
#     from_curr = "EUR"
#     to_curr = "USD"
#     tenor = "Spot"
#     venue = ["CIT", "MS"]
#     tif_fok = "FillOrKill"
#     tif_iok = "ImmediateOrCancel"
#     qty = "8000000"
#     client = "ASPECT_CITI"
#     try:
#         # Step 1
#         create_or_get_rates_tile(base_esp_details, ar_service)
#         modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
#         filter_venue(base_esp_details, ar_service, venue)
#         # Step 2
#         place_order(base_esp_details, ar_service)
#         modify_order_ticket(case_base_request, order_ticket_service, qty, tif_iok, client)
#         check_order_book_2_child(case_base_request, ob_act, case_id, tif_iok, owner, qty)
#         # Step 3
#         place_order(base_esp_details, ar_service)
#         modify_order_ticket(case_base_request, order_ticket_service, qty, tif_fok, client)
#         check_order_book_1_child(case_base_request, ob_act, case_id, tif_fok, owner, qty)
#
#     except Exception:
#         logging.error("Error execution", exc_info=True)
#         bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
#     finally:
#         try:
#             # Close tile
#             call(ar_service.closeRatesTile, base_esp_details.build())
#
#         except Exception:
#             logging.error("Error execution", exc_info=True)
# import logging
# from pathlib import Path
#
# from custom import basic_custom_actions as bca
# from custom.verifier import Verifier, VerificationMethod
# from stubs import Stubs
# from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
# from win_gui_modules.common_wrappers import BaseTileDetails
# from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
#     ModifyFXOrderDetails, ReleaseFXOrderDetails
# from win_gui_modules.order_ticket import FXOrderDetails
# from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
# from win_gui_modules.utils import call, get_base_request, prepare_fe_2, get_opened_fe
# from win_gui_modules.wrappers import set_base
#
#
# def create_or_get_rates_tile(base_request, service):
#     call(service.createRatesTile, base_request.build())
#
#
# def modify_rates_tile(base_request, service, from_c, to_c, tenor):
#     modify_request = ModifyRatesTileRequest(details=base_request)
#     modify_request.set_instrument(from_c, to_c, tenor)
#     call(service.modifyRatesTile, modify_request.build())
#
#
# def place_order(base_request, service):
#     esp_request = PlaceESPOrder(details=base_request)
#     esp_request.top_of_book()
#     esp_request.set_action(ESPTileOrderSide.BUY)
#     call(service.placeESPOrder, esp_request.build())
#
#
# def modify_order_ticket(base_request, service, qty):
#     order_ticket = FXOrderDetails()
#     order_ticket.set_qty(qty)
#     order_ticket.set_pending(True)
#     order_ticket.set_place(True)
#     new_order_details = NewFxOrderDetails(base_request, order_ticket)
#     call(service.placeFxOrder, new_order_details.build())
#
#
# def amend_order(base_request, ob_act, qty):
#     order_details = FXOrderDetails()
#     order_details.set_qty(qty)
#     amend_order_request = ModifyFXOrderDetails(base_request)
#     amend_order_request.set_order_details(order_details)
#     call(ob_act.amendOrder, amend_order_request.build())
#
#
# def release_order(base_request, ob_act):
#     order_details = FXOrderDetails()
#     release_order_request = ReleaseFXOrderDetails(base_request)
#     release_order_request.set_order_details(order_details)
#     call(ob_act.releaseOrder, release_order_request.build())
#
#
# def check_order_book(base_request, act_ob, case_id, owner, qty, status, *args):
#     ob = OrdersDetails()
#     execution_id = bca.client_orderid(4)
#     ob.set_default_params(base_request)
#     ob.set_extraction_id(execution_id)
#     ob.set_filter(["Owner", owner])
#     ob_status = ExtractionDetail("orderBook.Status", "Sts")
#     ob_qty = ExtractionDetail("orderBook.Qty", "Qty")
#
#     ob.add_single_order_info(
#         OrderInfo.create(
#             action=ExtractionAction.create_extraction_action(extraction_details=[ob_status, ob_qty])))
#     response = call(act_ob.getOrdersDetails, ob.request())
#
#     verifier = Verifier(case_id)
#     method = ""
#     if "EQUAL" in args:
#         method = VerificationMethod.EQUALS
#     if "NOT_EQUAL" in args:
#         method = VerificationMethod.NOT_EQUALS
#     verifier.set_event_name("Check Order book")
#     verifier.compare_values("Qty", qty, response[ob_qty.name].replace(',', ''))
#     verifier.compare_values("InstrType", status, response[ob_status.name], method)
#     verifier.verify()
#
#
# def execute(report_id, session_id):
#     case_name = Path(__file__).name[:-3]
#     order_ticket_service = Stubs.win_act_order_ticket_fx
#     ob_service = Stubs.win_act_order_book
#     fx_ob_service = Stubs.win_act_order_book_fx
#     # Create sub-report for case
#     case_id = bca.create_event(case_name, report_id)
#
#     set_base(session_id, case_id)
#     ar_service = Stubs.win_act_aggregated_rates_service
#
#     case_base_request = get_base_request(session_id, case_id)
#     base_esp_details = BaseTileDetails(base=case_base_request)
#
#     from_curr = "EUR"
#     to_curr = "USD"
#     tenor = "Spot"
#     qty = "5000000"
#     amend_qty = "6000000"
#     equal = "EQUAL"
#     not_equal = "NOT_EQUAL"
#
#     owner = Stubs.custom_config['qf_trading_fe_user']
#     sts_validated = "Validated"
#
#     try:
#         # Step 1
#         create_or_get_rates_tile(base_esp_details, ar_service)
#         modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
#         place_order(base_esp_details, ar_service)
#         # Step 2
#         modify_order_ticket(case_base_request, order_ticket_service, qty)
#         check_order_book(case_base_request, ob_service, case_id, owner, qty, sts_validated, equal)
#         # Step 3-4
#         amend_order(case_base_request, fx_ob_service, amend_qty)
#         # Step 5
#         release_order(case_base_request, fx_ob_service)
#         check_order_book(case_base_request, ob_service, case_id, owner, amend_qty, sts_validated, not_equal)
#
#     except Exception:
#         logging.error("Error execution", exc_info=True)
#         bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
#     finally:
#         try:
#             # Close tile
#             call(ar_service.closeRatesTile, base_esp_details.build())
#         except Exception:
#             logging.error("Error execution", exc_info=True)

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderType
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_order_ticket import FXOrderTicket
from test_framework.win_gui_wrappers.forex.rates_tile import RatesTile
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns as ob, Status as st


class QAP_T3090(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = RatesTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.order_ticket = FXOrderTicket(self.test_id, self.session_id)
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.tenor_spot = self.data_set.get_tenor_by_name("tenor_spot")
        self.client = self.data_set.get_client_by_name("client_1")
        self.tif_fok = TimeInForce.FOK.value
        self.tif_ioc = TimeInForce.IOC.value
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.ord_type = OrderType.market.value
        self.from_cur = self.symbol[:3]
        self.to_cur = self.symbol[4:]
        self.qty = "5000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_rates_tile(self.from_cur, self.to_cur, self.tenor_spot, qty=self.qty)
        self.rates_tile.click_on_tob_buy()
        self.order_ticket.set_order_details(tif=self.tif_ioc, order_type=self.ord_type, client=self.client, pending=True)
        self.order_ticket.create_order()

        self.order_book.set_filter(
            [ob.symbol.value, self.symbol, ob.qty.value, self.qty]).check_order_fields_list(
            {ob.symbol.value: self.symbol,
             ob.sts.value: st.validated.value,
             ob.qty.value: self.qty,
             ob.tif.value: self.tif_ioc}, 'Checking currency value in order book')
        # endregion
        # region Step 2
        self.order_ticket.amend_order([ob.symbol.value, self.symbol, ob.qty.value, self.qty])
        self.order_ticket.set_order_details(tif=self.tif_fok)
        self.order_ticket.create_order()
        self.order_ticket.release_order_request([ob.symbol.value, self.symbol, ob.qty.value, self.qty])
        self.order_book.set_filter(
            [ob.symbol.value, self.symbol, ob.qty.value, self.tif_fok]).check_order_fields_list(
            {ob.sts.value: st.terminated.value,
             ob.qty.value: self.qty,
             ob.tif.value: self.tif_fok}, 'Checking currency value in order book')
        # endregion
