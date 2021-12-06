import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.order_book_wrappers import CancelOrderDetails, OrdersDetails, ExtractionDetail, ExtractionAction, \
    OrderInfo
from win_gui_modules.utils import get_base_request, call


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    case_base_request = get_base_request(session_id, case_id)
    ob_service = Stubs.win_act_order_book
    try:
        # region CancelOrder ↓
        cancel_request = CancelOrderDetails(case_base_request)
        cancel_request.set_filter(["Qty", "1000000"])
        call(ob_service.cancelOrder, cancel_request.build())
        # endregion

        # region OrderExtract ↓
        extraction_id = bca.client_orderid(5)
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(case_base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["Order ID", "AO1211201160203720001"])
        main_order_qty = ExtractionDetail("order_qty", "Qty")

        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_qty])
        main_order_details.add_single_order_info(
            OrderInfo.create(action=main_order_extraction_action))
        request = call(ob_service.getOrdersDetails, main_order_details.request())

        main_qty = request[main_order_qty.name]
        print(main_qty)
        # endregion

        # region Verifier ↓
        extraction_id = bca.client_orderid(5)
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(case_base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["Order ID", "AO1211201160203720001"])
        main_order_qty = ExtractionDetail("order_qty", "Qty")

        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_qty])
        main_order_details.add_single_order_info(
            OrderInfo.create(action=main_order_extraction_action))
        request = call(ob_service.getOrdersDetails, main_order_details.request())

        qty = request[main_order_qty.name]
        verifier = Verifier(case_id)
        verifier.set_event_name("Check Qty")
        verifier.compare_values("Qty", "1,000,000", qty)
        verifier.verify()
        # endregion

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(case_base_request)
        main_order_details.set_extraction_id("order_info_extraction")
        main_order_details.set_filter(["Order ID", "AO1211201160203720001"])
        main_order_qty = ExtractionDetail("order_qty", "Qty")

        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_qty])

        child1_id = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
        sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
            extraction_details=[child1_id])
        sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])

        child2_id = ExtractionDetail("subOrder_lvl_2.id", "Order ID")
        sub_lvl1_2_ext_action = ExtractionAction.create_extraction_action(
            extraction_detail=child2_id)
        sub_lv1_2_info = OrderInfo.create(actions=[sub_lvl1_2_ext_action])

        sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info, sub_lv1_2_info])

        main_order_details.add_single_order_info(
            OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
        request = call(ob_service.getOrdersDetails, main_order_details.request())



    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
