import logging
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe, close_fe, get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent, order_analysis_algo_parameters_request, \
    create_order_analysis_events_request, create_verification_request, check_value
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo,\
    ExtractionDetail, ExtractionAction, ModifyOrderDetails, CancelOrderDetails
from th2_grpc_act_gui_quod.act_ui_win_pb2 import VerificationDetails
from rule_management import RuleManager


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    rule_manager = RuleManager()

    buy_side_session_alias = "fix-bs-eq-trqx"
    fh_session_alias = "fix-fh-eq-trqx"

    # Rules

    nos = rule_manager.add_NOS(buy_side_session_alias, "TRQX_CLIENT1")
    ocrr = rule_manager.add_OCRR(buy_side_session_alias)
    ocr = rule_manager.add_OCR(buy_side_session_alias)

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-2838"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:
        # Preconditions
        symbol_trqx = "3631"
        MDRefID_trqx = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_trqx,
            connection_id=ConnectionID(session_alias=fh_session_alias)
        )).MDRefID
        mdir_params_trade = {
            'MDReqID': MDRefID_trqx,
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '1',
                    'MDEntrySize': '100',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        Stubs.fix_act.sendMessage(request=bca.convert_to_request(
            'Send MarketDataIncrementalRefresh', fh_session_alias, case_id,
            bca.message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, fh_session_alias)
        ))

        # Step 1 - create algo order
        qty = "1000"
        limit = "1"
        lookup = "PAR_ST"

        act_order_ticket = Stubs.win_act_order_ticket
        config_vars = Stubs.custom_config
        act_order_book = Stubs.win_act_order_book
        common_win_act = Stubs.win_act

        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)

        quod_participant_strategy = order_ticket.add_quod_participation_strategy("Quod Participation")
        quod_participant_strategy.set_start_date("Now")
        quod_participant_strategy.set_end_date("Now", "0.9")
        quod_participant_strategy.set_percentage_volume('30')
        quod_participant_strategy.set_aggressivity("Neutral")

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)
        call(act_order_ticket.placeOrder, new_order_details.build())

        order_info_extraction = "getOrderInfo_1"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        main_order_details.set_filter(["Owner", config_vars["qf_trading_fe_user"]])

        main_order_status = ExtractionDetail("order_status", "Sts")
        main_order_id = ExtractionDetail("order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_status,
                                                                                                     main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        request = call(act_order_book.getOrdersDetails, main_order_details.request())
        call(common_win_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                         [verify_ent("Order Status", main_order_status.name, "Open")]))

        order_id = request[main_order_id.name]
        if not order_id:
            raise Exception("Order id is not returned")

        # Step 2 amend algo order

        act_order_book = Stubs.win_act_order_book

        order_amend = OrderTicketDetails()
        quod_participant_strategy_2 = order_amend.add_quod_participation_strategy("Quod Participation")
        quod_participant_strategy_2.set_percentage_volume('40')

        amend_order_details = ModifyOrderDetails()
        amend_order_details.set_default_params(base_request)
        amend_order_details.set_filter(["Order ID", order_id])
        amend_order_details.set_order_details(order_amend)

        call(act_order_book.amendOrder, amend_order_details.build())

        extraction_id = "getOrderAnalysisAlgoParameters"

        call(common_win_act.getOrderAnalysisAlgoParameters,
             order_analysis_algo_parameters_request(extraction_id, ["PercentageVolume"], {"Order ID": order_id}))
        call(common_win_act.verifyEntities, verification(extraction_id, "checking algo parameters",
                                                         [verify_ent("PercentageVolume", "PercentageVolume", "40.0")]))

        # Step 3 cancel algo order
        cancel_order_details = CancelOrderDetails()
        cancel_order_details.set_default_params(base_request)
        cancel_order_details.set_filter(["Order ID", order_id])
        cancel_order_details.set_comment("Order cancelled by script")
        cancel_order_details.set_cancel_children(True)

        call(act_order_book.cancelOrder, cancel_order_details.build())

        # Checking cancelled order status
        order_info_extraction_cancel = "getOrderInfo_cancelled"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction_cancel)
        main_order_details.set_filter(["Order ID", order_id])

        main_order_status = ExtractionDetail("order_status", "Sts")
        main_order_id = ExtractionDetail("order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_status,
                                                                                                     main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        call(act_order_book.getOrdersDetails, main_order_details.request())
        call(common_win_act.verifyEntities, verification(order_info_extraction_cancel, "checking order",
                                                     [ verify_ent("Order Status", main_order_status.name, "Cancelled")]))

        # step 4 check Audit for algo
        extraction_id = "getOrderAnalysisEvents"
        call(common_win_act.getOrderAnalysisEvents,
             create_order_analysis_events_request(extraction_id, {"Order ID": order_id}))

        vr = create_verification_request("checking order events", extraction_id, extraction_id)

        check_value(vr, "Event 1 Description contains", "event1.desc", "New User's Synthetic Order Received",
                    VerificationDetails.VerificationMethod.CONTAINS)

        check_value(vr, "Event 2 Description contains", "event2.desc", "last trade is 100@1",
                    VerificationDetails.VerificationMethod.CONTAINS)

        check_value(vr, "Event 3 Description contains", "event3.desc",
                    "User's Modification Received on the Synthetic Order",
                    VerificationDetails.VerificationMethod.CONTAINS)

        check_value(vr, "Event 4 Description contains", "event4.desc",
                    "User's Cancellation Received on the Synthetic Order",
                    VerificationDetails.VerificationMethod.CONTAINS)

        check_value(vr, "Events Count", "events.count", "4")
        call(common_win_act.verifyEntities, vr)

    except Exception as e:
        logging.error("Error execution", exc_info=True)
    rule_manager.remove_rule(nos)
    rule_manager.remove_rule(ocrr)
    rule_manager.remove_rule(ocr)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
