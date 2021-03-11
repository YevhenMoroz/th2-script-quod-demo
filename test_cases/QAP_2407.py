from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from stubs import Stubs
from win_gui_modules.wrappers import *
from logging import getLogger, INFO
from datetime import datetime
from copy import deepcopy
from custom.basic_custom_actions import timestamps, create_event, convert_to_request, message_to_grpc, client_orderid, \
    create_check_rule, filter_to_grpc
from win_gui_modules.utils import call, prepare_fe, set_session_id, get_base_request, close_fe
from th2_grpc_common.common_pb2 import ConnectionID, Direction
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from rule_management import RuleManager


logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "QAP-2407"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    rule_manager = RuleManager()
    common_act = Stubs.win_act
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    sell_side_connectivity = "gtwquod3"
    buy_side_connectivity = "fix-bs-eq-paris"
    nos_rule = rule_manager.add_NOS(buy_side_connectivity)
    ocr_rule = rule_manager.add_OCR(buy_side_connectivity)

    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)

    try:
        symbol_1 = "596"
        # Send Snapshots
        MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_1,
            connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
        )).MDRefID
        mdir_params_bid = {
            'MDReqID': MDRefID_1,
            'NoMDEntriesIR': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '30',
                    'MDEntrySize': '5000',
                    'MDUpdateAction': '0'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '40',
                    'MDEntrySize': '5000',
                    'MDUpdateAction': '0'
                }
            ]
        }
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', "fix-fh-eq-paris", case_id,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_bid, "fix-fh-eq-paris")
        ))

        algo_order_params = {
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '2',
            'OrderQty': 1500,
            'TimeInForce': '0',
            'Price': 36,
            'OrdType': '2',
            'ClOrdID': client_orderid(9),
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': 'FR0000125460_EUR',
                'SecurityID': 'FR0000125460',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'ComplianceID': 'FX5',
            'ClientAlgoPolicyID': 'QA_SORPING',
            'TargetStrategy': 1011
        }

        new_algo_order = Stubs.fix_act.placeOrderFIX(
            convert_to_request(
                'Send NewSingleOrder',
                sell_side_connectivity,
                case_id,
                message_to_grpc('NewOrderSingle', algo_order_params, sell_side_connectivity)
            ))
        checkpoint_1 = new_algo_order.checkpoint_id
        er_pending_params = {
            'Account': algo_order_params['Account'],
            'HandlInst': algo_order_params['HandlInst'],
            'Side': algo_order_params['Side'],
            'TimeInForce': algo_order_params['TimeInForce'],
            'OrdType': algo_order_params['OrdType'],
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': algo_order_params['TargetStrategy'],
            'ClOrdID': algo_order_params['ClOrdID'],
            'OrderID': new_algo_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'LeavesQty': algo_order_params['OrderQty'],
            'Instrument': algo_order_params['Instrument']
        }
        Stubs.verifier.submitCheckRule(
            create_check_rule(
                "Received Execution Report with OrdStatus = Pending",
                filter_to_grpc("ExecutionReport", er_pending_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, sell_side_connectivity, case_id
            )
        )
        er_new_params = deepcopy(er_pending_params)
        er_new_params['OrdStatus'] = er_new_params['ExecType'] = '0'
        er_new_params['Instrument'] = {
            'Symbol': 'FR0000125460_EUR',
            'SecurityExchange': 'XPAR'
        }
        Stubs.verifier.submitCheckRule(
            create_check_rule(
                "Received Execution Report with OrdStatus = New",
                filter_to_grpc("ExecutionReport", er_new_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, sell_side_connectivity, case_id
            )
        )

        new_order_bs_params = {
            'Account': algo_order_params['Account'],
            'HandlInst': '1',
            'Side': algo_order_params['Side'],
            'OrderQty': algo_order_params['OrderQty'],
            'TimeInForce': algo_order_params['TimeInForce'],
            'Price': algo_order_params['Price'],
            'OrdType': algo_order_params['OrdType'],
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'ClOrdID': '*',
            'ChildOrderID': '*',
            'TransactTime': '*',
            'Instrument': {
                'Symbol': 'AN',
                'SecurityID': 'FR0000125460',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'ExDestination': 'XPAR',

        }
        Stubs.verifier.submitCheckRule(
            create_check_rule(
                'NewOrderSingle transmitted >> PARIS',
                filter_to_grpc('NewOrderSingle', new_order_bs_params, ["ClOrdID"]),
                checkpoint_1, buy_side_connectivity, case_id
        ))

        er_new_bs_params = {
            'ClOrdID': '*',
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'CumQty': '0',
            'OrderQty': new_order_bs_params['OrderQty'],
            'OrdType': new_order_bs_params['OrdType'],
            'Side': new_order_bs_params['Side'],
            # 'LastPx': '0',
            'AvgPx': '0',
            'OrdStatus': '0',
            'ExecType': '0',
            'LeavesQty': '0',
            'Text': '*'
        }
        Stubs.verifier.submitCheckRule(
            create_check_rule(
                'ER NewOrderSingle transmitted << PARIS',
                filter_to_grpc('ExecutionReport', er_new_bs_params, ["ClOrdID", "OrdStatus"]),
                checkpoint_1, buy_side_connectivity,
                case_id,
                Direction.Value("SECOND")
            )
        )

        order_info_extraction = "getOrderInfo"

        ClOrdID = algo_order_params['ClOrdID']
        # ClOrdID = "133880250"

        child_order_1_order_id = ExtractionDetail("child_order_1.OrderID", "Order ID")
        child_order_1_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=child_order_1_order_id)
        )

        child_order_2_order_id = ExtractionDetail("child_order_2.OrderID", "Order ID")
        child_order_2_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=child_order_2_order_id)
        )

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        main_order_details.set_filter(["ClOrdID", ClOrdID])

        main_order_exec_pcy = ExtractionDetail("order.ExecPcy", "ExecPcy")
        main_order_price = ExtractionDetail("order.LmtPrice", "LmtPrice")
        main_order_qty = ExtractionDetail("order.Qty", "Qty")

        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[
                ExtractionDetail("order.ExecPcy", "ExecPcy"),
                ExtractionDetail("order.LmtPrice", "LmtPrice"),
                ExtractionDetail("order.Qty", "Qty"),
                ExtractionDetail("order.OrderID", "Order ID")
            ])
        main_order_details.add_single_order_info(
            OrderInfo.create(
                action=main_order_extraction_action,
                sub_order_details=OrdersDetails.create(order_info_list=[child_order_1_info, child_order_2_info])
            ))

        data = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
        child_1_order_id = data[child_order_1_order_id.name]
        logger.info(child_1_order_id)
        child_2_order_id = data[child_order_2_order_id.name]
        logger.info(child_2_order_id)

        call(common_act.verifyEntities, verification(order_info_extraction, "checking order", [
            verify_ent("Order ExecPcy", main_order_exec_pcy.name, "Synth (Quod LitDark)"),
            verify_ent("Order LmtPrice", main_order_price.name, "36"),
            verify_ent("Order Qty", main_order_qty.name, "1,500")
        ]))

        # check 1st child order

        extraction_id = "order.LitDark"

        child_order_1_1_exec_pcy = ExtractionDetail("child_order_1_1.ExecPcy", "ExecPcy")
        child_order_1_1_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=child_order_1_1_exec_pcy)
        )
        child_order_1_1_details = OrdersDetails.create(info=child_order_1_1_info)
        length_name = "child_order_1_1.length"
        child_order_1_1_details.extract_length(length_name)

        child_order_1_details = OrdersDetails()
        child_order_1_details.set_default_params(base_request)
        child_order_1_details.set_extraction_id(extraction_id)
        child_order_1_details.set_filter(["Order ID", child_1_order_id])

        child_order_1_exec_pcy = ExtractionDetail("child_order_1.ExecPcy", "ExecPcy")
        child_order_1_price = ExtractionDetail("child_order_1.LmtPrice", "LmtPrice")
        child_order_1_tif = ExtractionDetail("child_order_1.TIF", "TIF")
        child_order_1_qty = ExtractionDetail("child_order_1.Qty", "Qty")

        child_order_1_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[
                child_order_1_exec_pcy,
                child_order_1_tif,
                child_order_1_price,
                child_order_1_qty

            ])
        child_order_1_details.add_single_order_info(
            OrderInfo.create(
                action=child_order_1_extraction_action,
                sub_order_details=child_order_1_1_details
            ))

        call(Stubs.win_act_order_book.getChildOrdersDetails, child_order_1_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "Checking child orders", [
            verify_ent("Sub Order 1 Lvl 1 ExecPcy", child_order_1_exec_pcy.name, "Synth (Quod MultiListing)"),
            verify_ent("Sub Order 1 Lvl 1 TIF", child_order_1_tif.name, "Day"),
            verify_ent("Sub Order 1 Lvl 1 LmtPrice", child_order_1_price.name, "36"),
            verify_ent("Sub Order 1 Lvl 1 Qty", child_order_1_qty.name, "1,500"),
            verify_ent("Sub Order 1 Lvl 2 ExecPcy", child_order_1_1_exec_pcy.name, "DMA"),
            verify_ent("Sub order 1 Lvl 2 count", length_name, "1")
        ]))

        # check 2nd child order

        extraction_id = "order.DarkPool"

        child_order_2_1_tif = ExtractionDetail("child_order_2_1.TIF", "TIF")
        child_order_2_1_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=child_order_2_1_tif)
        )

        child_order_2_2_tif = ExtractionDetail("child_order_2_2.TIF", "TIF")
        child_order_2_2_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=child_order_2_2_tif)
        )
        child_order_2_sub_details = OrdersDetails.create(order_info_list=[child_order_2_1_info, child_order_2_2_info])
        length_name = "child_order_2_sub.length"
        child_order_2_sub_details.extract_length(length_name)

        child_order_2_details = OrdersDetails()
        child_order_2_details.set_default_params(base_request)
        child_order_2_details.set_extraction_id(extraction_id)
        child_order_2_details.set_filter(["Order ID", child_2_order_id])

        child_order_2_exec_pcy = ExtractionDetail("child_order_2.ExecPcy", "ExecPcy")
        child_order_2_extraction_action = ExtractionAction.create_extraction_action(
            extraction_detail=child_order_2_exec_pcy)
        child_order_2_details.add_single_order_info(
            OrderInfo.create(
                action=child_order_2_extraction_action,
                sub_order_details=child_order_2_sub_details
            ))

        call(Stubs.win_act_order_book.getChildOrdersDetails, child_order_2_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "Checking child orders", [
            verify_ent("Sub Order 2 Lvl 1 ExecPcy", child_order_2_exec_pcy.name, "Synth (Quod DarkPool)"),
            verify_ent("Sub Order 2 Lvl 2 child 1 TIF", child_order_2_1_tif.name, "ImmediateOrCancel"),
            verify_ent("Sub Order 2 Lvl 2 child 2 TIF", child_order_2_2_tif.name, "ImmediateOrCancel"),
            verify_ent("Sub order 2 Lvl 2 count", length_name, "2")
        ]))

        # Postcondition

        cancel_order_params = {
            'OrigClOrdID': algo_order_params['ClOrdID'],
            'ClOrdID': client_orderid(9),
            'Instrument': algo_order_params['Instrument'],
            'Side': algo_order_params['Side'],
            'TransactTime': datetime.utcnow().isoformat(),
            'OrderQty': algo_order_params['OrderQty'],
            'Text': 'Cancel order'
        }

        cancel_order = Stubs.fix_act.placeOrderCancelFIX(
            convert_to_request(
                'Send CancelOrderRequest',
                sell_side_connectivity,
                case_id,
                message_to_grpc('OrderCancelRequest', cancel_order_params, sell_side_connectivity),
            ))
        er_cancelled_params = deepcopy(er_new_params)
        er_cancelled_params['OrdStatus'] = er_cancelled_params['ExecType'] = '4'
        er_cancelled_params['LeavesQty'] = 0
        er_cancelled_params['ClOrdID'] = cancel_order_params['ClOrdID']
        er_cancelled_params['OrigClOrdID'] = algo_order_params['ClOrdID']

        Stubs.verifier.submitCheckRule(
            create_check_rule(
                "Received Execution Report with OrdStatus = Cancelled",
                filter_to_grpc('ExecutionReport', er_cancelled_params, ["ClOrdID", "OrdStatus"]),
                cancel_order.checkpoint_id, sell_side_connectivity, case_id
            )
        )
    except Exception:
        logger.error("Error execution", exc_info=True)
    rule_manager.remove_rule(nos_rule)
    rule_manager.remove_rule(ocr_rule)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
