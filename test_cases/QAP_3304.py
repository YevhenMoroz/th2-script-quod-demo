from custom.verifier import Verifier
from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, ExtractionDetail, \
    CancelOrderDetails, ExtractionAction
from stubs import Stubs
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
from custom.basic_custom_actions import timestamps, create_event
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
import logging
from rule_management import RuleManager
from datetime import datetime
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs, RequestMDRefID
from custom import basic_custom_actions as bca
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails, ExtractMiddleOfficeBlotterValuesRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    fix_act = Stubs.fix_act
    act = Stubs.win_act_order_ticket
    act2 = Stubs.win_act_order_book
    common_act = Stubs.win_act
    simulator = Stubs.simulator

    bs_paris = 'fix-bs-eq-paris'
    bs_trqx = 'fix-bs-eq-trqx'

    seconds, nanos = timestamps()  # Store case start time
    case_name = "QAP-3304"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:

        case_params = {
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'fix-bs-eq-paris',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'MOClient',
            'HandlInst': '1',
            'Side': '2',
            'OrderQty': '100',
            'OrdType': '2',
            'Price': '100',
            'TimeInForce': '0',
            'DeliverToCompID': 'PARIS',
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': 4,
                'SecurityExchange': 'XPAR'
            }
        }

        trade_rule_1 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
            connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
            no_party_ids=[
                TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
                TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
                TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
            ],
            cum_qty=100,
            mask_as_connectivity="fix-fh-eq-paris",
            md_entry_size={500: 0},
            md_entry_px={30: 25},
            symbol={"XPAR": '1224'}))

        dma_order_params = {
            'Account': case_params['Account'],
            'HandlInst': case_params['HandlInst'],
            'Side': case_params['Side'],
            'OrderQty': case_params['OrderQty'],
            'TimeInForce': case_params['TimeInForce'],
            'Price': case_params['Price'],
            'OrdType': case_params['OrdType'],
            'ClOrdID': bca.client_orderid(9),
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': case_params['Instrument'],
            'OrderCapacity': 'A',
            'Currency': 'EUR'
        }
        new_dma_order = fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                "Send new dma order", "gtwquod5", case_id,
                bca.message_to_grpc('NewOrderSingle', dma_order_params, "gtwquod5")
            ))

        Stubs.core.removeRule(trade_rule_1)

        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)
        modify_request.set_filter(["ClOrdID", dma_order_params['ClOrdID']])

        call(middle_office_service.bookOrder, modify_request.build())

        extraction_id = "main_order"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["ClOrdID", dma_order_params['ClOrdID']])

        main_order_post_trade_status = ExtractionDetail("post_trade_status", "PostTradeStatus")
        main_order_id = ExtractionDetail("main_order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_post_trade_status, main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        request = call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                     [verify_ent("Order PostTradeStatus", main_order_post_trade_status.name, "Booked")]))

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
        extract_request.add_extraction_details([block_order_status, block_order_match_status, block_order_summary_status])
        request = call(middle_office_service.extractMiddleOfficeBlotterValues, extract_request.build())

        verifier = Verifier(case_id)

        verifier.set_event_name("Checking block order")
        verifier.compare_values("Order Status", "ApprovalPending", request[block_order_status.name])
        verifier.compare_values("Order Match Status", "Unmatched", request[block_order_match_status.name])
        verifier.compare_values("Order Summary Status", "", request[block_order_summary_status.name])
        verifier.verify()

        # Step 2 UnBook Order

        modify_request = ModifyTicketDetails(base=base_request)
        modify_request.set_filter(["ClOrdID", dma_order_params['ClOrdID']])
        call(middle_office_service.unBookOrder, modify_request.build())

        extraction_id = "main_order"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["ClOrdID", dma_order_params['ClOrdID']])

        main_order_post_trade_status = ExtractionDetail("post_trade_status", "PostTradeStatus")
        main_order_id = ExtractionDetail("main_order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_post_trade_status, main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                     [verify_ent("Order PostTradeStatus",
                                                                 main_order_post_trade_status.name, "ReadyToBook")]))

        ext_id_unbook = "MiddleOfficeExtractionId2"
        middle_office_service_unbook = Stubs.win_act_middle_office_service
        extract_request_unbook = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        extract_request_unbook.set_extraction_id(ext_id_unbook)
        block_order_status = ExtractionDetail("middleOffice.status", "Status")
        block_order_match_status = ExtractionDetail("middleOffice.matchStatus", "Match Status")
        block_order_summary_status = ExtractionDetail("middleOffice.summaryStatus", "Summary Status")
        extract_request_unbook.add_extraction_details(
            [block_order_status, block_order_match_status, block_order_summary_status])
        request_unbook = call(middle_office_service_unbook.extractMiddleOfficeBlotterValues, extract_request_unbook.build())

        extraction_id = "main_order"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["ClOrdID", dma_order_params['ClOrdID']])

        main_order_post_trade_status = ExtractionDetail("post_trade_status", "PostTradeStatus")
        main_order_id = ExtractionDetail("main_order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_post_trade_status, main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                     [verify_ent("Order PostTradeStatus",
                                                                 main_order_post_trade_status.name, "ReadyToBook")]))

        verifier = Verifier(case_id)

        verifier.set_event_name("Checking block order")
        verifier.compare_values("Order Status", "Canceled", request_unbook[block_order_status.name])
        verifier.compare_values("Order Match Status", "Unmatched", request_unbook[block_order_match_status.name])
        verifier.compare_values("Order Summary Status", "", request_unbook[block_order_summary_status.name])
        verifier.verify()

    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")