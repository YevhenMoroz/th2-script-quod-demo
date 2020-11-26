import logging
from copy import deepcopy
from time import sleep
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import verifier_pb2, infra_pb2
from grpc_modules.act_fix_pb2_grpc import ActStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = ActStub(case_params['act'])
    verifier = VerifierStub(case_params['verifier'])
    seconds, nanos = bca.timestamps()  # Store case start time
    reusable_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': case_params['TargetStrategy']
    }

    bca.create_event(EventStoreServiceStub(case_params['event-store']), case_name, case_params['case_id'], report_id)

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
        'DisplayInstruction': {'DisplayQty': '50'}
    }

    logger.debug(f"Send new order with ClOrdID = {new_iceberg_order_params['ClOrdID']}")
    new_iceberg_order = act.placeOrderFIX(
        bca.convert_to_request(
            "Send NewIcebergOrder",
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_iceberg_order_params)
        ))

    checkpoint = new_iceberg_order.checkpoint_id

    execution_report_params_1 = {
        **reusable_params,
        'OrderQty': new_iceberg_order_params['OrderQty'],
        'Price': new_iceberg_order_params['Price'],
        'ClOrdID': new_iceberg_order_params['ClOrdID'],
        'OrderID': new_iceberg_order.response_message.fields['OrderID'].simple_value,
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
            "Receive Execution Report Pending",
            bca.filter_to_grpc("ExecutionReport", execution_report_params_1, ['ClOrdID', 'OrdStatus']),
            checkpoint,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    execution_report_params_2 = deepcopy(execution_report_params_1)
    execution_report_params_2['OrdStatus'] = execution_report_params_2['ExecType'] = '0'
    execution_report_params_2['Instrument'] = {
        'Symbol': case_params['Instrument']['Symbol'],
        'SecurityExchange': case_params['Instrument']['SecurityExchange']
    }
    execution_report_params_2['ExecRestatementReason'] = '4'
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Verify received Execution Report (OrdStatus = New)",
            bca.filter_to_grpc("ExecutionReport", execution_report_params_2, ['ClOrdID', 'OrdStatus']),
            checkpoint,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    replace_order_params = {
        'OrigClOrdID': new_iceberg_order_params['ClOrdID'],
        'ClOrdID': bca.client_orderid(9),
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Instrument': case_params['Instrument'],
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrdType': case_params['OrdType'],
        'OrderQty': case_params['OrderQty'],
        'Price': case_params['NewPrice'],
        'OrderCapacity': 'A',
        'CFICode': 'EMXXXB',
        'ExDestination': 'QDL1',
        'Currency': 'EUR',
        'TimeInForce': '0',
        'IClOrdIdAO': '1543927957',
        'DisplayInstruction': {'DisplayQty': '45'}
    }

    logger.debug(f"Send replace order with ClOrdID = {replace_order_params['ClOrdID']}")
    replace_order = act.placeOrderReplaceFIX(
        bca.convert_to_request(
            'Send OrderCancelReplaceRequest',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('OrderCancelReplaceRequest', replace_order_params)
        ))

    execution_report_params_3 = {
        **reusable_params,
        'ClOrdID': replace_order_params['ClOrdID'],
        'OrderID': execution_report_params_1['OrderID'],
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
        'NoParty': '*',
        'DisplayInstruction': {'DisplayQty': '45'}
    }

    logger.debug("Verify received Execution Report (OrdStatus = New, ExecType = Replaced)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport3',
            bca.filter_to_grpc('ExecutionReport', execution_report_params_3, ["ClOrdID", "OrdStatus"]),
            replace_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    if timeouts:
        sleep(5)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
