from google.protobuf.empty_pb2 import Empty

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
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs, RequestMDRefID, \
    TemplateQuodNOSRule
from custom import basic_custom_actions as bca
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails, ExtractMiddleOfficeBlotterValuesRequest, \
    AllocationsExtractionDetails

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
    case_name = "QAP-3351"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']

    NOS = simulator.createQuodNOSRule(
        request=TemplateQuodNOSRule(connection_id=ConnectionID(session_alias='fix-bs-eq-paris'), account="XPAR_CLIENT2"))

    print(NOS)

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:

        # Step 1

        order_ticket_dma1 = OrderTicketDetails()
        order_ticket_dma1.set_quantity('100')
        order_ticket_dma1.set_limit('100')
        order_ticket_dma1.buy()

        commissions_details = order_ticket_dma1.add_commissions_details()
        commissions_details.toggle_manual()
        commissions_details.add_commission(basis="Absolute", rate="5", amount="5")

        dma_order_details = NewOrderDetails()
        dma_order_details.set_lookup_instr('VETO')
        dma_order_details.set_order_details(order_ticket_dma1)
        dma_order_details.set_default_params(base_request)

        call(act.placeOrder, dma_order_details.build())

        extraction_id = "main_order"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["Owner", username])

        main_order_id = ExtractionDetail("main_order_id", "Order ID")
        main_order_status = ExtractionDetail("main_order_status", "Sts")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_status, main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        request = call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "Checking order",
                                                     [verify_ent("Order Status", main_order_status.name, "Open")]))

        block_order_id = request[main_order_id.name]
        if not block_order_id:
            raise Exception("Block order id is not returned")
        print("Block order id " + block_order_id)

    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe(case_id, session_id)
    Stubs.core.removeRule(NOS)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")