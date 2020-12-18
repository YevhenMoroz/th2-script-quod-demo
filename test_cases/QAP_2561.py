import logging
from copy import deepcopy
from time import sleep
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import verifier_pb2, infra_pb2
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier

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
            'Symbol': 'FR0000125460_EUR',
            'SecurityID': 'FR0000125460',
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
            bca.message_to_grpc('NewOrderSingle', new_iceberg_order_params)
        ))

    checkpoint = new_iceberg_order.checkpoint_id

    pending_er_params = {
        **reusable_params,
        'OrderQty': new_iceberg_order_params['OrderQty'],
        'Price': new_iceberg_order_params['Price'],
        'ClOrdID': new_iceberg_order_params['ClOrdID'],
        'OrderID': new_iceberg_order.response_messages_list[0].fields['OrderID'].simple_value,
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
        'NoParty': '*'
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
    new_er_params['Instrument'] = {
        'Symbol': case_params['Instrument']['Symbol'],
        'SecurityExchange': case_params['Instrument']['SecurityExchange']
    }
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
        'Symbol': 'PAR',
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
        'ExDestination': 'XPAR'

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
        # 'LastPx': '0',
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
            infra_pb2.Direction.Value("SECOND")
        )
    )

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
        'IClOrdIdAO': '1543927957',
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
            bca.message_to_grpc('OrderCancelReplaceRequest', replace_order_params)
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
        'Instrument': {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        },
        'ExecRestatementReason': '4',
        'Price': case_params['NewPrice'],
        'OrderQty': case_params['OrderQty'],
        'NoParty': '*'
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
        'IClOrdIdAO': new_iceberg_order_params['IClOrdIdAO']
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
        'IClOrdIdAO': replace_order_params['IClOrdIdAO'],
        'Instrument': instrument_bs,
        'ExDestination': 'XPAR'

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
        # 'LastPx': '0',
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
            infra_pb2.Direction.Value("SECOND")
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
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params),
        ))

    cancellation_er_params = {
        **reusable_params,
        'Instrument': {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        },
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
        'NoParty': '*'
    }
    bs_cancel_order_params = {
        'Account': case_params['Account'],
        'Instrument': instrument_bs,
        'ClOrdID': '*',
        'OrderID': '*',
        'Side': case_params['Side'],
        'TransactTime': '*',
        'OrderQty': replace_order_params['DisplayInstruction']['DisplayQty'],
        'IClOrdIdAO': replace_order_params['IClOrdIdAO'],
        'ChildOrderID': '*',
        'ExDestination': new_iceberg_order_params['ExDestination']
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
        },
        # 'TestReqID': ('TEST', "NOT_EQUAL")
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

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
