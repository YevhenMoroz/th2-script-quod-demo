import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe, close_fe, get_base_request, call
from win_gui_modules.order_book_wrappers import ManualExecutingDetails
from win_gui_modules.order_book_wrappers import ManualCrossDetails
from win_gui_modules.order_book_wrappers import CompleteOrdersDetails
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.wrappers import *
from rule_management import RuleManager

# from test_cases.QAP_1560 import TestCase


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    fix_act = Stubs.fix_act
    rule_manager = RuleManager()

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-3306"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    session_id = set_session_id()
    # set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    #nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-paris", "MOClient", "XPAR", 5)


    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:
        qty1 = "100"
        qty2 = "70"
        qty3 = "30"
        limit = "5"

        #create care market order
        cmo1_params = {
            'Account': 'MOClient',
            'HandlInst': '3',
            'Side': '1',
            'OrderQty': qty1,
            'OrdType': '1',
            'SettlType': '0',
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
        new_dma_order = fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                "Send new dma order", "gtwquod5", case_id,
                bca.message_to_grpc('NewOrderSingle', cmo1_params, "gtwquod5")
            ))

        # create care market order
        cmo2_params = {
            'Account': 'MOClient',
            'HandlInst': '3',
            'Side': '2',
            'OrderQty': qty2,
            'OrdType': '2',
            'Price': limit,
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
        new_dma_order = fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                "Send new dma order", "gtwquod5", case_id,
                bca.message_to_grpc('NewOrderSingle', cmo2_params, "gtwquod5")
            ))

        # create care market order
        cmo3_params = {
            'Account': 'MOClient',
            'HandlInst': '3',
            'Side': '2',
            'OrderQty': qty3,
            'OrdType': '2',
            'Price': limit,
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
        new_dma_order = fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                "Send new dma order", "gtwquod5", case_id,
                bca.message_to_grpc('NewOrderSingle', cmo3_params, "gtwquod5")
            ))

        # create manual cross1
        service = Stubs.win_act_order_book

        manual_cross_details = ManualCrossDetails(base_request)
        # manual_cross_details.set_filter()
        manual_cross_details.set_selected_rows([3, 2])

        manual_cross_details.set_quantity("70")
        manual_cross_details.set_price("5")
        manual_cross_details.set_last_mkt("XPAR")
        manual_cross_details.set_capacity("Agency")

        call(service.manualCross, manual_cross_details.build())

        # create manual cross2
        service = Stubs.win_act_order_book

        manual_cross_details = ManualCrossDetails(base_request)
        # manual_cross_details.set_filter()
        manual_cross_details.set_selected_rows([3, 1])

        manual_cross_details.set_quantity("30")
        manual_cross_details.set_price("7")
        manual_cross_details.set_last_mkt("XPAR")
        manual_cross_details.set_capacity("Agency")

        call(service.manualCross, manual_cross_details.build())

        #rule_manager.remove_rule(nos_rule2)

    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")