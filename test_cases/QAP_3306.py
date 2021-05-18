import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe, close_fe, get_base_request, call
from win_gui_modules.order_book_wrappers import ManualExecutingDetails, OrdersDetails, ExtractionDetail, \
    ExtractionAction, OrderInfo
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
    act2 = Stubs.win_act_order_book


    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-3306"

    common_act = Stubs.win_act

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
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "MOClient")
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
            'OrdType': '2',
            'Price': '20',
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

        call(common_act.acceptOrder, accept_order_request(session_id, case_id, "VETO", qty1, ""))

        # create care market order
        cmo2_params = {
            'Account': 'MOClient',
            'HandlInst': '3',
            'Side': '2',
            'OrderQty': qty2,
            'OrdType': '1',
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
        call(common_act.acceptOrder, accept_order_request(session_id, case_id, "VETO", qty2, ""))

        # create care market order
        cmo3_params = {
            'Account': 'MOClient',
            'HandlInst': '3',
            'Side': '2',
            'OrderQty': qty3,
            'OrdType': '1',
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
        call(common_act.acceptOrder, accept_order_request(session_id, case_id, "VETO", qty3, ""))

        # Checkpoint1 creation
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint

        # create manual cross1
        test = cmo1_params['ClOrdID']+" "+cmo2_params['ClOrdID']
        service = Stubs.win_act_order_book

        manual_cross_details = ManualCrossDetails(base_request)
        base_data = BaseTableDataRequest(base=base_request)
        #base_data.set_filter_dict({"ClOrdID": test})
        #manual_cross_details.set_filter_dict({"ClOrdID": test})
        #manual_cross_details.set_filter({'NIN': '111111', 'Client': 'MOClient'})
        manual_cross_details.set_selected_rows([3, 2])

        manual_cross_details.set_quantity("70")
        manual_cross_details.set_price("5")
        manual_cross_details.set_last_mkt("XPAR")
        manual_cross_details.set_capacity("Agency")

        call(service.manualCross, manual_cross_details.build())

        # verify
        # extraction_id = "main_order"
        # main_order_details = OrdersDetails()
        # main_order_details.set_default_params(base_request)
        # main_order_details.set_extraction_id(extraction_id)
        # main_order_details.set_filter(["ClOrdID", cmo1_params['ClOrdID']])
        #
        # main_order_exec_status = ExtractionDetail("exec_status", "ExecSts")
        # main_order_id = ExtractionDetail("main_order_id", "Order ID")
        # main_order_extraction_action = ExtractionAction.create_extraction_action(
        #     extraction_details=[main_order_exec_status, main_order_id])
        # main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))
        #
        # call(act2.getOrdersDetails, main_order_details.request())
        # call(common_act.verifyEntities, verification(extraction_id, "checking order",
        #                                              [verify_ent("Order Exec Status",
        #                                                          main_order_exec_status.name, "Filled")]))

        # extraction_id = "order_details"
        # order2_details = OrdersDetails()
        # order2_details.set_default_params(base_request)
        # order2_details.set_extraction_id(extraction_id)
        # order2_details.set_filter(["ClOrdID", cmo2_params['ClOrdID']])
        #
        # order2_status = ExtractionDetail("order_status", "Sts")
        # order2_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order2_status])
        # order2_details.add_single_order_info(OrderInfo.create(action=order2_extraction_action))
        #
        # request = call(act2.getOrdersDetails, order2_details.request())
        # call(common_act.verifyEntities, verification(extraction_id, "checking order",
        #                                              [verify_ent("ExecStatus", order2_status.name, "Filled")]))

        # verify execution report
        execution_report1_params = {
            'ClOrdID': cmo1_params['ClOrdID'],
            'OrderID': cmo1_params['ClOrdID'],
            # 'ExecID': '*',
            # 'TransactTime': '*',
            # 'CumQty': '0',
            # 'SettlDate': todayp2,
            #
            # 'OrderQtyData': {
            #     'OrderQty': qty
            # },
            # 'Instrument': {
            #     'SecurityDesc': '*',
            #     'Symbol': 'VETO',
            #     'SecurityIDSource': '4',
            #     'SecurityID': 'FR0004186856',
            #     'SecurityExchange': 'XPAR',
            #
            # },
            # 'OrdType': '2',
            # 'Side': '1',
            # 'AvgPx': '0',
            'OrdStatus': '1',
            'ExecType': 'F',
            'LeavesQty': '30',
            # 'Price': limit,
            # 'TimeInForce': '0'
        }

        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Execution Report",
                bca.filter_to_grpc_nfu("ExecutionReport", execution_report1_params, ['ClOrdID']),
                checkpoint_id1, 'fix-ss-back-office', case_id
            )
        )

        # verify execution report
        execution_report2_params = {
            'ClOrdID': cmo2_params['ClOrdID'],
            'OrderID': cmo2_params['ClOrdID'],
            # 'ExecID': '*',
            # 'TransactTime': '*',
            # 'CumQty': '0',
            # 'SettlDate': todayp2,
            #
            # 'OrderQtyData': {
            #     'OrderQty': qty
            # },
            # 'Instrument': {
            #     'SecurityDesc': '*',
            #     'Symbol': 'VETO',
            #     'SecurityIDSource': '4',
            #     'SecurityID': 'FR0004186856',
            #     'SecurityExchange': 'XPAR',
            #
            # },
            # 'OrdType': '2',
            # 'Side': '1',
            # 'AvgPx': '0',
            'OrdStatus': '1',
            'ExecType': 'F',
            'LeavesQty': '0',
            # 'Price': limit,
            # 'TimeInForce': '0'
        }

        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Execution Report",
                bca.filter_to_grpc_nfu("ExecutionReport", execution_report2_params, ['ClOrdID']),
                checkpoint_id1, 'fix-ss-back-office', case_id
            )
        )

        # Checkpoint2 creation
        checkpoint_response2 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id2 = checkpoint_response2.checkpoint

        # create manual cross2
        service = Stubs.win_act_order_book

        manual_cross_details = ManualCrossDetails(base_request)
        # manual_cross_details.set_filter()
        #manual_cross_details.set_filter({'NIN': '111111', 'Client': 'MOClient'})
        manual_cross_details.set_selected_rows([3, 1])

        manual_cross_details.set_quantity("30")
        manual_cross_details.set_price("7")
        manual_cross_details.set_last_mkt("XPAR")
        manual_cross_details.set_capacity("Agency")

        call(service.manualCross, manual_cross_details.build())

        # # verify
        # extraction_id = "order_details"
        # order1_details = OrdersDetails()
        # order1_details.set_default_params(base_request)
        # order1_details.set_extraction_id(extraction_id)
        # order1_details.set_filter(["ClOrdID", cmo1_params['ClOrdID']])
        #
        # order1_status = ExtractionDetail("order_status", "Sts")
        # order1_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order1_status])
        # order1_details.add_single_order_info(OrderInfo.create(action=order1_extraction_action))
        #
        # request = call(act2.getOrdersDetails, order1_details.request())
        # call(common_act.verifyEntities, verification(extraction_id, "checking order",
        #                                              [verify_ent("ExecStatus", order1_status.name, "Filled")]))

        # extraction_id = "order_details"
        # order3_details = OrdersDetails()
        # order3_details.set_default_params(base_request)
        # order3_details.set_extraction_id(extraction_id)
        # order3_details.set_filter(["ClOrdID", cmo3_params['ClOrdID']])
        #
        # order3_status = ExtractionDetail("order_status", "Sts")
        # order3_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order3_status])
        # order3_details.add_single_order_info(OrderInfo.create(action=order3_extraction_action))
        #
        # request = call(act2.getOrdersDetails, order3_details.request())
        # call(common_act.verifyEntities, verification(extraction_id, "checking order",
        #                                              [verify_ent("ExecStatus", order3_status.name, "Filled")]))

        # verify execution report
        execution_report3_params = {
            'ClOrdID': cmo1_params['ClOrdID'],
            'OrderID': cmo1_params['ClOrdID'],
            # 'ExecID': '*',
            # 'TransactTime': '*',
            # 'CumQty': '0',
            # 'SettlDate': todayp2,
            #
            # 'OrderQtyData': {
            #     'OrderQty': qty
            # },
            # 'Instrument': {
            #     'SecurityDesc': '*',
            #     'Symbol': 'VETO',
            #     'SecurityIDSource': '4',
            #     'SecurityID': 'FR0004186856',
            #     'SecurityExchange': 'XPAR',
            #
            # },
            # 'OrdType': '2',
            # 'Side': '1',
            # 'AvgPx': '0',
            'OrdStatus': '1',
            'ExecType': 'F',
            'LeavesQty': '0',
            # 'Price': limit,
            # 'TimeInForce': '0'
        }

        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Execution Report",
                bca.filter_to_grpc_nfu("ExecutionReport", execution_report3_params, ['ClOrdID', 'LeavesQty']),
                checkpoint_id2, 'fix-ss-back-office', case_id
            )
        )

        # verify execution report
        execution_report4_params = {
            'ClOrdID': cmo3_params['ClOrdID'],
            'OrderID': cmo3_params['ClOrdID'],
            # 'ExecID': '*',
            # 'TransactTime': '*',
            # 'CumQty': '0',
            # 'SettlDate': todayp2,
            #
            # 'OrderQtyData': {
            #     'OrderQty': qty
            # },
            # 'Instrument': {
            #     'SecurityDesc': '*',
            #     'Symbol': 'VETO',
            #     'SecurityIDSource': '4',
            #     'SecurityID': 'FR0004186856',
            #     'SecurityExchange': 'XPAR',
            #
            # },
            # 'OrdType': '2',
            # 'Side': '1',
            # 'AvgPx': '0',
            'OrdStatus': '1',
            'ExecType': 'F',
            'LeavesQty': '0',
            # 'Price': limit,
            # 'TimeInForce': '0'
        }

        Stubs.verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Execution Report",
                bca.filter_to_grpc_nfu("ExecutionReport", execution_report4_params, ['ClOrdID']),
                checkpoint_id2, 'fix-ss-back-office', case_id
            )
        )

        #rule_manager.remove_rule(nos_rule2)
        rule_manager.remove_rule(nos_rule)

    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")