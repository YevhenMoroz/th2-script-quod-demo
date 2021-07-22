import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from stubs import Stubs

from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe, close_fe, get_base_request, call
from win_gui_modules.order_book_wrappers import ManualExecutingDetails, OrdersDetails, ExtractionDetail, \
    ExtractionAction, OrderInfo, CompleteOrdersDetails
from win_gui_modules.wrappers import *
from rule_management import RuleManager
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails, ExtractMiddleOfficeBlotterValuesRequest, \
    AllocationsExtractionDetails
from custom.verifier import Verifier

# from test_cases.QAP_1560 import TestCase


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    fix_act = Stubs.fix_act
    act2 = Stubs.win_act_order_book


    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-2701"

    common_act = Stubs.win_act

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    #nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-paris", "MOClient", "XPAR", 5)


    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "MOClient")
        qty1 = "100"
        qty2 = "70"
        qty3 = "30"
        limit = "5"
        today = datetime.now()
        todayp2 = today + timedelta(days=2)
        todayp2 = todayp2.strftime('%Y%m%d')
        today = today.strftime('%Y%m%d')

        #create care market order
        cmo1_params = {
            'Account': 'MOClient',
            'HandlInst': '3',
            'Side': '1',
            'Price': '10',
            'OrderQty': qty1,
            'OrdType': '2',
            'TimeInForce': '0',
            'ClOrdID': bca.client_orderid(9),
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': 4,
                'SecurityExchange': 'XPAR'
            },
            'OrderCapacity': 'A',
            'Currency': 'EUR'
        }
        new_cmo1_order = fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                "Send new dma order", "gtwquod5", case_id,
                bca.message_to_grpc('NewOrderSingle', cmo1_params, "gtwquod5")
            ))

        call(common_act.acceptOrder, accept_order_request(session_id, case_id, "VETO", qty1, ""))

        # create manual execution
        service = Stubs.win_act_order_book

        manual_executing_details = ManualExecutingDetails(base_request)
        manual_executing_details.set_filter({"ClOrdID": cmo1_params['ClOrdID']})
        # manual_executing_details.set_row_number(1)

        executions_details = manual_executing_details.add_executions_details()
        # executions_details.set_quantity(qty)
        # executions_details.set_price(limit)
        executions_details.set_executing_firm("ExecutingFirm")
        executions_details.set_contra_firm("Contra_Firm")
        executions_details.set_last_capacity("Agency")

        call(service.manualExecution, manual_executing_details.build())

        # verify
        middle_office_service = Stubs.win_act_middle_office_service

        extraction_id = "main_order"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["ClOrdID", cmo1_params['ClOrdID']])

        main_order_status = ExtractionDetail("order_status", "Sts")
        main_order_exec_status = ExtractionDetail("exec_status", "ExecSts")

        main_order_id = ExtractionDetail("main_order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=
                                                                                 [main_order_status,
                                                                                  main_order_exec_status,
                                                                                  main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        request = call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                     [verify_ent("Order Status", main_order_status.name, "Open"),
                                                      verify_ent("Order Exec Status",
                                                                 main_order_exec_status.name, "Filled")]))

        #complete order
        #service = Stubs.win_act_order_book

        complete_orders_details = CompleteOrdersDetails(base_request)
        complete_orders_details.set_filter({"ClOrdID": cmo1_params['ClOrdID']})
        # complete_orders_details.set_selected_row_count(2)

        call(service.completeOrders, complete_orders_details.build())

        #verify
        extraction_id = "main_order"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["ClOrdID", cmo1_params['ClOrdID']])

        main_order_post_trade_status = ExtractionDetail("post_trade_status", "PostTradeStatus")
        main_order_id = ExtractionDetail("main_order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_post_trade_status, main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                     [verify_ent("Order Post Trade Status",
                                                                 main_order_post_trade_status.name, "ReadyToBook")
                                                      ]))
        
        # # Checkpoint3 creation
        # checkpoint_response3 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        # checkpoint_id3 = checkpoint_response3.checkpoint

        #book order
        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)
        modify_request.set_filter(["ClOrdID", cmo1_params['ClOrdID']])
        # modify_request.set_selected_row_count(4)

        extraction_details = modify_request.add_extraction_details()
        extraction_details.set_extraction_id("BookExtractionId")
        extraction_details.extract_net_price("book.netPrice")
        extraction_details.extract_net_amount("book.netAmount")
        extraction_details.extract_total_comm("book.totalComm")
        extraction_details.extract_gross_amount("book.grossAmount")
        extraction_details.extract_total_fees("book.totalFees")
        extraction_details.extract_agreed_price("book.agreedPrice")

        call(middle_office_service.bookOrder, modify_request.build())

        #verify
        extraction_id = "main_order"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["ClOrdID", cmo1_params['ClOrdID']])

        main_order_post_trade_status = ExtractionDetail("post_trade_status", "PostTradeStatus")
        main_order_id = ExtractionDetail("main_order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_post_trade_status, main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        request = call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                     [verify_ent("Order PostTradeStatus",
                                                                 main_order_post_trade_status.name, "Booked")]))

        block_order_id = request[main_order_id.name]
        if not block_order_id:
            raise Exception("Block order id is not returned")
        print("Block order id " + block_order_id)

        ext_id = "MiddleOfficeExtractionId"
        middle_office_service = Stubs.win_act_middle_office_service
        extract_request = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        extract_request.set_extraction_id(ext_id)
        extract_request.set_filter(["Order ID", block_order_id])
        block_order_status = ExtractionDetail("middleOffice.status", "Status")
        block_order_match_status = ExtractionDetail("middleOffice.matchStatus", "Match Status")
        block_order_summary_status = ExtractionDetail("middleOffice.summaryStatus", "Summary Status")
        extract_request.add_extraction_details(
            [block_order_status, block_order_match_status, block_order_summary_status])
        request = call(middle_office_service.extractMiddleOfficeBlotterValues, extract_request.build())

        verifier = Verifier(case_id)

        verifier.set_event_name("Checking block order")
        verifier.compare_values("Order Status", "ApprovalPending", request[block_order_status.name])
        verifier.compare_values("Order Match Status", "Unmatched", request[block_order_match_status.name])
        verifier.compare_values("Order Summary Status", "", request[block_order_summary_status.name])
        verifier.verify()

        #verify
        extract_request = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        ext_id_allocate = "MiddleOfficeExtractionId3"
        extract_request_allocate = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        extract_request_allocate.set_extraction_id(ext_id_allocate)
        block_order_status = ExtractionDetail("middleOffice.status", "Status")
        block_order_match_status = ExtractionDetail("middleOffice.matchStatus", "Match Status")
        block_order_summary_status = ExtractionDetail("middleOffice.summaryStatus", "Summary Status")
        block_order_conf_service = ExtractionDetail("middleOffice.confService", "Conf Service")
        extract_request.add_extraction_details([block_order_status, block_order_match_status, block_order_summary_status, block_order_conf_service])
        request_allocate = call(middle_office_service.extractMiddleOfficeBlotterValues, extract_request.build())

        verifier = Verifier(case_id)

        verifier.set_event_name("Checking block order after allocate")
        verifier.compare_values("Order Status", "Accepted", request_allocate[block_order_status.name])
        verifier.compare_values("Order Match Status", "Matched", request_allocate[block_order_match_status.name])
        verifier.compare_values("Order Summary Status", "MatchedAgreed", request_allocate[block_order_summary_status.name])
        verifier.compare_values("Order Conf Service", "CTM",
                                request_allocate[block_order_conf_service.name])
        verifier.verify()

        # # Check allocations blotter for MOClientSA1
        #
        # middle_office_service = Stubs.win_act_middle_office_service
        #
        # extract_request = AllocationsExtractionDetails(base=base_request)
        # extract_request.set_block_filter({"Order ID": block_order_id})
        # extract_request.set_allocations_filter({"Account ID": "MOClientSA1"})
        # allocate_status = ExtractionDetail("middleOffice.status", "Status")
        # allocate_account_id = ExtractionDetail("middleOffice.account_id", "Account ID")
        # allocate_status_match_status = ExtractionDetail("middleOffice.match_status", "Match Status")
        # order_details = extract_request.add_order_details()
        # order_details.add_extraction_details([allocate_status, allocate_account_id,
        #                                       allocate_status_match_status])
        # request_allocate_blotter = call(middle_office_service.extractAllocationsTableData, extract_request.build())
        #
        # verifier = Verifier(case_id)
        #
        # verifier.set_event_name("Checking allocate blotter")
        # verifier.compare_values("Allocation Status", "Affirmed", request_allocate_blotter[allocate_status.name])
        # verifier.compare_values("Allocation Account ID", "MOClientSA1", request_allocate_blotter[allocate_account_id.name])
        # verifier.compare_values("Allocation Match Status", "Matched", request_allocate_blotter[allocate_status_match_status.name])
        # verifier.verify()


    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
