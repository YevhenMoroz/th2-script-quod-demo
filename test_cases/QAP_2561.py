import logging
from copy import deepcopy
from time import sleep
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Direction
from stubs import Stubs
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodNOSRule, TemplateQuodOCRRRule, TemplateQuodOCRRule
from th2_grpc_common.common_pb2 import ConnectionID

from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe_2, close_fe_2
from win_gui_modules.wrappers import set_base, create_verification_request, check_value
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, \
    ExtractionDetail, ExtractionAction

from google.protobuf.empty_pb2 import Empty

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier

    # Rules
    simulator = Stubs.simulator
    conn = ConnectionID(session_alias='fix-bs-eq-paris')
    NOS = simulator.createQuodNOSRule(request=TemplateQuodNOSRule(connection_id=conn))
    OCRR = simulator.createQuodOCRRRule(request=TemplateQuodOCRRRule(connection_id=conn))
    OCR = simulator.createQuodOCRRule(request=TemplateQuodOCRRule(connection_id=conn))

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-2561"
    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'TraderConnectivity2': 'fix-bs-eq-paris',
        'SenderCompID': 'QUOD3',
        'TargetCompID': 'QUODFX_UAT',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '1',
        'OrderQty': '400',
        'OrdType': '2',
        'Price': '20',
        'NewPrice': '25',
        'TimeInForce': '0',
        'Instrument': {
            'Symbol': 'FR0010542647_EUR',
            'SecurityID': 'FR0010542647',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        },
        'TargetStrategy': 1004
    }
    reusable_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR'
    }

    case_id = bca.create_event(case_name, report_id)

    new_iceberg_order_params = {
        **reusable_params,
        'Instrument': case_params['Instrument'],
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'OrderQty': case_params['OrderQty'],
        'Price': case_params['Price'],
        'ExDestination': 'XPAR',
        'ComplianceID': 'FX5',
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'F_ShortCode': '17536',
        'StrategyName': 'ICEBERG',
        'DisplayInstruction': {
            'DisplayQty': '50'
        },
        'TargetStrategy': case_params['TargetStrategy']
    }

    logger.debug(f"Send new order with ClOrdID = {new_iceberg_order_params['ClOrdID']}")
    new_iceberg_order = act.placeOrderFIX(
        bca.convert_to_request(
            "Send NewIcebergOrder",
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', new_iceberg_order_params, case_params['TraderConnectivity'])
        ))

    checkpoint = new_iceberg_order.checkpoint_id

    pending_er_params = {
        **reusable_params,
        'OrderQty': new_iceberg_order_params['OrderQty'],
        'Price': new_iceberg_order_params['Price'],
        'ClOrdID': new_iceberg_order_params['ClOrdID'],
        'OrderID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_iceberg_order_params['OrderQty'],
        'Instrument': case_params['Instrument'],
        'NoParty': '*',
        'NoStrategyParameters': [{'StrategyParameterName': 'ReleasedNbr',
                                  'StrategyParameterType': '1', 'StrategyParameterValue': '1'},
                                 {'StrategyParameterName': 'ReleasedQty',
                                  'StrategyParameterType': '6', 'StrategyParameterValue': '400'}],
        'MaxFloor': '50',
        'ExecID': '*'
    }

    logger.debug("Verify received Execution Report (OrdStatus = Pending)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            "ER Pending NewOrderSingle Received",
            bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
            checkpoint,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    new_er_params = deepcopy(pending_er_params)
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['Instrument'] = case_params['Instrument']
    new_er_params['ExecRestatementReason'] = '4'
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Verify received Execution Report (OrdStatus = New)",
            bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
            checkpoint,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    instrument_bs = {
        'SecurityType': 'CS',
        'Symbol': 'RSC',
        'SecurityID': case_params['Instrument']['SecurityID'],
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    nos_bs_params = {
        **reusable_params,
        'HandlInst': '1',
        'OrderQty': new_iceberg_order_params['DisplayInstruction']['DisplayQty'],
        'Price': case_params['Price'],
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'TransactTime': '*',
        'IClOrdIdCO': new_iceberg_order_params['IClOrdIdCO'],
        'IClOrdIdAO': new_iceberg_order_params['IClOrdIdAO'],
        'Instrument': instrument_bs,
        'ExDestination': new_iceberg_order_params['ExDestination']
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            'NewOrderSingle transmitted >> PARIS',
            bca.filter_to_grpc('NewOrderSingle', nos_bs_params, ["ClOrdID"]),
            checkpoint,
            case_params['TraderConnectivity2'],
            case_id
        )
    )

    er_bs_params = {
        'ClOrdID': '*',
        'OrderID': '*',
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'OrderQty': nos_bs_params['OrderQty'],
        'OrdType': case_params['OrdType'],
        'Side': case_params['Side'],
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '0',
        'LeavesQty': '0',
        'Text': '*'
    }

    logger.debug("Verify received Execution Report (OrdStatus = New)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'ER NewOrderSingle transmitted << PARIS',
            bca.filter_to_grpc('ExecutionReport', er_bs_params, ["ClOrdID", "OrdStatus"]),
            checkpoint,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        )
    )

    # GUI section
    # Step 1

    # case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    act_order_book = Stubs.win_act_order_book
    common_win_act = Stubs.win_act

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    try:
        order_info_extraction = "getOrderInfo"
        order_exec_pcy = ExtractionDetail("order.ExecPcy", "ExecPcy")
        order_qty = ExtractionDetail("order.Qty", "Qty")
        order_disp_qty = ExtractionDetail("order.DisplQty", "DisplQty")

        order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[order_exec_pcy, order_qty, order_disp_qty])
        main_order_info = OrderInfo.create(action=order_extraction_action)

        main_co_details = OrdersDetails()
        main_co_details.set_default_params(base_request)
        main_co_details.set_extraction_id(order_info_extraction)
        main_co_details.add_single_order_info(main_order_info)
        main_co_details.set_filter(["ClOrdID", new_iceberg_order_params['ClOrdID']])

        call(act_order_book.getOrdersDetails, main_co_details.request())

        vr = create_verification_request("checking order", order_info_extraction)
        check_value(vr, "Order ExecPcy", order_exec_pcy.name, "Synth (Quod Split Manager)")
        check_value(vr, "Order Qty", order_qty.name, "400")
        check_value(vr, "Order DisplayQty", order_disp_qty.name, "50")
        call(common_win_act.verifyEntities, vr)

        # Step 2
        # Check child orders

        extraction_id = "order.algo_split_man"

        # sub_order_1_lv2_qty = ExtractionDetail("subOrder_1_lv2.Qty", "Qty")
        # sub_order_1_lv2_exec_pcy = ExtractionDetail("subOrder_1_lv2.ExecPcy", "ExecPcy")
        # sub_order_1_lv2_ext_action = ExtractionAction.create_extraction_action(
        #     extraction_details=[sub_order_1_lv2_qty, sub_order_1_lv2_exec_pcy])
        # sub_order_1_lv2_info = OrderInfo.create(action=sub_order_1_lv2_ext_action)
        #
        # sub_order_2_lv2_qty = ExtractionDetail("subOrder_2_lv2.Qty", "Qty")
        # sub_order_2_lv2_exec_pcy = ExtractionDetail("subOrder_2_lv2.ExecPcy", "ExecPcy")
        # sub_order_2_lv2_ext_action = ExtractionAction.create_extraction_action(
        #     extraction_details=[sub_order_2_lv2_qty, sub_order_2_lv2_exec_pcy])
        # sub_order_2_lv2_info = OrderInfo.create(action=sub_order_2_lv2_ext_action)
        #
        # lvl2_count = "subOrders_lv2.length"
        sub_order_1_lv1_qty = ExtractionDetail("subOrder_lv1.Qty", "Qty")
        sub_order_1_lv1_displ_qty = ExtractionDetail("subOrder_lv1.DisplQty", "DisplQty")
        sub_order_1_lv1_exec_pcy = ExtractionDetail("subOrder_lv1.ExecPcy", "ExecPcy")
        sub_order_1_lv1_ext_action = ExtractionAction.create_extraction_action(
            extraction_details=[sub_order_1_lv1_qty, sub_order_1_lv1_displ_qty, sub_order_1_lv1_exec_pcy])
        # sub_lv2_details = OrdersDetails.create(order_info_list=[sub_order_1_lv2_info, sub_order_2_lv2_info])
        # sub_lv2_details.extract_length(lvl2_count)

        # sub_1_lv1_info = OrderInfo.create(action=sub_order_1_lv1_ext_action, sub_order_details=sub_lv2_details)
        sub_1_lv1_info = OrderInfo.create(action=sub_order_1_lv1_ext_action) # remove it later!

        sub_1_lv1_details = OrdersDetails.create(info=sub_1_lv1_info)
        main_order_info = OrderInfo.create(sub_order_details=sub_1_lv1_details)

        main_co_details = OrdersDetails()
        main_co_details.set_default_params(base_request)
        main_co_details.set_extraction_id(extraction_id)
        main_co_details.add_single_order_info(main_order_info)
        main_co_details.set_filter(["ClOrdID", new_iceberg_order_params['ClOrdID']])

        call(act_order_book.getOrdersDetails, main_co_details.request())

        vr = create_verification_request("checking order", extraction_id)
        check_value(vr, "Sub Lvl 1 Qty", sub_order_1_lv1_qty.name, "400")
        check_value(vr, "Sub Lvl 1 Display Qty", sub_order_1_lv1_displ_qty.name, "50")
        check_value(vr, "Sub Lvl 1 ExecPcy", sub_order_1_lv1_exec_pcy.name, "Synthetic")
        # check_value(vr, "Sub 1 Lvl 2 Qty", sub_order_1_lv2_qty.name, "45")
        # check_value(vr, "Sub 1 Lvl 2 ExecPcy", sub_order_1_lv2_exec_pcy.name, "DMA")
        # check_value(vr, "Sub 2 Lvl 2 Qty", sub_order_2_lv2_qty.name, "50")
        # check_value(vr, "Sub 2 Lvl 2 ExecPcy", sub_order_2_lv2_exec_pcy.name, "DMA")
        # check_value(vr, "Sub order Lvl 2 count", lvl2_count, "3")
        call(common_win_act.verifyEntities, vr)

    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe_2(case_id, session_id)
    # GUI section end

    replace_order_params = {
        **reusable_params,
        'OrigClOrdID': new_iceberg_order_params['ClOrdID'],
        'ClOrdID': bca.client_orderid(9),
        'Instrument': case_params['Instrument'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': case_params['OrderQty'],
        'Price': case_params['NewPrice'],
        'CFICode': 'EMXXXB',
        'ExDestination': 'QDL1',
        'DisplayInstruction': {
            'DisplayQty': '45'
        }
    }

    logger.debug(f"Send replace order with ClOrdID = {replace_order_params['ClOrdID']}")
    replace_order = act.placeOrderReplaceFIX(
        bca.convert_to_request(
            'Send OrderCancelReplaceRequest',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('OrderCancelReplaceRequest', replace_order_params, case_params['TraderConnectivity'])
        ))
    checkpoint2 = replace_order.checkpoint_id

    replacement_er_params = {
        **reusable_params,
        'ClOrdID': replace_order_params['ClOrdID'],
        'OrigClOrdID': replace_order_params['OrigClOrdID'],
        'OrderID': new_er_params['OrderID'],
        'ExecID': '*',
        'CumQty': '*',
        'LastPx': '*',
        'LastQty': '*',
        'QtyType': '*',
        'AvgPx': '*',
        'OrdStatus': '*',
        'ExecType': '5',
        'LeavesQty': case_params['OrderQty'],
        'Instrument': case_params['Instrument'],
        'ExecRestatementReason': '4',
        'Price': case_params['NewPrice'],
        'OrderQty': case_params['OrderQty'],
        'NoParty': '*',
        'NoStrategyParameters': [{'StrategyParameterName': 'ReleasedNbr',
                                  'StrategyParameterType': '1', 'StrategyParameterValue': '1'},
                                 {'StrategyParameterName': 'ReleasedQty',
                                  'StrategyParameterType': '6', 'StrategyParameterValue': '400'}],
        'MaxFloor': '45',
        'TransactTime': '*'
    }

    logger.debug("Verify received Execution Report (OrdStatus = New, ExecType = Replaced)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'OrderReplace ER Received',
            bca.filter_to_grpc('ExecutionReport', replacement_er_params, ["ClOrdID", "OrdStatus"]),
            replace_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )
    bs_cancel_replace_order_params = {
        'Account': case_params['Account'],
        'Instrument': instrument_bs,
        'ClOrdID': '*',
        'OrderID': '*',
        'Side': case_params['Side'],
        'TransactTime': '*',
        'OrderQty': new_iceberg_order_params['DisplayInstruction']['DisplayQty'],
        'ChildOrderID': '*',
        'IClOrdIdCO': new_iceberg_order_params['IClOrdIdCO'],
        'IClOrdIdAO': new_iceberg_order_params['IClOrdIdAO'],
        'ExDestination': new_iceberg_order_params['ExDestination'],
        'OrigClOrdID': '*'
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Check OrderCancelRequest for Replacement >> PARIS',
            bca.filter_to_grpc('OrderCancelRequest', bs_cancel_replace_order_params),
            checkpoint2,
            case_params['TraderConnectivity2'],
            case_id
        )
    )

    replace_nos_bs_params = {
        **reusable_params,
        'HandlInst': '1',
        'OrderQty': replace_order_params['DisplayInstruction']['DisplayQty'],
        'Price': replace_order_params['Price'],
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'TransactTime': '*',
        'IClOrdIdCO': new_iceberg_order_params['IClOrdIdCO'],
        'IClOrdIdAO': new_iceberg_order_params['IClOrdIdAO'],
        'Instrument': instrument_bs,
        'ExDestination': new_iceberg_order_params['ExDestination']

    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            'Replacement NOS transmitted >> PARIS',
            bca.filter_to_grpc('NewOrderSingle', replace_nos_bs_params, ["ClOrdID"]),
            checkpoint2,
            case_params['TraderConnectivity2'],
            case_id
        )
    )

    replace_er_bs_params = {
        'ClOrdID': '*',
        'OrderID': '*',
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'OrderQty': replace_order_params['DisplayInstruction']['DisplayQty'],
        'OrdType': case_params['OrdType'],
        'Side': case_params['Side'],
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '0',
        'LeavesQty': '0',
        'Text': '*'
    }

    logger.debug("Verify received Execution Report (OrdStatus = New)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Replacement ER transmitted << PARIS',
            bca.filter_to_grpc('ExecutionReport', replace_er_bs_params, ["ClOrdID", "OrdStatus"]),
            checkpoint2,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        )
    )
    cancel_order_params = {
        'OrigClOrdID': new_iceberg_order_params['ClOrdID'],
        'ClOrdID': new_iceberg_order_params['ClOrdID'],
        'Instrument': new_iceberg_order_params['Instrument'],
        'ExDestination': 'QDL1',
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': case_params['OrderQty'],
        'Text': 'Cancel order'
    }

    cancel_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send CancelOrderRequest',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params, case_params['TraderConnectivity']),
        ))

    cancellation_er_params = {
        **reusable_params,
        'Instrument': case_params['Instrument'],
        'ClOrdID': cancel_order_params['ClOrdID'],
        'OrderID': new_er_params['OrderID'],
        'OrderQty': replace_order_params['OrderQty'],
        'Price': replace_order_params['Price'],
        'TransactTime': '*',
        'ExecID': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'ExecRestatementReason': '4',
        'NoParty': '*',
        'NoStrategyParameters': [{'StrategyParameterName': 'ReleasedNbr',
                                  'StrategyParameterType': '1', 'StrategyParameterValue': '1'},
                                 {'StrategyParameterName': 'ReleasedQty',
                                  'StrategyParameterType': '6', 'StrategyParameterValue': '400'}],
        'MaxFloor': '45',
        'Text': '*',
        'OrigClOrdID': '*'
    }
    bs_cancel_order_params = {
        'Account': case_params['Account'],
        'Instrument': instrument_bs,
        'ClOrdID': '*',
        'OrderID': '*',
        'Side': case_params['Side'],
        'TransactTime': '*',
        'OrderQty': replace_order_params['DisplayInstruction']['DisplayQty'],
        'IClOrdIdCO': new_iceberg_order_params['IClOrdIdCO'],
        'IClOrdIdAO': new_iceberg_order_params['IClOrdIdAO'],
        'ChildOrderID': '*',
        'ExDestination': new_iceberg_order_params['ExDestination'],
        'OrigClOrdID': '*'
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Check OrderCancelRequest >> PARIS',
            bca.filter_to_grpc('OrderCancelRequest', bs_cancel_order_params),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity2'],
            case_id
        )
    )

    verifier.submitCheckRule(
        bca.create_check_rule(
            'Cancellation ER Received',
            bca.filter_to_grpc('ExecutionReport', cancellation_er_params, ["ClOrdID", "OrdStatus"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    pre_filter_sim_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL"),
            'SenderCompID': case_params['SenderCompID2'],
            'TargetCompID': case_params['TargetCompID2']
        }
    }
    pre_filter_sim = bca.prefilter_to_grpc(pre_filter_sim_params)
    message_filters_sim = [
        bca.filter_to_grpc('NewOrderSingle', nos_bs_params),
        bca.filter_to_grpc('OrderCancelRequest', bs_cancel_replace_order_params),
        bca.filter_to_grpc('NewOrderSingle', replace_nos_bs_params),
        bca.filter_to_grpc('OrderCancelRequest', bs_cancel_order_params),
    ]
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side messages from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_sim,
            checkpoint=checkpoint,
            connectivity=case_params['TraderConnectivity2'],
            event_id=case_id,
            timeout=2000
        )
    )

    if timeouts:
        sleep(5)

    for rule in [NOS, OCRR, OCR]:
        Stubs.core.removeRule(rule)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
